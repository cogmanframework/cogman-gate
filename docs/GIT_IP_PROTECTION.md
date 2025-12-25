# Git IP Protection Guide

**Purpose:** Guide for protecting Intellectual Property when using Git

---

## 🔒 IP Protection Strategy

### Core Principles

1. **Source Code is IP**
   - C++ kernel source code contains core formulas (CORE-1 to CORE-9)
   - Python implementation contains architecture
   - Both are valuable IP

2. **What to Protect**
   - ✅ Source code (already in repo)
   - ✅ Architecture and design
   - ✅ Core formulas (LOCKED)
   - ❌ Build artifacts (excluded)
   - ❌ Test data (excluded)
   - ❌ Secrets/keys (excluded)

3. **What NOT to Commit**
   - ❌ Compiled binaries
   - ❌ API keys / secrets
   - ❌ Personal notes
   - ❌ Test data with real scenarios
   - ❌ Build artifacts

---

## 📋 Pre-Commit Checklist

Before committing, verify:

- [ ] No API keys or secrets in code
- [ ] No hardcoded credentials
- [ ] No personal notes or TODOs with sensitive info
- [ ] No compiled binaries
- [ ] No test data with real scenarios
- [ ] `.gitignore` is up to date
- [ ] No large files (>100MB)

---

## 🛡️ Protection Measures

### 1. .gitignore Configuration

Ensure `.gitignore` excludes:
- Build artifacts (`kernel/build/`, `*.so`, `*.dylib`, `*.dll`)
- Python cache (`__pycache__/`, `*.pyc`)
- Logs and runtime data
- Configuration files with secrets
- IDE files

### 2. License Protection

- ✅ MIT License (permissive)
- ✅ Copyright notice in files
- ✅ License file in repo
- ⚠️ Consider adding license headers to source files

### 3. Repository Settings

#### GitHub/GitLab Settings

1. **Repository Visibility**
   - Private: Only authorized users
   - Public: Anyone can see (use with caution)

2. **Branch Protection**
   - Protect `main` branch
   - Require pull request reviews
   - Require status checks

3. **Secrets Management**
   - Use GitHub Secrets / GitLab CI/CD variables
   - Never commit secrets to code

### 4. Commit Message Guidelines

**DO:**
- Use clear, descriptive messages
- Reference issues/tickets
- Follow conventional commits

**DON'T:**
- Include sensitive information
- Include API keys
- Include personal notes

---

## 🔐 Sensitive Information

### Never Commit

1. **API Keys / Secrets**
   ```
   # BAD
   API_KEY = "sk-1234567890abcdef"
   
   # GOOD
   API_KEY = os.getenv("COGMAN_API_KEY")
   ```

2. **Credentials**
   ```
   # BAD
   password = "mypassword123"
   
   # GOOD
   password = os.getenv("COGMAN_PASSWORD")
   ```

3. **Personal Information**
   - Email addresses
   - Phone numbers
   - Personal notes

4. **Test Data with Real Scenarios**
   - Real user data
   - Production-like data
   - Sensitive test cases

---

## 📝 File Headers for IP Protection

### C++ Source Files

```cpp
/**
 * Cogman Kernel - Core Formulas
 * 
 * Copyright (c) 2024 Cogman Energetic Engine
 * 
 * This file contains proprietary formulas (CORE-1 to CORE-9).
 * Unauthorized copying, modification, or distribution is prohibited.
 * 
 * Licensed under MIT License - see LICENSE file for details.
 */
```

### Python Source Files

```python
"""
Cogman Energetic Engine - [Module Name]

Copyright (c) 2024 Cogman Energetic Engine

This file contains proprietary implementation.
Unauthorized copying, modification, or distribution is prohibited.

Licensed under MIT License - see LICENSE file for details.
"""
```

---

## 🚀 Git Workflow for IP Protection

### 1. Pre-Commit Hook (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook to check for sensitive information

# Check for API keys
if git diff --cached | grep -E "(api[_-]?key|secret|password|token)\s*=\s*['\"][^'\"]+['\"]"; then
    echo "ERROR: Potential API key or secret detected!"
    echo "Please use environment variables instead."
    exit 1
fi

# Check for large files
git diff --cached --name-only | while read file; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        if [ "$size" -gt 104857600 ]; then  # 100MB
            echo "ERROR: File $file is larger than 100MB"
            exit 1
        fi
    fi
done

exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### 2. Commit Workflow

```bash
# 1. Check status
git status

# 2. Review changes
git diff

# 3. Add files (respects .gitignore)
git add .

# 4. Verify no sensitive info
git diff --cached | grep -i "key\|secret\|password"

# 5. Commit
git commit -m "feat: Add new feature"

# 6. Push
git push origin main
```

---

## 🔍 Security Audit

### Before Public Release

1. **Scan for Secrets**
   ```bash
   # Use tools like git-secrets or truffleHog
   git-secrets --scan
   ```

2. **Check .gitignore**
   ```bash
   # Verify .gitignore is working
   git status --ignored
   ```

3. **Review Commit History**
   ```bash
   # Check for accidentally committed secrets
   git log --all --full-history --source -- "*secret*"
   git log --all --full-history --source -- "*key*"
   ```

4. **Check Large Files**
   ```bash
   # Find large files
   find . -type f -size +1M | grep -v ".git"
   ```

---

## 📚 Best Practices

### 1. Use Environment Variables

```python
# BAD
API_KEY = "sk-1234567890"

# GOOD
import os
API_KEY = os.getenv("COGMAN_API_KEY")
if not API_KEY:
    raise ValueError("COGMAN_API_KEY environment variable not set")
```

### 2. Use Config Files (Not in Git)

```yaml
# config/secrets.yaml (in .gitignore)
api_key: ${COGMAN_API_KEY}
database_url: ${DATABASE_URL}
```

### 3. Use .env Files (Not in Git)

```bash
# .env (in .gitignore)
COGMAN_API_KEY=sk-1234567890
DATABASE_URL=postgresql://...
```

### 4. Document Required Environment Variables

Create `.env.example`:

```bash
# .env.example (committed to git)
COGMAN_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@host:port/db
```

---

## 🚨 If Secrets Are Committed

### Immediate Actions

1. **Remove from History**
   ```bash
   # Use git-filter-branch or BFG Repo-Cleaner
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/secret/file" \
     --prune-empty --tag-name-filter cat -- --all
   ```

2. **Rotate Secrets**
   - Change all exposed API keys
   - Change passwords
   - Regenerate tokens

3. **Force Push** (if private repo)
   ```bash
   git push origin --force --all
   ```

4. **Notify Team**
   - Inform team members
   - Update documentation

---

## 📋 Repository Structure for IP Protection

```
cogman_runtime/
├── .gitignore              # ✅ Committed (protects IP)
├── LICENSE                 # ✅ Committed (IP license)
├── README.md               # ✅ Committed (public info)
│
├── kernel/                  # ✅ Committed (source code)
│   ├── src/                # ✅ Committed (IP - formulas)
│   ├── include/            # ✅ Committed (IP - headers)
│   └── build/              # ❌ NOT committed (.gitignore)
│
├── config/                 # ⚠️ Partially committed
│   ├── gate_profiles.yaml  # ✅ Committed (template)
│   └── secrets.yaml        # ❌ NOT committed (.gitignore)
│
└── storage/                # ❌ NOT committed (.gitignore)
    └── *.json              # ❌ Runtime data
```

---

## 🔗 Related Documentation

- **LICENSE:** MIT License terms
- **README.md:** Public information
- **README_DEV.md:** Developer guide
- **.gitignore:** Excluded files

---

## ⚠️ Important Notes

1. **Source Code is IP**
   - Core formulas (CORE-1 to CORE-9) are LOCKED
   - Implementation is proprietary
   - Architecture is valuable

2. **Public vs Private**
   - **Public repo:** Anyone can see code
   - **Private repo:** Only authorized users
   - Choose based on IP strategy

3. **License Choice**
   - **MIT:** Permissive, allows commercial use
   - **GPL:** Copyleft, requires open source
   - **Proprietary:** No public license

4. **Contributions**
   - Contributor License Agreement (CLA) may be needed
   - Ensure contributors understand IP ownership

---

## 📞 Support

If you have questions about IP protection:
- Review LICENSE file
- Consult legal counsel
- Check repository settings

---

**Last Updated:** 2024-12-25

