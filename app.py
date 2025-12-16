"""
Lead Generation Dashboard - Main Streamlit Application
3D In-Vitro Models Lead Generation Tool
"""

import streamlit as st
import pandas as pd
from io import BytesIO
import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from identification import IdentificationEngine, Lead
from enrichment import EnrichmentEngine
from ranking import RankingEngine

# Page configuration
st.set_page_config(
    page_title="3D In-Vitro Models Lead Generator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def export_to_csv(df: pd.DataFrame) -> BytesIO:
    """Convert DataFrame to CSV bytes"""
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output


def export_to_excel(df: pd.DataFrame) -> BytesIO:
    """Convert DataFrame to Excel bytes"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Leads')
    output.seek(0)
    return output


def format_location_display(lead: Lead) -> str:
    """Format location display showing person location vs HQ"""
    if lead.location and lead.company_hq:
        if lead.location.lower() != lead.company_hq.lower():
            return f"{lead.location} (HQ: {lead.company_hq})"
        else:
            return lead.location
    elif lead.location:
        return lead.location
    elif lead.company_hq:
        return f"HQ: {lead.company_hq}"
    return "Unknown"


def main():
    """Main application"""
    
    # Header
    st.markdown('<p class="main-header">🔬 3D In-Vitro Models Lead Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Identify, Enrich, and Rank High-Probability Leads</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("Search Criteria")
        
        # Job titles input
        job_titles_input = st.text_area(
            "Job Titles (one per line)",
            value="Director of Toxicology\nHead of Preclinical Safety\nVP Preclinical Development",
            help="Enter job titles to search for, one per line"
        )
        job_titles = [title.strip() for title in job_titles_input.split("\n") if title.strip()]
        
        # Keywords input
        keywords_input = st.text_area(
            "Keywords",
            value="Drug-Induced Liver Injury\n3D cell culture\nHepatic spheroids",
            help="Enter keywords for PubMed and conference searches"
        )
        keywords = [kw.strip() for kw in keywords_input.split("\n") if kw.strip()]
        
        # Locations input
        locations_input = st.text_input(
            "Locations (comma-separated)",
            value="Boston, Cambridge, San Francisco, Basel",
            help="Enter locations to filter by"
        )
        locations = [loc.strip() for loc in locations_input.split(",") if loc.strip()]
        
        # Max results
        max_results = st.slider(
            "Maximum Results",
            min_value=10,
            max_value=1000,
            value=100,
            step=10
        )
        
        # API Keys (optional)
        st.subheader("API Keys (Optional)")
        linkedin_api_key = st.text_input("LinkedIn/Proxycurl API Key", type="password")
        email_api_key = st.text_input("Email Finder API Key", type="password")
        funding_api_key = st.text_input("Funding Intelligence API Key", type="password")
        
        # Run button
        run_analysis = st.button("🚀 Generate Leads", type="primary", use_container_width=True)
    
    # Main content area
    if run_analysis:
        with st.spinner("Identifying leads from multiple sources..."):
            # Initialize engines
            identification_engine = IdentificationEngine(linkedin_api_key=linkedin_api_key)
            enrichment_engine = EnrichmentEngine(
                email_api_key=email_api_key,
                funding_api_key=funding_api_key
            )
            ranking_engine = RankingEngine()
            
            # Stage 1: Identification
            st.info("🔍 Stage 1: Identifying leads from LinkedIn, PubMed, and Conferences...")
            leads = identification_engine.identify_leads(
                job_titles=job_titles,
                keywords=keywords,
                locations=locations,
                max_results=max_results
            )
            
            if not leads:
                st.warning("No leads found. Please adjust your search criteria.")
                return
            
            # Stage 2: Enrichment
            st.info("📊 Stage 2: Enriching leads with contact info, location, and company data...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            enriched_leads = []
            for i, lead in enumerate(leads):
                try:
                    enrichment_engine.enrich_lead(lead)
                    enriched_leads.append(lead)
                    progress_bar.progress((i + 1) / len(leads))
                    status_text.text(f"Enriched {i + 1}/{len(leads)} leads...")
                except Exception as e:
                    logger.error(f"Error enriching lead {lead.name}: {e}")
                    enriched_leads.append(lead)  # Add even if enrichment fails
            
            progress_bar.empty()
            status_text.empty()
            
            # Stage 3: Ranking
            st.info("🎯 Stage 3: Ranking leads by propensity to buy...")
            ranked_leads = ranking_engine.rank_leads(enriched_leads)
            
            st.success(f"✅ Generated {len(ranked_leads)} leads!")
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Leads", len(ranked_leads))
            with col2:
                high_score_count = sum(1 for lead in ranked_leads if lead.score >= 70)
                st.metric("High Score (≥70)", high_score_count)
            with col3:
                avg_score = sum(lead.score for lead in ranked_leads) / len(ranked_leads) if ranked_leads else 0
                st.metric("Average Score", f"{avg_score:.1f}")
            with col4:
                with_email = sum(1 for lead in ranked_leads if lead.email)
                st.metric("With Email", with_email)
            
            # Store in session state
            st.session_state['leads'] = ranked_leads
            st.session_state['job_titles'] = job_titles
            st.session_state['keywords'] = keywords
    
    # Display results if available
    if 'leads' in st.session_state and st.session_state['leads']:
        leads = st.session_state['leads']
        
        st.header("📋 Lead Generation Dashboard")
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input(
                "🔍 Search (Name, Company, Location, Title)",
                placeholder="e.g., Boston, Oncology, Director..."
            )
        with col2:
            min_score = st.slider("Min Score", 0, 100, 0, key="min_score")
        
        # Filter leads
        filtered_leads = leads
        if search_query:
            query_lower = search_query.lower()
            filtered_leads = [
                lead for lead in filtered_leads
                if (query_lower in lead.name.lower() or
                    query_lower in lead.company.lower() or
                    query_lower in lead.location.lower() or
                    query_lower in lead.title.lower() or
                    query_lower in (lead.company_hq or "").lower())
            ]
        
        filtered_leads = [lead for lead in filtered_leads if lead.score >= min_score]
        
        # Convert to DataFrame
        leads_data = []
        for lead in filtered_leads:
            leads_data.append({
                "Rank": getattr(lead, 'rank', 0),
                "Probability": f"{lead.score}/100",
                "Name": lead.name,
                "Title": lead.title,
                "Company": lead.company,
                "Location": format_location_display(lead),
                "HQ": lead.company_hq or "Unknown",
                "Email": lead.email or "Not found",
                "LinkedIn": lead.linkedin_url or "N/A",
                "Papers": len(lead.pubmed_papers),
                "Conferences": ", ".join(lead.conference_attendance) if lead.conference_attendance else "None",
                "Funding": lead.funding_info.get("funding_stage", "Unknown") if lead.funding_info else "Unknown"
            })
        
        df = pd.DataFrame(leads_data)
        
        # Display table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=600
        )
        
        # Export buttons
        st.subheader("📥 Export Data")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = export_to_csv(df)
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name="leads_export.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            excel_data = export_to_excel(df)
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name="leads_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col3:
            st.info(f"Showing {len(filtered_leads)} of {len(leads)} leads")
        
        # Score distribution chart
        st.subheader("📈 Score Distribution")
        score_counts = pd.Series([lead.score for lead in filtered_leads])
        st.bar_chart(score_counts.value_counts().sort_index())
        
        # Top 10 leads
        st.subheader("🏆 Top 10 Leads")
        top_10_df = df.head(10)
        st.dataframe(top_10_df, use_container_width=True, hide_index=True)
    
    else:
        # Welcome message
        st.info("👈 Configure your search criteria in the sidebar and click 'Generate Leads' to get started!")
        
        # Show scoring criteria
        with st.expander("📖 Scoring Criteria"):
            st.markdown("""
            ### Propensity to Buy Score (0-100)
            
            The ranking engine assigns scores based on weighted criteria:
            
            | Signal | Category | Criteria | Weight |
            |--------|----------|----------|--------|
            | **Title contains** | Role Fit | Toxicology, Safety, Hepatic, 3D | High (+30) |
            | **Company Intent** | Funding | Series A/B funding, cash to spend | High (+20) |
            | **Technographic** | Tech Usage | Uses similar tech (in vitro models) | Medium (+15) |
            | **Technographic** | NAMs | Open to New Approach Methodologies | Medium (+10) |
            | **Location** | Hub | Boston/Cambridge, Bay Area, Basel, UK Golden Triangle | Medium (+10) |
            | **Scientific Intent** | Publications | Published on DILI/3D models in last 2 years | Very High (+40) |
            
            **Example Scores:**
            - Junior Scientist at non-funded startup: ~15/100
            - Director of Safety at Series B biotech in Cambridge who published on liver toxicity: ~95/100
            """)


if __name__ == "__main__":
    main()

