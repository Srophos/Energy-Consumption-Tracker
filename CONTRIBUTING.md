# Contributing to Energy Tracker

Thank you for considering contributing to Energy Tracker! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/energy-tracker.git
   cd energy-tracker
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black isort flake8
   ```

## Development Workflow

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Urgent production fixes
- `docs/description` - Documentation updates

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Run tests** to ensure nothing breaks:
   ```bash
   pytest tests/ -v
   ```

4. **Format your code**:
   ```bash
   black app/ tests/ run.py
   isort app/ tests/ run.py
   flake8 app/ tests/ run.py --max-line-length=100
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request** on GitHub

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guide
- Maximum line length: 100 characters
- Use Black for code formatting
- Use isort for import sorting
- Use type hints where appropriate

### Testing Requirements

- Write tests for all new features
- Maintain minimum 80% code coverage
- All tests must pass before PR approval
- Include unit, integration, and system tests as needed

### Documentation

- Update README.md for significant changes
- Add docstrings to all functions and classes
- Update API documentation if routes change
- Include comments for complex logic

## Pull Request Process

1. **Ensure all tests pass** locally before submitting
2. **Update documentation** as needed
3. **Provide a clear PR description** explaining:
   - What changes were made
   - Why these changes are necessary
   - Any breaking changes
4. **Link related issues** in the PR description
5. **Wait for CI/CD pipeline** to complete successfully
6. **Address review comments** promptly
7. **Squash commits** if requested before merging

## Testing Guidelines

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_routes.py -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# Watch for changes
pytest-watch
```

### Writing Tests

```python
import unittest
from app import create_app

class MyTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
    
    def test_something(self):
        """Test description."""
        # Arrange
        # Act
        # Assert
        pass
```

## Security

- Never commit sensitive data (passwords, API keys, etc.)
- Use environment variables for configuration
- Report security vulnerabilities privately to maintainers
- Follow security best practices in code

## Questions?

If you have questions or need help:
- Open an issue with the "question" label
- Check existing issues and documentation
- Reach out to maintainers

Thank you for contributing! 🎉
