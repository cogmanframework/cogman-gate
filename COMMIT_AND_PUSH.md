# Commit and Push to GitHub

**Repository:** https://github.com/cogmanframework/cogman_runtime.git

---

## Quick Commands

```bash
# 1. ไปที่ project directory
cd /Users/tiewphopum/Developments/@git/@developments/RESEARCH/cogman_enegetic_engine

# 2. ตรวจสอบ branch
git branch
# ถ้ายังไม่อยู่ใน main:
git checkout main

# 3. Stage ไฟล์ทั้งหมด
git add .

# 4. Commit
git commit -m "feat: Initial commit - Cogman Runtime v2.0

- GitHub + Binary-First distribution strategy
- Installer script (install.sh)
- Complete documentation
- IP protection strategy
- All repository URLs updated to cogmanframework/cogman_runtime
- Removed PyPI-related files (strategic decision)"

# 5. Push ไปยัง GitHub
git push -u origin main
```

---

## Verification

```bash
# ตรวจสอบ remote
git remote -v

# ตรวจสอบ status
git status

# ตรวจสอบ commit
git log --oneline -1
```

---

## Expected Output

### After `git add .`
```
# Should show many files staged (A = Added)
```

### After `git commit`
```
[main abc1234] feat: Initial commit - Cogman Runtime v2.0
 313 files changed, ...
```

### After `git push`
```
Enumerating objects: ...
Counting objects: ...
Writing objects: ...
To https://github.com/cogmanframework/cogman_runtime.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Troubleshooting

### "fatal: Unable to create index.lock"
```bash
# Remove lock file
rm -f .git/index.lock
# Then try again
```

### "error setting certificate verify locations"
```bash
# This is a sandbox issue, should work in your terminal
# Or configure git SSL:
git config --global http.sslCAInfo /etc/ssl/certs/ca-certificates.crt
```

### "Permission denied"
```bash
# Make sure you have write access to .git directory
# Or run with proper permissions
```

---

## Verify on GitHub

After push, check:
1. https://github.com/cogmanframework/cogman_runtime
2. Files should be visible
3. README.md should display correctly

---

**Ready to execute!**

