@echo off
echo 🚀 Preparing for Render deployment...
echo.

echo 📝 Initializing Git repository...
git init

echo 📦 Adding all files...
git add .

echo 💾 Creating initial commit...
git commit -m "Ready for Render deployment"

echo.
echo ✅ Git repository ready!
echo.
echo 📋 Next steps:
echo 1. Create a new repository on GitHub
echo 2. Copy the repository URL
echo 3. Run: git remote add origin YOUR_GITHUB_REPO_URL
echo 4. Run: git push -u origin main
echo 5. Go to render.com and connect your GitHub repo
echo.
echo 🌐 Your app will be live at: https://your-app-name.onrender.com
echo.
pause
