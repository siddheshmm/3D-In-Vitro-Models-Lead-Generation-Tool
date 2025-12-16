# Adding Deployment Link to GitHub Repository

This guide explains where and how to add your Streamlit Cloud deployment link to your GitHub repository.

## Best Practices: Where to Add the Link

### 1. ✅ README.md (MOST IMPORTANT - Already Done!)

The deployment link has been added to the README.md file at the top. This is the **most visible** place and what most people will see first.

**Location**: Top of README.md, right after the title

### 2. ✅ Repository Description (RECOMMENDED)

Add the link to your repository description for maximum visibility:

**Steps:**
1. Go to your repository: https://github.com/siddheshmm/3D-In-Vitro-Models-Lead-Generation-Tool
2. Click the **gear icon** (⚙️) next to "About" section (or click "Edit" if you see it)
3. In the **Description** field, add:
   ```
   3D In-Vitro Models Lead Generation Tool - Live Demo: https://your-app-name.streamlit.app
   ```
4. Click **Save changes**

### 3. ✅ Repository Website URL (RECOMMENDED)

Add it as the official website:

**Steps:**
1. Go to your repository settings
2. Scroll to the "About" section
3. Check the box next to "Website"
4. Enter your Streamlit Cloud URL: `https://your-app-name.streamlit.app`
5. Click **Save changes**

### 4. ⚠️ Releases (OPTIONAL - Only if you create releases)

If you create GitHub releases:

**Steps:**
1. Go to your repository
2. Click "Releases" → "Create a new release"
3. Add the deployment link in the release notes:
   ```
   ## Live Demo
   Try the application: https://your-app-name.streamlit.app
   ```

### 5. ✅ Topics/Tags (OPTIONAL)

Add relevant topics to help people discover your repo:

**Steps:**
1. Go to your repository
2. Click the gear icon in the "About" section
3. In "Topics", add:
   - `streamlit`
   - `lead-generation`
   - `biotech`
   - `data-science`
   - `web-scraping`

## Quick Setup Checklist

After deploying to Streamlit Cloud:

- [ ] Update README.md with actual Streamlit Cloud URL (replace placeholder)
- [ ] Add link to repository description
- [ ] Add link as repository website URL
- [ ] (Optional) Create a release with the link
- [ ] (Optional) Add relevant topics/tags

## Example Repository Description

```
🔬 3D In-Vitro Models Lead Generation Tool | Identifies, enriches, and ranks high-probability leads for 3D in-vitro models | Live Demo: https://your-app-name.streamlit.app
```

## Visual Badge (Optional)

You can also add a Streamlit badge to your README. The code is already in the README.md:

```markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)
```

This creates a clickable badge that links to your app.

## Summary

**Priority Order:**
1. **README.md** - ✅ Already added
2. **Repository Description** - Add this manually
3. **Repository Website URL** - Add this manually
4. **Releases** - Only if you create releases
5. **Topics** - Optional but helpful

The README.md is the most important since it's what people see when they visit your repository!

