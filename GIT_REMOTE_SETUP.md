# Git Remote Setup

**Repository:** https://github.com/cogmanframework/cogman_runtime.git

---

## Setup Remote

```bash
# Check current remote
git remote -v

# Add or update remote
git remote add origin https://github.com/cogmanframework/cogman_runtime.git
# or if exists:
git remote set-url origin https://github.com/cogmanframework/cogman_runtime.git

# Verify
git remote -v
```

---

## First Push

```bash
# Check status
git status

# Add all files
git add .

# Commit
git commit -m "feat: Initial commit - Cogman Runtime v2.0"

# Push to remote
git push -u origin main
```

---

## Verify

```bash
# Check remote
git remote -v

# Should show:
# origin  https://github.com/cogmanframework/cogman_runtime.git (fetch)
# origin  https://github.com/cogmanframework/cogman_runtime.git (push)
```

---

**Note:** All documentation has been updated to use the new repository URL.

