# Step-by-Step Guide: Commit Local Work and Push to Work GitHub (Windows)

## Prerequisites
- Your work GitHub repository URL (e.g., `https://github.com/your-work-org/repo-name.git`)
- Git installed and configured with your work credentials
- Access permissions to the work repository
- Open Command Prompt, PowerShell, or Git Bash in VS Code terminal

## Step 1: Commit Current Local Changes

### 1.1 Check Current Status
```cmd
git status
```

### 1.2 Stage All Changes
```cmd
# Stage all modified and new files
git add .

# Or stage specific files if needed
git add specific-file.py
```

### 1.3 Commit Changes
```cmd
git commit -m "Initial commit of Databricks DAB Azure project

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Step 2: Configure Work GitHub Remote

### 2.1 Remove Current Remote (if exists)
```cmd
git remote remove origin
```

### 2.2 Add Work GitHub as Origin
```cmd
git remote add origin https://github.com/YOUR-WORK-ORG/YOUR-REPO-NAME.git
```

### 2.3 Verify Remote Configuration
```cmd
git remote -v
```

## Step 3: Push to Work Repository

### 3.1 Push to Work Repository
```cmd
# For first push with upstream tracking
git push -u origin main

# Or if your branch is named 'master'
git push -u origin master
```

### 3.2 Verify Success
- Check the work GitHub repository in your browser
- Confirm all files and commit history are present

## Troubleshooting

### If Authentication Fails:
- Ensure you're using work credentials
- May need to configure Git with work email:
  ```cmd
  git config user.email "your-work-email@company.com"
  git config user.name "Your Name"
  ```

### If Push is Rejected:
- The remote repository may not be empty
- Use force push (ONLY if you're sure): `git push -f origin main`

This will preserve your local work and move it cleanly to your work GitHub repository for sharing with others.