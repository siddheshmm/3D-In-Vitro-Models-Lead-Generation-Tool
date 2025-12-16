"""
Stage 2: Enrichment Module
Gathers contact information, location data, and company intelligence
"""

import requests
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EnrichmentData:
    """Data class for enrichment results"""
    email: Optional[str] = None
    phone: Optional[str] = None
    company_hq: Optional[str] = None
    funding_info: Optional[Dict] = None
    technographic_signals: List[str] = None
    
    def __post_init__(self):
        if self.technographic_signals is None:
            self.technographic_signals = []


class EmailFinder:
    """Find business email addresses"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize email finder
        Note: In production, use services like:
        - Hunter.io API
        - Apollo.io API
        - Snov.io API
        """
        self.api_key = api_key
    
    def find_email(self, name: str, company: str, domain: Optional[str] = None) -> Optional[str]:
        """
        Find business email for a person
        """
        logger.info(f"Finding email for {name} at {company}")
        
        # Extract domain from company name or use provided domain
        if not domain:
            domain = self._extract_domain(company)
        
        if not domain:
            return None
        
        # Mock implementation - in production, use email finder API
        # Common patterns: firstname.lastname@domain, firstinitial.lastname@domain
        name_parts = name.lower().split()
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = name_parts[-1]
            
            # Try common patterns
            patterns = [
                f"{first_name}.{last_name}@{domain}",
                f"{first_name[0]}{last_name}@{domain}",
                f"{first_name}{last_name}@{domain}",
                f"{first_name}_{last_name}@{domain}"
            ]
            
            # In production, verify email exists using email verification API
            # For now, return first pattern as mock
            return patterns[0]
        
        return None
    
    def _extract_domain(self, company: str) -> Optional[str]:
        """Extract domain from company name"""
        # Common biotech/pharma domains
        domain_map = {
            "pfizer": "pfizer.com",
            "moderna": "modernatx.com",
            "biogen": "biogen.com",
            "gilead": "gilead.com",
            "regeneron": "regeneron.com",
            "vertex": "vrtx.com",
            "amgen": "amgen.com",
            "bristol myers squibb": "bms.com",
            "merck": "merck.com",
            "novartis": "novartis.com",
            "roche": "roche.com"
        }
        
        company_lower = company.lower()
        for key, domain in domain_map.items():
            if key in company_lower:
                return domain
        
        # Generic pattern
        company_slug = re.sub(r'[^a-z0-9]', '', company_lower)
        return f"{company_slug}.com"


class LocationEnricher:
    """Enrich location data - distinguish person location vs company HQ"""
    
    def __init__(self):
        self.hub_locations = [
            "boston", "cambridge", "bay area", "san francisco", "san jose",
            "basel", "london", "oxford", "cambridge uk", "golden triangle"
        ]
    
    def enrich_location(self, 
                       person_location: str,
                       company: str) -> Dict[str, str]:
        """
        Enrich location data and identify if person is in a hub
        """
        company_hq = self._get_company_hq(company)
        
        # Check if person location is a hub
        person_location_lower = person_location.lower()
        is_hub = any(hub in person_location_lower for hub in self.hub_locations)
        
        return {
            "person_location": person_location,
            "company_hq": company_hq,
            "is_hub": is_hub,
            "is_remote": person_location != company_hq and person_location != ""
        }
    
    def _get_company_hq(self, company: str) -> str:
        """Get company headquarters location"""
        # Mock company HQ data
        hq_map = {
            "pfizer": "New York, NY",
            "moderna": "Cambridge, MA",
            "biogen": "Cambridge, MA",
            "gilead": "Foster City, CA",
            "regeneron": "Tarrytown, NY",
            "vertex": "Boston, MA",
            "amgen": "Thousand Oaks, CA",
            "bristol myers squibb": "New York, NY",
            "merck": "Kenilworth, NJ",
            "novartis": "Basel, Switzerland",
            "roche": "Basel, Switzerland"
        }
        
        company_lower = company.lower()
        for key, hq in hq_map.items():
            if key in company_lower:
                return hq
        
        return "Unknown"


class FundingIntelligence:
    """Gather funding and business intelligence"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize funding intelligence
        Note: In production, use:
        - Crunchbase API
        - PitchBook API
        - FierceBiotech RSS feeds
        """
        self.api_key = api_key
    
    def get_funding_info(self, company: str) -> Optional[Dict]:
        """
        Get funding information for a company
        """
        logger.info(f"Fetching funding info for {company}")
        
        # Mock implementation
        # In production, query Crunchbase/PitchBook APIs
        funding_mock_data = {
            "moderna": {
                "recent_funding": "Series B - $50M (2024)",
                "funding_stage": "Series B",
                "amount": 50000000,
                "date": "2024-01-15",
                "has_budget": True
            },
            "biogen": {
                "recent_funding": "IPO - Public Company",
                "funding_stage": "Public",
                "amount": None,
                "date": None,
                "has_budget": True
            }
        }
        
        company_lower = company.lower()
        for key, data in funding_mock_data.items():
            if key in company_lower:
                return data
        
        # Default: assume no recent funding
        return {
            "recent_funding": None,
            "funding_stage": "Unknown",
            "amount": None,
            "date": None,
            "has_budget": False
        }


class TechnographicEnricher:
    """Identify if company uses similar technologies"""
    
    def __init__(self):
        self.tech_keywords = [
            "in vitro models",
            "3d cell culture",
            "organ-on-chip",
            "microphysiological systems",
            "new approach methodologies",
            "nams",
            "hepatic models",
            "spheroids"
        ]
    
    def check_technographics(self, company: str) -> List[str]:
        """
        Check if company uses similar technologies
        Note: In production, would scrape company websites, job postings,
        or use technographic databases
        """
        # Mock implementation
        # In production, would:
        # 1. Scrape company website for keywords
        # 2. Check job postings
        # 3. Query technographic databases
        
        technographic_signals = []
        
        # Mock: some companies use these technologies
        if "moderna" in company.lower() or "biogen" in company.lower():
            technographic_signals.append("Uses in vitro models")
            technographic_signals.append("Open to NAMs")
        
        return technographic_signals


class EnrichmentEngine:
    """Main enrichment engine"""
    
    def __init__(self, 
                 email_api_key: Optional[str] = None,
                 funding_api_key: Optional[str] = None):
        self.email_finder = EmailFinder(email_api_key)
        self.location_enricher = LocationEnricher()
        self.funding_intelligence = FundingIntelligence(funding_api_key)
        self.technographic_enricher = TechnographicEnricher()
    
    def enrich_lead(self, lead) -> None:
        """
        Enrich a lead with all available data
        Modifies the lead object in place
        """
        logger.info(f"Enriching lead: {lead.name}")
        
        # 1. Find email
        if not lead.email:
            lead.email = self.email_finder.find_email(
                name=lead.name,
                company=lead.company
            )
        
        # 2. Enrich location
        location_data = self.location_enricher.enrich_location(
            person_location=lead.location,
            company=lead.company
        )
        lead.company_hq = location_data["company_hq"]
        lead.location = location_data["person_location"]
        
        # 3. Get funding info
        lead.funding_info = self.funding_intelligence.get_funding_info(
            lead.company
        )
        
        # 4. Check technographics
        technographic_signals = self.technographic_enricher.check_technographics(
            lead.company
        )
        # Store in a way that can be used for scoring
        lead.technographic_signals = technographic_signals
    
    def enrich_leads(self, leads: List) -> List:
        """
        Enrich a list of leads
        """
        logger.info(f"Enriching {len(leads)} leads...")
        
        for lead in leads:
            try:
                self.enrich_lead(lead)
            except Exception as e:
                logger.error(f"Error enriching lead {lead.name}: {e}")
        
        return leads

