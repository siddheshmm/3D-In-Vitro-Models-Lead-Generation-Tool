"""
Stage 3: Ranking Module
Applies "Propensity to Buy" score (0-100) based on weighted criteria
"""

import logging
from typing import List
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ScoringWeights:
    """Weights for different scoring signals"""
    role_fit_high: int = 30
    company_intent_high: int = 20
    technographic_medium: int = 15
    technographic_nams: int = 10
    location_hub: int = 10
    scientific_intent_very_high: int = 40


class RankingEngine:
    """Main ranking engine that scores and prioritizes leads"""
    
    def __init__(self, weights: ScoringWeights = None):
        self.weights = weights or ScoringWeights()
        
        # Keywords for role matching
        self.high_value_titles = [
            "director", "head", "vp", "vice president", "chief",
            "senior", "principal", "lead"
        ]
        
        self.role_keywords = [
            "toxicology", "safety", "hepatic", "3d", "preclinical",
            "drug discovery", "pharmacology", "dili"
        ]
        
        # Scientific keywords
        self.scientific_keywords = [
            "drug-induced liver injury",
            "dili",
            "liver toxicity",
            "hepatic",
            "3d model",
            "organ-on-chip"
        ]
    
    def calculate_score(self, lead) -> int:
        """
        Calculate propensity to buy score (0-100) for a lead
        """
        score = 0
        
        # 1. Role Fit - Title contains keywords (High: +30)
        role_score = self._score_role_fit(lead.title)
        score += role_score
        
        # 2. Company Intent - Funding stage (High: +20)
        company_score = self._score_company_intent(lead.funding_info)
        score += company_score
        
        # 3. Technographic - Uses similar tech (Medium: +15)
        tech_score = self._score_technographic(lead.technographic_signals)
        score += tech_score
        
        # 4. Technographic - Open to NAMs (Medium: +10)
        nams_score = self._score_nams(lead.technographic_signals)
        score += nams_score
        
        # 5. Location - In a hub (Medium: +10)
        location_score = self._score_location(lead.location, lead.company_hq)
        score += location_score
        
        # 6. Scientific Intent - Published relevant papers (Very High: +40)
        scientific_score = self._score_scientific_intent(lead.pubmed_papers)
        score += scientific_score
        
        # Cap at 100
        lead.score = min(score, 100)
        
        return lead.score
    
    def _score_role_fit(self, title: str) -> int:
        """Score based on role/title fit"""
        if not title:
            return 0
        
        title_lower = title.lower()
        
        # Check for high-value title keywords
        has_high_value_title = any(
            keyword in title_lower for keyword in self.high_value_titles
        )
        
        # Check for role keywords
        has_role_keyword = any(
            keyword in title_lower for keyword in self.role_keywords
        )
        
        if has_high_value_title and has_role_keyword:
            return self.weights.role_fit_high
        elif has_role_keyword:
            return self.weights.role_fit_high // 2  # Partial score
        
        return 0
    
    def _score_company_intent(self, funding_info: dict) -> int:
        """Score based on company funding and budget"""
        if not funding_info:
            return 0
        
        funding_stage = funding_info.get("funding_stage", "").lower()
        has_budget = funding_info.get("has_budget", False)
        
        # High-value funding stages
        high_value_stages = ["series a", "series b", "series c", "public", "ipo"]
        
        if any(stage in funding_stage for stage in high_value_stages) and has_budget:
            return self.weights.company_intent_high
        elif has_budget:
            return self.weights.company_intent_high // 2
        
        return 0
    
    def _score_technographic(self, technographic_signals: List[str]) -> int:
        """Score based on using similar technologies"""
        if not technographic_signals:
            return 0
        
        tech_keywords = ["in vitro", "3d", "organ-on-chip", "spheroids"]
        
        for signal in technographic_signals:
            signal_lower = signal.lower()
            if any(keyword in signal_lower for keyword in tech_keywords):
                return self.weights.technographic_medium
        
        return 0
    
    def _score_nams(self, technographic_signals: List[str]) -> int:
        """Score based on openness to New Approach Methodologies"""
        if not technographic_signals:
            return 0
        
        for signal in technographic_signals:
            if "nam" in signal.lower():
                return self.weights.technographic_nams
        
        return 0
    
    def _score_location(self, person_location: str, company_hq: str) -> int:
        """Score based on being in a hub location"""
        hub_locations = [
            "boston", "cambridge", "bay area", "san francisco",
            "basel", "london", "oxford", "golden triangle"
        ]
        
        location_lower = (person_location or "").lower()
        hq_lower = (company_hq or "").lower()
        
        # Check if person location or company HQ is in a hub
        for hub in hub_locations:
            if hub in location_lower or hub in hq_lower:
                return self.weights.location_hub
        
        return 0
    
    def _score_scientific_intent(self, pubmed_papers: List[dict]) -> int:
        """Score based on recent relevant publications"""
        if not pubmed_papers:
            return 0
        
        # Check for recent papers (last 2 years) with relevant keywords
        current_year = 2024
        relevant_papers = 0
        
        for paper in pubmed_papers:
            paper_year = paper.get("year", 0)
            paper_title = (paper.get("title", "") or "").lower()
            
            # Check if paper is recent (within 2 years)
            if paper_year >= current_year - 2:
                # Check if paper title contains relevant keywords
                if any(keyword in paper_title for keyword in self.scientific_keywords):
                    relevant_papers += 1
        
        if relevant_papers > 0:
            return self.weights.scientific_intent_very_high
        
        return 0
    
    def rank_leads(self, leads: List) -> List:
        """
        Score and rank all leads by propensity to buy
        """
        logger.info(f"Ranking {len(leads)} leads...")
        
        # Calculate scores
        for lead in leads:
            self.calculate_score(lead)
        
        # Sort by score (descending)
        ranked_leads = sorted(leads, key=lambda x: x.score, reverse=True)
        
        # Add rank number
        for i, lead in enumerate(ranked_leads, 1):
            lead.rank = i
        
        logger.info(f"Ranked leads. Top score: {ranked_leads[0].score if ranked_leads else 0}")
        
        return ranked_leads

