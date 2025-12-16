# 3D In-Vitro Models Lead Generation Tool

A comprehensive web agent/crawler that identifies, enriches, and ranks high-probability leads for 3D in-vitro models helping researchers design new therapies.

## 🌐 Live Demo

**👉 [Try the application online](https://your-app-name.streamlit.app)** *(Replace with your actual Streamlit Cloud URL after deployment)*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

> **Note**: After deploying to Streamlit Cloud, replace `https://your-app-name.streamlit.app` above with your actual deployment URL.

## 🎯 Overview

This tool acts as a business development assistant that crawls the web for relevant information to output well-qualified leads. It identifies potential customers, enriches their data, and ranks them by their probability of wanting to work with 3D in-vitro model solutions.

## 🏗️ Architecture

The tool operates in three main stages:

### Stage 1: Identification
Scans target profiles based on criteria (e.g., Director of Toxicology, Head of Preclinical Safety) from:
- **LinkedIn** (and Sales Navigator)
- **PubMed** (for authors of recent relevant papers)
- **Conference attendee lists** (e.g., SOT - Society of Toxicology)

### Stage 2: Enrichment
For each identified person, the tool queries external databases to find:
- **Contact Info**: Business email and phone numbers
- **Location Data**: Distinguishes between Person's Location (e.g., remote in Colorado) and Company HQ (e.g., Cambridge, MA)
- **Company Intelligence**: Funding information, technographic signals

### Stage 3: Ranking
Applies "Propensity to Buy" score (0-100) based on weighted criteria:

| Signal | Category | Criteria | Weight |
|--------|----------|----------|--------|
| Title contains | Role Fit | Toxicology, Safety, Hepatic, 3D | High (+30) |
| Company Intent | Funding | Series A/B funding, cash to spend | High (+20) |
| Technographic | Tech Usage | Uses similar tech (in vitro models) | Medium (+15) |
| Technographic | NAMs | Open to New Approach Methodologies | Medium (+10) |
| Location | Hub | Boston/Cambridge, Bay Area, Basel, UK Golden Triangle | Medium (+10) |
| Scientific Intent | Publications | Published on DILI/3D models in last 2 years | Very High (+40) |

## 🚀 Getting Started

### Option 1: Use the Live Demo (Recommended)

Simply visit the [Live Demo](https://your-app-name.streamlit.app) link above - no installation required!

### Option 2: Run Locally

#### Prerequisites

- Python 3.8 or higher
- pip package manager

#### Installation

1. Clone this repository:
```bash
git clone https://github.com/siddheshmm/3D-In-Vitro-Models-Lead-Generation-Tool.git
cd 3D-In-Vitro-Models-Lead-Generation-Tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Streamlit dashboard:
```bash
streamlit run app.py
```

2. Open your browser to the URL shown in the terminal (typically `http://localhost:8501`)

3. Configure your search criteria in the sidebar:
   - Enter job titles (one per line)
   - Add keywords for PubMed searches
   - Specify locations to filter by
   - Set maximum number of results

4. Click "🚀 Generate Leads" to start the process

5. View, search, and export your ranked leads from the dashboard

## 📊 Features

- **Multi-Source Identification**: Aggregates leads from LinkedIn, PubMed, and conference attendee lists
- **Data Enrichment**: Automatically finds contact information and company intelligence
- **Intelligent Ranking**: Scores leads based on multiple weighted signals
- **Interactive Dashboard**: Searchable, filterable table with real-time updates
- **Export Functionality**: Download results as CSV or Excel files
- **Location Intelligence**: Distinguishes between person location and company HQ

## 🔧 Configuration

### API Keys (Optional)

For production use, you can configure API keys in the sidebar:
- **LinkedIn/Proxycurl API Key**: For enhanced LinkedIn profile data
- **Email Finder API Key**: For email discovery services (Hunter.io, Apollo.io, etc.)
- **Funding Intelligence API Key**: For Crunchbase/PitchBook integration

Note: The tool works with mock data for demonstration purposes. Replace mock implementations with actual API integrations for production use.

## 📁 Project Structure

```
euprime-submission/
├── app.py                 # Main Streamlit application
├── src/
│   ├── identification.py  # Stage 1: Lead identification
│   ├── enrichment.py      # Stage 2: Data enrichment
│   └── ranking.py         # Stage 3: Lead ranking/scoring
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

## 🎓 Data Sources

The tool searches through five main categories of websites:

1. **Professional Social Networks**: LinkedIn, Xing
2. **Scientific Publication Databases**: PubMed, Google Scholar, bioRxiv
3. **Biomedical Conference Event Sites**: SOT, AACR, ISSX, ACT
4. **Business & Funding Intelligence**: Crunchbase, PitchBook, FierceBiotech
5. **Public Grant Databases**: NIH RePORTER (USA), CORDIS (EU)

## 📝 Example Output

The dashboard displays leads in a searchable table with columns:
- Rank
- Probability Score
- Name
- Title
- Company
- Location (with HQ distinction)
- Email
- LinkedIn
- Number of Papers
- Conference Attendance
- Funding Stage

## 🔄 Future Enhancements

- Integration with actual LinkedIn Sales Navigator API
- Real-time PubMed API integration
- Conference website scraping automation
- Advanced email verification
- Machine learning-based scoring refinement
- Automated outreach email generation

## 📄 License

This project is created for the EuPrime job application assignment.

## 👤 Author

Created for EuPrime job application submission.

---

**Note**: This is a demonstration version. For production use, integrate with actual APIs and implement proper rate limiting, error handling, and data validation.

