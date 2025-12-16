# Quick Start Guide

## Setup Complete! ✅

Your environment has been set up and dependencies installed.

## Running the Application

### Option 1: Using the command that's already running
The Streamlit app should be starting. Look for output in your terminal that says:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Option 2: Start manually
If you need to start it again, run these commands:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the app
streamlit run app.py
```

## Using the Application

1. **Open your browser** to `http://localhost:8501` (or the URL shown in terminal)

2. **Configure search criteria** in the sidebar:
   - Job Titles: Enter titles like "Director of Toxicology", "Head of Preclinical Safety"
   - Keywords: Add search terms like "Drug-Induced Liver Injury", "3D cell culture"
   - Locations: Specify locations like "Boston, Cambridge, San Francisco"
   - Maximum Results: Set how many leads you want (default: 100)

3. **Click "🚀 Generate Leads"** to start the process

4. **View results** in the dashboard:
   - Search and filter leads
   - View score distribution
   - Export to CSV or Excel

## Troubleshooting

### If Streamlit doesn't start:
- Make sure the virtual environment is activated: `.\venv\Scripts\Activate.ps1`
- Check if port 8501 is already in use
- Try: `streamlit run app.py --server.port 8502`

### If you see import errors:
- Make sure you're in the project directory
- Activate the virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

## Next Steps

- The app uses mock data for demonstration
- For production use, integrate with actual APIs:
  - LinkedIn Sales Navigator API
  - Email finder APIs (Hunter.io, Apollo.io)
  - Funding intelligence APIs (Crunchbase, PitchBook)

