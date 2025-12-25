# Fix Secret in Git History

## Problem

GitHub Push Protection detected an OpenAI API key in commit `b78b035accc40f86b1df652fa29375dcdab7d7a4`:
- **File:** `RESEARCH/@poc_core_series/cogman_cfi/cogman_cfi_13_alpha/examples/gpt_fusion_demo.py:90`
- **Secret:** Hardcoded OpenAI API key

## Solution Options

### Option 1: Use GitHub's Allow URL (Quick Fix)

GitHub provided this URL to allow the secret:
```
https://github.com/cogmanframework/cogman_runtime/security/secret-scanning/unblock-secret/37JoH8v4N9YaiNPRhUIssIM30dz
```

**⚠️ Warning:** This allows the secret to remain in history. **Not recommended for production.**

---

### Option 2: Remove Secret from History (Recommended)

Use `git filter-repo` to remove the secret from all commits:

```bash
# Install git-filter-repo (if not installed)
pip install git-filter-repo

# Navigate to repository root
cd /Users/tiewphopum/Developments/@git/@developments

# Backup first!
git clone --mirror . ../cogman_backup

# Remove secret from all commits
git filter-repo --path RESEARCH/@poc_core_series/cogman_cfi/cogman_cfi_13_alpha/examples/gpt_fusion_demo.py \
  --invert-paths \
  --force

# Or replace the secret in the file across all commits
git filter-repo --path RESEARCH/@poc_core_series/cogman_cfi/cogman_cfi_13_alpha/examples/gpt_fusion_demo.py \
  --replace-text <(echo "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==>REMOVED_SECRET") \
  --force
```

**Better approach - Replace with environment variable:**

```bash
# Create replacement file
cat > /tmp/replace_secret.txt << 'EOF'
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==>os.getenv("OPENAI_API_KEY")
EOF

# Apply replacement
git filter-repo \
  --replace-text /tmp/replace_secret.txt \
  --force
```

---

### Option 3: Use BFG Repo-Cleaner (Alternative)

```bash
# Download BFG (if not installed)
# https://rtyley.github.io/bfg-repo-cleaner/

# Create replacement file
echo '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==>REMOVED' > /tmp/secret.txt

# Clean repository
java -jar bfg.jar --replace-text /tmp/secret.txt

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

---

## After Fixing History

1. **Force push** (⚠️ This rewrites history):
   ```bash
   git push origin main --force
   ```

2. **Notify collaborators** - They need to re-clone or reset their local repositories.

3. **Rotate the API key** - The exposed key should be considered compromised and rotated immediately.

---

## Current Status

✅ **Fixed in current commit:** Secret removed from `gpt_fusion_demo.py`  
❌ **Still in history:** Commit `b78b035` contains the secret  
⚠️ **Action required:** Remove secret from history or use GitHub's allow URL

---

## Recommendation

**Use Option 2 (git filter-repo)** to completely remove the secret from history. This is the safest approach for production repositories.

