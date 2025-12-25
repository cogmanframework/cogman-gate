# Git Setup Guide

**Purpose:** Complete guide for setting up Git with IP protection

---

## 🚀 Initial Repository Setup

### 1. Initialize Repository

```bash
# If starting fresh
git init
git branch -M main

# Or clone existing
git clone https://github.com/cogmanframework/cogman_runtime.git
cd cogman_runtime
```

### 2. Configure Git

```bash
# Set user info
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Set default editor
git config core.editor "nano"  # or "vim", "code --wait", etc.

# Set line ending handling
git config core.autocrlf input  # Linux/Mac
# git config core.autocrlf true  # Windows

# Enable pre-commit hook
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### 3. Verify .gitignore

```bash
# Check what will be ignored
git status --ignored

# Test .gitignore
git check-ignore -v kernel/build/
# Should output: kernel/build/ .gitignore:XX:kernel/build/
```

---

## 📤 First Push

### 1. Add Remote

```bash
# Add remote repository
git remote add origin https://github.com/cogmanframework/cogman_runtime.git

# Verify remote
git remote -v
```

### 2. Stage Files

```bash
# Add all files (respects .gitignore)
git add .

# Verify what will be committed
git status
```

### 3. Initial Commit

```bash
# Commit
git commit -m "feat: Initial commit - Cogman Energetic Engine v2.0"

# Verify commit
git log -1
```

### 4. Push to Remote

```bash
# Push main branch
git push -u origin main

# Verify on remote
git ls-remote origin
```

---

## 🔒 IP Protection Setup

### 1. Enable Pre-Commit Hook

```bash
# Copy sample hook
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit

# Make executable
chmod +x .git/hooks/pre-commit

# Test hook
git commit --allow-empty -m "test: Test pre-commit hook"
```

### 2. Configure Repository Settings

#### GitHub

1. Go to repository settings
2. **General:**
   - Repository name: `cogman_runtime`
   - Description: Add description
   - Visibility: **Private** (recommended for IP protection)

3. **Branches:**
   - Default branch: `main`
   - Branch protection: Enable for `main`
     - Require pull request reviews
     - Require status checks
     - Restrict who can push

4. **Secrets and variables:**
   - Add secrets for CI/CD
   - Never commit secrets to code

#### GitLab

1. Go to project settings
2. **General:**
   - Visibility: **Private** (recommended)
   - Default branch: `main`

3. **Repository:**
   - Protected branches: Protect `main`
   - Push rules: Configure as needed

4. **CI/CD:**
   - Variables: Add secrets
   - Never commit secrets

---

## 🛡️ Security Checklist

Before every push:

- [ ] `.gitignore` is working
- [ ] No API keys in code
- [ ] No secrets in code
- [ ] No large files (>10MB)
- [ ] No personal information
- [ ] Pre-commit hook enabled
- [ ] Tests pass

---

## 📋 Common Commands

### Daily Workflow

```bash
# Check status
git status

# Review changes
git diff

# Stage files
git add .

# Commit
git commit -m "feat: Description"

# Push
git push origin main
```

### Branch Management

```bash
# Create branch
git checkout -b feature/new-feature

# Switch branch
git checkout main

# List branches
git branch -a

# Delete branch
git branch -d feature/old-feature
```

### History

```bash
# View commit history
git log --oneline -10

# View file history
git log --follow -- path/to/file

# View changes
git diff HEAD~1
```

---

## 🔍 Verification

### Check What Will Be Committed

```bash
# See staged files
git diff --cached --name-only

# See all changes
git status

# See ignored files
git status --ignored
```

### Check for Secrets

```bash
# Search commit history
git log -p | grep -i "key\|secret\|password"

# Search current changes
git diff | grep -i "key\|secret\|password"
```

---

## 🚨 Troubleshooting

### Issue: Large File

```bash
# Remove from history (if not pushed)
git reset HEAD~1
# Add to .gitignore
# Commit again
```

### Issue: Accidental Secret Commit

```bash
# Remove from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (if private repo)
git push origin --force --all
```

### Issue: .gitignore Not Working

```bash
# Remove from cache
git rm -r --cached .
git add .
git commit -m "fix: Update .gitignore"
```

---

## 📚 Additional Resources

- **GIT_IP_PROTECTION.md:** IP protection guide
- **GIT_WORKFLOW.md:** Workflow guide
- **.gitignore:** Excluded files
- **LICENSE:** License terms

---

**Last Updated:** 2024-12-25

