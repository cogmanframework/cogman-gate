# Verify Git Remote URL

**Expected URL:** https://github.com/cogmanframework/cogman_runtime.git

---

## Quick Check

```bash
# Method 1: Show all remotes
git remote -v

# Expected output:
# origin  https://github.com/cogmanframework/cogman_runtime.git (fetch)
# origin  https://github.com/cogmanframework/cogman_runtime.git (push)
```

---

## Detailed Verification

### 1. Check Remote URL

```bash
# Get origin URL
git remote get-url origin

# Or
git config --get remote.origin.url

# Should output:
# https://github.com/cogmanframework/cogman_runtime.git
```

### 2. Test Connection

```bash
# Test if remote is accessible
git ls-remote --heads origin

# Should show branches (main, etc.)
```

### 3. Verify Repository Exists

```bash
# Check if repository exists (requires network)
curl -I https://github.com/cogmanframework/cogman_runtime

# Should return HTTP 200 or 301
```

---

## Common Issues

### Issue: "remote origin already exists" with wrong URL

**Fix:**
```bash
# Update existing remote
git remote set-url origin https://github.com/cogmanframework/cogman_runtime.git

# Verify
git remote -v
```

### Issue: "Repository not found"

**Check:**
1. Repository exists at https://github.com/cogmanframework/cogman_runtime
2. You have access (if private)
3. URL is correct (no typos)

### Issue: "Permission denied"

**Fix:**
- Use HTTPS with token, or
- Set up SSH keys

---

## Verification Checklist

- [ ] `git remote -v` shows correct URL
- [ ] `git remote get-url origin` matches expected
- [ ] `git ls-remote origin` works (if network available)
- [ ] Repository exists on GitHub

---

## Expected Values

| Check | Expected Value |
|-------|----------------|
| Remote name | `origin` |
| Fetch URL | `https://github.com/cogmanframework/cogman_runtime.git` |
| Push URL | `https://github.com/cogmanframework/cogman_runtime.git` |

---

**Last Updated:** 2024-12-25

