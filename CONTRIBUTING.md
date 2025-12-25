# Contributing to Cogman Gate

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 🔒 IP Protection

### Important Notes

1. **Core Formulas are LOCKED**
   - CORE-1 to CORE-9 formulas are LOCKED
   - Do not modify core formulas without review
   - See `docs/COGMAN_CORE_KERNEL.md`

2. **Source Code is IP**
   - All contributions become part of the project
   - MIT License applies to contributions
   - See `LICENSE` file

3. **No Sensitive Information**
   - Do not commit API keys or secrets
   - Do not commit personal information
   - Use environment variables for secrets

---

## 🚀 Getting Started

### 1. Fork the Repository

```bash
# Fork on GitHub/GitLab
# Then clone your fork
git clone https://github.com/cogmanframework/cogman_gate.git
cd cogman_gate
```

### 2. Set Up Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Build C++ kernel
cd kernel
mkdir build && cd build
cmake ..
make
cd ../..
```

### 3. Create a Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bugfix branch
git checkout -b bugfix/issue-number
```

---

## 📝 Making Changes

### Code Style

- **Python:** Follow PEP 8
- **C++:** Follow project style (see `kernel/README.md`)
- **Documentation:** Use Markdown

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
test: Add tests
refactor: Refactor code
chore: Maintenance tasks
```

### Testing

```bash
# Run tests before committing
python3 tests/run_tests.py

# Run C++ tests
cd kernel/build
./test_core_formulas
```

---

## 🔍 Pre-Commit Checklist

Before committing:

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No sensitive information
- [ ] No large files
- [ ] `.gitignore` respected

---

## 📤 Submitting Changes

### 1. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 2. Create Pull Request

- Go to GitHub/GitLab
- Create pull request
- Fill out PR template
- Request review

### 3. Address Review Comments

- Make requested changes
- Update PR
- Respond to comments

---

## 📋 Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tests pass
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No sensitive information
- [ ] Tests added/updated
```

---

## 🔒 IP Protection Agreement

By contributing, you agree:

1. **License:** Your contributions are licensed under MIT License
2. **IP Ownership:** All contributions become part of the project
3. **No Secrets:** You will not commit sensitive information
4. **Code Review:** All contributions require review

---

## 📞 Questions?

- **Documentation:** Check `docs/` directory
- **Issues:** Open GitHub issue
- **Discussions:** Use GitHub Discussions

---

**Thank you for contributing!**

