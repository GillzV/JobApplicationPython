# Contributing to Job Application Automation Bot

Thank you for your interest in contributing to the Job Application Automation Bot! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Provide detailed information about the bug
- Include steps to reproduce the issue
- Mention your operating system and Python version

### Suggesting Features
- Open a new issue with the "enhancement" label
- Describe the feature in detail
- Explain why this feature would be useful
- Consider implementation complexity

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- pip

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/job-application-bot.git
cd job-application-bot

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📝 Code Style Guidelines

### Python Code
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

### Example
```python
def parse_resume(file_path: str) -> Dict[str, Any]:
    """
    Parse resume from various file formats and extract structured information.
    
    Args:
        file_path: Path to the resume file
        
    Returns:
        Dictionary containing extracted resume information
        
    Raises:
        ValueError: If file format is not supported
    """
    # Implementation here
    pass
```

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Add more details in the body if needed

### Example
```
Add resume parsing functionality

- Support for PDF, DOCX, and TXT files
- Extract name, email, phone, skills, experience
- Add validation and error handling
- Include unit tests for parser functions
```

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=.
```

### Writing Tests
- Create test files in a `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Test both success and failure cases

### Example Test
```python
def test_parse_resume_pdf():
    """Test parsing a PDF resume file."""
    parser = ResumeParser()
    result = parser.parse_resume("sample_resume.pdf")
    
    assert result["name"] == "John Doe"
    assert result["email"] == "john.doe@email.com"
    assert "Python" in result["skills"]
```

## 📋 Pull Request Guidelines

### Before Submitting
- Ensure all tests pass
- Update documentation if needed
- Check that your code follows style guidelines
- Test the application manually

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No breaking changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No console errors
```

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 📞 Getting Help

If you need help with contributing:
- Check existing issues and pull requests
- Join our discussions in GitHub Discussions
- Contact maintainers through GitHub issues

## 🎯 Areas for Contribution

### High Priority
- Real web scraping implementation
- Browser automation with Selenium/Playwright
- Enhanced error handling and validation
- Performance optimizations

### Medium Priority
- Additional resume formats support
- More job search platforms
- Advanced analytics and reporting
- Export functionality improvements

### Low Priority
- UI/UX improvements
- Additional language support
- Documentation enhancements
- Code refactoring

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to make this project better! 🚀 