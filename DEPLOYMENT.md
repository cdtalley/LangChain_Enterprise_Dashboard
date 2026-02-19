# 🚀 GitHub Pages Deployment Guide

This guide explains how the Next.js dashboard is deployed to GitHub Pages.

## 📋 Prerequisites

1. GitHub repository with GitHub Pages enabled
2. GitHub Actions enabled in repository settings
3. Repository name: `LangChain_Enterprise_Dashboard`

## ⚙️ Configuration

### Next.js Configuration

The `next.config.js` is configured to:
- Enable static export when `GITHUB_PAGES=true`
- Set `basePath` to `/LangChain_Enterprise_Dashboard` for GitHub Pages
- Disable image optimization for static export
- Configure asset prefix for proper asset loading

### Build Scripts

- `npm run build` - Standard Next.js build
- `npm run build:gh-pages` - Build for GitHub Pages (static export)
- `npm run export` - Alias for `build:gh-pages`

## 🔄 Automatic Deployment

The dashboard automatically deploys to GitHub Pages when:
- Code is pushed to the `main` branch
- Manual workflow dispatch is triggered

### Workflow: `.github/workflows/deploy-gh-pages.yml`

The workflow:
1. Checks out the code
2. Sets up Node.js 18
3. Installs dependencies
4. Builds the Next.js app for static export
5. Uploads the `out` directory as a Pages artifact
6. Deploys to GitHub Pages

## 🌐 Accessing the Dashboard

After deployment, the dashboard will be available at:
```
https://<your-username>.github.io/LangChain_Enterprise_Dashboard/
```

## 🔧 Manual Deployment

To deploy manually:

1. Enable GitHub Pages in repository settings:
   - Go to Settings → Pages
   - Source: GitHub Actions

2. Build locally (optional):
   ```bash
   npm run build:gh-pages
   ```

3. Push to main branch or trigger workflow manually:
   - Go to Actions tab
   - Select "Deploy Next.js Dashboard to GitHub Pages"
   - Click "Run workflow"

## 📝 Notes

- The app uses client-side routing, so all navigation works correctly
- All data is generated client-side (no backend required)
- Static export ensures fast loading times
- The `out` directory contains the static files (gitignored)

## 🐛 Troubleshooting

### Build fails
- Check Node.js version (should be 18+)
- Verify all dependencies are installed
- Check for TypeScript errors: `npm run type-check`

### Pages not loading
- Verify GitHub Pages is enabled in repository settings
- Check the Actions tab for deployment errors
- Ensure `basePath` matches your repository name

### Assets not loading
- Verify `assetPrefix` is set correctly in `next.config.js`
- Check browser console for 404 errors
- Ensure paths use the basePath prefix

## 🔄 Updating the Deployment

Simply push changes to the `main` branch - the workflow will automatically rebuild and redeploy.
