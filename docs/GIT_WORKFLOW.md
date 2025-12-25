# Git Workflow for IP Protection

**Purpose:** Step-by-step guide for safe Git operations

---

## 🚀 Initial Setup

### 1. Configure Git

```bash
# Set user info (use work email, not personal)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Set default branch name
git config init.defaultBranch main

# Enable pre-commit hook (optional)
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### 2. Verify .gitignore

```bash
# Check what will be ignored
git status --ignored

# Verify .gitignore is working
git check-ignore -v kernel/build/
```

---

## 📝 Daily Workflow

### Before Making Changes

```bash
# 1. Pull latest changes
git pull origin main

# 2. Check status
git status

# 3. Review what will be committed
git diff
```

### Making Changes

```bash
# 1. Make your changes
# ... edit files ...

# 2. Review changes
git diff

# 3. Stage files (respects .gitignore)
git add .

# 4. Verify staged changes
git diff --cached

# 5. Check for sensitive info
git diff --cached | grep -i "key\|secret\|password"
```

### Committing

```bash
# 1. Commit with descriptive message
git commit -m "feat: Add new feature"

# 2. Verify commit
git log -1

# 3. Push to remote
git push origin main
```

---

## 🔒 IP Protection Checklist

Before every commit:

- [ ] No API keys or secrets in code
- [ ] No hardcoded credentials
- [ ] No personal information
- [ ] No large files (>10MB)
- [ ] `.gitignore` is working
- [ ] Build artifacts are excluded
- [ ] Test data is excluded

---

## 🛡️ Branch Strategy

### Recommended Branches

```
main          # Production-ready code (protected)
develop       # Development branch
feature/*     # Feature branches
bugfix/*      # Bug fix branches
release/*     # Release branches
```

### Branch Protection

```bash
# Protect main branch (on GitHub/GitLab)
# - Require pull request reviews
# - Require status checks
# - Require up-to-date branches
# - Restrict who can push
```

---

## 📤 Pushing to Remote

### First Time Setup

```bash
# 1. Add remote
git remote add origin https://github.com/cogmanframework/cogman_runtime.git

# 2. Verify remote
git remote -v

# 3. Push main branch
git push -u origin main
```

### Regular Push

```bash
# 1. Pull latest changes
git pull origin main

# 2. Resolve conflicts if any
# ... resolve conflicts ...

# 3. Push changes
git push origin main
```

### Push with Tags

```bash
# Tag a release
git tag -a v2.0.0 -m "Release version 2.0.0"

# Push tags
git push origin --tags
```

---

## 🔍 Security Checks

### Before Push

```bash
# 1. Check for secrets
git log -p | grep -i "key\|secret\|password"

# 2. Check file sizes
find . -type f -size +1M | grep -v ".git"

# 3. Review commit history
git log --oneline -10
```

### After Push

```bash
# 1. Verify on remote
git ls-remote origin

# 2. Check what's on remote
git fetch origin
git log origin/main --oneline -10
```

---

## 🚨 Emergency Procedures

### If Secrets Are Committed

1. **Immediately:**
   ```bash
   # Rotate all exposed secrets
   # Change API keys
   # Change passwords
   ```

2. **Remove from History:**
   ```bash
   # Use git-filter-branch or BFG
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/file" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force Push (if private repo):**
   ```bash
   git push origin --force --all
   ```

4. **Notify Team:**
   - Inform all team members
   - Update documentation

---

## 📋 Repository Settings

### GitHub Settings

1. **General**
   - Repository name: `cogman_runtime`
   - Description: Add description
   - Visibility: Private (recommended) or Public

2. **Branches**
   - Default branch: `main`
   - Branch protection: Enable for `main`

3. **Secrets and variables**
   - Add secrets for CI/CD
   - Never commit secrets

### GitLab Settings

1. **General**
   - Visibility: Private (recommended) or Public
   - Default branch: `main`

2. **Repository**
   - Protected branches: Protect `main`
   - Push rules: Configure as needed

3. **CI/CD**
   - Variables: Add secrets
   - Never commit secrets

---

## 🔗 Related Documentation

- **GIT_IP_PROTECTION.md:** IP protection guide
- **.gitignore:** Excluded files
- **LICENSE:** License terms

---

**Last Updated:** 2024-12-25

