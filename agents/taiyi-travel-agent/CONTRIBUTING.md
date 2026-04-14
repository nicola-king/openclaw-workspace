# Contributing to Taiyi Travel Pathfinder Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 How to Contribute

### 1. Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any error messages
- Your environment (Python version, OS, etc.)

### 2. Suggesting Features

Feature suggestions are welcome! Please include:

- A clear and descriptive title
- A detailed description of the feature
- Use cases and examples
- Any alternative solutions you've considered

### 3. Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Include screenshots and animated GIFs in your pull request whenever possible
- Follow the Python style guide
- Include documentation for new features
- Ensure all tests pass

## 📋 Development Setup

### 1. Fork the Repository

```bash
# Fork on GitHub, then clone
git clone https://github.com/your-username/taiyi-travel-agent.git
cd taiyi-travel-agent
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### 4. Run Tests

```bash
python3 -m pytest tests/
```

## 📝 Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions
- Keep functions small and focused
- Use meaningful variable names

## 🚀 Release Process

1. Update version number in `__init__.py`
2. Update `CHANGELOG.md` with changes
3. Create a pull request
4. After review and testing, merge to main
5. Create a GitHub release

## 📞 Contact

- **GitHub Issues**: https://github.com/nicola-king/taiyi-travel-agent/issues
- **Discussions**: https://github.com/nicola-king/taiyi-travel-agent/discussions

---

*Thank you for contributing to Taiyi Travel Pathfinder Agent!*
