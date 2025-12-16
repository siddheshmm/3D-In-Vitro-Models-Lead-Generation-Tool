# Deploying to Streamlit Cloud

This guide will help you deploy your 3D In-Vitro Models Lead Generation Tool to Streamlit Cloud.

## Prerequisites

1. A GitHub account (you already have this: https://github.com/siddheshmm/3D-In-Vitro-Models-Lead-Generation-Tool)
2. A Streamlit Cloud account (free at https://streamlit.io/cloud)

## Step-by-Step Deployment Instructions

### Step 1: Sign up for Streamlit Cloud

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "Sign up" or "Get started"
3. Sign in with your GitHub account
4. Authorize Streamlit Cloud to access your GitHub repositories

### Step 2: Deploy Your App

1. Once logged in, click **"New app"** button
2. You'll see a form with the following fields:

   **App name**: 
   - Enter a name like `3d-invitro-lead-generator` or `euprime-lead-tool`
   
   **Repository**: 
   - Select: `siddheshmm/3D-In-Vitro-Models-Lead-Generation-Tool`
   
   **Branch**: 
   - Select: `main`
   
   **Main file path**: 
   - Enter: `app.py`
   
   **Python version**: 
   - Select: `3.12` (or the version you're using)

3. Click **"Deploy!"**

### Step 3: Wait for Deployment

- Streamlit Cloud will:
  1. Clone your repository
  2. Install dependencies from `requirements.txt`
  3. Run your app
  4. Provide you with a public URL

### Step 4: Access Your App

- Once deployed, you'll get a URL like:
  `https://your-app-name.streamlit.app`
- Share this URL with anyone who needs access!

## Configuration Files

Your repository already includes:
- ✅ `requirements.txt` - All Python dependencies
- ✅ `app.py` - Main application file
- ✅ `.streamlit/config.toml` - Streamlit configuration (optional)

## Troubleshooting

### If deployment fails:

1. **Check requirements.txt**:
   - Make sure all dependencies are listed
   - Check for any version conflicts

2. **Check file paths**:
   - Ensure `app.py` is in the root directory
   - Ensure `src/` folder exists with all modules

3. **Check logs**:
   - Click on your app in Streamlit Cloud dashboard
   - View the logs to see any error messages

4. **Common issues**:
   - **Import errors**: Make sure all Python files are in the correct directories
   - **Missing dependencies**: Add them to `requirements.txt`
   - **Path issues**: The code uses relative paths which should work fine on Streamlit Cloud

### If you need to update your app:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
3. Streamlit Cloud will automatically redeploy your app!

## Environment Variables (Optional)

If you need to add API keys later:

1. In Streamlit Cloud dashboard, go to your app settings
2. Click "Secrets" tab
3. Add your API keys as secrets:
   ```
   LINKEDIN_API_KEY=your_key_here
   EMAIL_API_KEY=your_key_here
   FUNDING_API_KEY=your_key_here
   ```
4. Access them in your code with `st.secrets["LINKEDIN_API_KEY"]`

## Free Tier Limits

Streamlit Cloud free tier includes:
- ✅ Unlimited public apps
- ✅ Automatic deployments
- ✅ Custom domains
- ⚠️ Apps sleep after 7 days of inactivity (wake up on next visit)
- ⚠️ 1GB RAM limit

## Next Steps

After deployment:
1. Test all features of your app
2. Share the URL with EuPrime
3. Monitor usage and performance
4. Consider upgrading if you need more resources

## Support

- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-cloud
- Streamlit Community: https://discuss.streamlit.io/

