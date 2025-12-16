"""
Stage 1: Identification Module
Scans target profiles from LinkedIn, PubMed, and Conference attendee lists
"""

import requests
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Lead:
    """Data class to represent a lead"""
    name: str
    title: str
    company: str
    location: str
    company_hq: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    pubmed_papers: List[Dict] = None
    conference_attendance: List[str] = None
    funding_info: Optional[Dict] = None
    score: int = 0
    
    def __post_init__(self):
        if self.pubmed_papers is None:
            self.pubmed_papers = []
        if self.conference_attendance is None:
            self.conference_attendance = []


class LinkedInSearcher:
    """Search LinkedIn profiles based on criteria"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LinkedIn searcher
        Note: In production, use LinkedIn API or Proxycurl API
        """
        self.api_key = api_key
        self.base_url = "https://nubela.co/proxycurl/api/v2/linkedin" if api_key else None
    
    def search_profiles(self, 
                       job_titles: List[str],
                       keywords: List[str] = None,
                       locations: List[str] = None,
                       limit: int = 100) -> List[Dict]:
        """
        Search LinkedIn profiles
        Note: This is a mock implementation. In production, integrate with:
        - LinkedIn Sales Navigator API
        - Proxycurl API
        - Or use web scraping (with proper rate limiting)
        """
        logger.info(f"Searching LinkedIn for: {job_titles}")
        
        # Mock data for demonstration
        # In production, replace with actual API calls
        mock_profiles = [
            {
                "name": "Dr. Sarah Johnson",
                "title": "Director of Toxicology",
                "company": "Pfizer Inc",
                "location": "Cambridge, MA",
                "linkedin_url": "https://linkedin.com/in/sarah-johnson",
                "company_hq": "New York, NY"
            },
            {
                "name": "Dr. Michael Chen",
                "title": "Head of Preclinical Safety",
                "company": "Moderna Therapeutics",
                "location": "Boston, MA",
                "linkedin_url": "https://linkedin.com/in/michael-chen",
                "company_hq": "Cambridge, MA"
            },
            {
                "name": "Dr. Emily Rodriguez",
                "title": "VP Preclinical Development",
                "company": "Biogen",
                "location": "San Francisco, CA",
                "linkedin_url": "https://linkedin.com/in/emily-rodriguez",
                "company_hq": "Cambridge, MA"
            }
        ]
        
        # Filter based on job titles
        filtered = [p for p in mock_profiles if any(title.lower() in p["title"].lower() for title in job_titles)]
        
        return filtered[:limit]
    
    def get_profile_details(self, linkedin_url: str) -> Dict:
        """Get detailed profile information"""
        # Mock implementation
        return {
            "email": None,  # Would be enriched later
            "phone": None,
            "experience": [],
            "education": []
        }


class PubMedSearcher:
    """Search PubMed for relevant papers and authors"""
    
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def search_papers(self, 
                     keywords: List[str],
                     max_results: int = 50,
                     years: int = 2) -> List[Dict]:
        """
        Search PubMed for papers matching keywords
        """
        import urllib.parse
        
        logger.info(f"Searching PubMed for: {keywords}")
        
        # Build search query
        query_terms = " OR ".join([f'"{term}"' for term in keywords])
        query = f"{query_terms} AND (\"{2024 - years + 1}\"[Publication Date] : \"{2024}\"[Publication Date])"
        
        try:
            # Search API
            search_url = f"{self.base_url}/esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "retmode": "json"
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                pmids = data.get("esearchresult", {}).get("idlist", [])
                
                # Fetch details for each paper
                papers = []
                for pmid in pmids[:max_results]:
                    paper = self._get_paper_details(pmid)
                    if paper:
                        papers.append(paper)
                    time.sleep(0.1)  # Rate limiting
                
                return papers
        except Exception as e:
            logger.error(f"Error searching PubMed: {e}")
            # Return mock data for demonstration
            return self._get_mock_papers()
    
    def _get_paper_details(self, pmid: str) -> Optional[Dict]:
        """Get detailed information about a paper"""
        try:
            fetch_url = f"{self.base_url}/efetch.fcgi"
            params = {
                "db": "pubmed",
                "id": pmid,
                "retmode": "xml"
            }
            
            response = requests.get(fetch_url, params=params, timeout=10)
            if response.status_code == 200:
                # Parse XML response (simplified)
                # In production, use proper XML parsing
                return {
                    "pmid": pmid,
                    "title": f"Research Paper {pmid}",
                    "authors": [],
                    "year": 2024,
                    "journal": "Journal of Toxicology"
                }
        except Exception as e:
            logger.error(f"Error fetching paper {pmid}: {e}")
        
        return None
    
    def _get_mock_papers(self) -> List[Dict]:
        """Return mock papers for demonstration"""
        return [
            {
                "pmid": "12345678",
                "title": "Drug-Induced Liver Injury: A Comprehensive Review",
                "authors": ["Dr. Sarah Johnson", "Dr. John Smith"],
                "year": 2024,
                "journal": "Toxicology and Applied Pharmacology"
            },
            {
                "pmid": "12345679",
                "title": "3D In-Vitro Models for Hepatic Toxicity Assessment",
                "authors": ["Dr. Michael Chen", "Dr. Lisa Wang"],
                "year": 2023,
                "journal": "Biomaterials"
            }
        ]
    
    def extract_authors_from_papers(self, papers: List[Dict]) -> List[Dict]:
        """Extract author information from papers"""
        authors = []
        for paper in papers:
            for author in paper.get("authors", []):
                authors.append({
                    "name": author,
                    "paper_title": paper.get("title"),
                    "year": paper.get("year"),
                    "pmid": paper.get("pmid")
                })
        return authors


class ConferenceSearcher:
    """Search conference attendee lists and abstracts"""
    
    def __init__(self):
        self.conferences = {
            "SOT": "Society of Toxicology",
            "AACR": "American Association for Cancer Research",
            "ISSX": "International Society for the Study of Xenobiotics",
            "ACT": "American College of Toxicology"
        }
    
    def search_attendees(self, 
                       conference: str,
                       keywords: List[str] = None) -> List[Dict]:
        """
        Search conference attendees and presenters
        Note: This is a mock implementation. In production, would scrape
        conference websites or use their APIs if available.
        """
        logger.info(f"Searching {conference} conference")
        
        # Mock data
        mock_attendees = [
            {
                "name": "Dr. Sarah Johnson",
                "title": "Director of Toxicology",
                "company": "Pfizer Inc",
                "presentation": "Poster: 3D Liver Models for DILI Assessment",
                "conference": conference
            },
            {
                "name": "Dr. Emily Rodriguez",
                "title": "VP Preclinical Development",
                "company": "Biogen",
                "presentation": "Oral: New Approach Methodologies in Safety",
                "conference": conference
            }
        ]
        
        return mock_attendees


class IdentificationEngine:
    """Main identification engine that coordinates all sources"""
    
    def __init__(self, linkedin_api_key: Optional[str] = None):
        self.linkedin_searcher = LinkedInSearcher(linkedin_api_key)
        self.pubmed_searcher = PubMedSearcher()
        self.conference_searcher = ConferenceSearcher()
    
    def identify_leads(self,
                      job_titles: List[str],
                      keywords: List[str] = None,
                      locations: List[str] = None,
                      max_results: int = 500) -> List[Lead]:
        """
        Main method to identify leads from all sources
        """
        logger.info("Starting lead identification process...")
        
        leads_dict = {}  # Use name+company as key to deduplicate
        
        # 1. Search LinkedIn
        linkedin_profiles = self.linkedin_searcher.search_profiles(
            job_titles=job_titles,
            keywords=keywords,
            locations=locations,
            limit=max_results
        )
        
        for profile in linkedin_profiles:
            key = f"{profile['name']}_{profile['company']}"
            leads_dict[key] = Lead(
                name=profile["name"],
                title=profile["title"],
                company=profile["company"],
                location=profile.get("location", ""),
                company_hq=profile.get("company_hq"),
                linkedin_url=profile.get("linkedin_url")
            )
        
        # 2. Search PubMed
        if keywords:
            pubmed_keywords = keywords + [
                "Drug-Induced Liver Injury",
                "3D cell culture",
                "Organ-on-chip",
                "Hepatic spheroids",
                "Investigative Toxicology"
            ]
            papers = self.pubmed_searcher.search_papers(
                keywords=pubmed_keywords,
                max_results=100
            )
            
            authors = self.pubmed_searcher.extract_authors_from_papers(papers)
            
            for author_info in authors:
                author_name = author_info["name"]
                # Try to match with existing leads or create new
                matched = False
                for key, lead in leads_dict.items():
                    if author_name.lower() in lead.name.lower() or lead.name.lower() in author_name.lower():
                        lead.pubmed_papers.append({
                            "title": author_info["paper_title"],
                            "year": author_info["year"],
                            "pmid": author_info["pmid"]
                        })
                        matched = True
                        break
                
                if not matched:
                    # Create new lead from author
                    key = f"{author_name}_Unknown"
                    leads_dict[key] = Lead(
                        name=author_name,
                        title="Researcher",
                        company="Unknown",
                        location="",
                        pubmed_papers=[{
                            "title": author_info["paper_title"],
                            "year": author_info["year"],
                            "pmid": author_info["pmid"]
                        }]
                    )
        
        # 3. Search Conferences
        for conf_name in ["SOT", "AACR", "ISSX", "ACT"]:
            attendees = self.conference_searcher.search_attendees(
                conference=conf_name,
                keywords=keywords
            )
            
            for attendee in attendees:
                key = f"{attendee['name']}_{attendee['company']}"
                if key in leads_dict:
                    leads_dict[key].conference_attendance.append(conf_name)
                else:
                    leads_dict[key] = Lead(
                        name=attendee["name"],
                        title=attendee["title"],
                        company=attendee["company"],
                        location="",
                        conference_attendance=[conf_name]
                    )
        
        leads = list(leads_dict.values())
        logger.info(f"Identified {len(leads)} unique leads")
        
        return leads[:max_results]

