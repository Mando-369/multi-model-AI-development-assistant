# Contributing to Multi-Model AI Development Assistant

Thank you for your interest in contributing to our project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/multi-model-AI-development-assistant.git
cd multi-model-AI-development-assistant
git remote add upstream https://github.com/Mando-369/multi-model-AI-development-assistant.git
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Development Guidelines

### Code Style

- **Python**: Follow PEP 8, use Black formatter
- **Type Hints**: Use type hints for function signatures
- **Docstrings**: Use Google-style docstrings

Example:
```python
def process_audio_buffer(
    buffer: np.ndarray, 
    sample_rate: int = 44100
) -> np.ndarray:
    """Process an audio buffer with effects.
    
    Args:
        buffer: Audio samples as numpy array
        sample_rate: Sample rate in Hz
        
    Returns:
        Processed audio buffer
        
    Raises:
        ValueError: If buffer is empty
    """
    if len(buffer) == 0:
        raise ValueError("Buffer cannot be empty")
    # Processing logic here
    return processed_buffer
```

### Testing

Write tests for new features:
```python
# tests/test_your_feature.py
import pytest
from your_module import your_function

def test_your_function():
    result = your_function(input_data)
    assert result == expected_output

def test_your_function_error():
    with pytest.raises(ValueError):
        your_function(invalid_input)
```

Run tests:
```bash
pytest tests/
pytest tests/ --cov=.  # With coverage
```

### Commit Messages

Follow the conventional commits format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
```
feat(routing): add intelligent auto-routing based on task complexity
fix(hrm): resolve MPS acceleration issue on M4 Max
docs(readme): update installation instructions for macOS
```

## 🎯 Areas for Contribution

### High Priority

1. **Model Integration**
   - Add support for new local models
   - Optimize model loading and caching
   - Implement model fine-tuning pipelines

2. **FAUST/JUCE Features**
   - Expand FAUST code generation templates
   - Add JUCE component generators
   - Create audio effect presets

3. **Performance Optimization**
   - Improve MPS acceleration
   - Optimize ChromaDB queries
   - Reduce model switching latency

### Good First Issues

- Add more syntax highlighting languages
- Improve error messages
- Add example projects
- Enhance documentation
- Write unit tests

## 🔄 Pull Request Process

### 1. Before Submitting

- [ ] Update documentation if needed
- [ ] Add/update tests
- [ ] Run the test suite
- [ ] Update CHANGELOG.md
- [ ] Ensure code follows style guidelines

### 2. PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### 3. Review Process

1. Submit PR against `main` branch
2. Automated tests will run
3. Wait for code review
4. Address feedback
5. PR will be merged once approved

## 🐛 Reporting Issues

### Bug Reports

Include:
- System information (OS, Python version, hardware)
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs
- Screenshots if applicable

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Additional context

## 📚 Documentation

### Adding Documentation

1. **Code Documentation**: Use docstrings
2. **User Guides**: Add to `docs/user_guide.md`
3. **API Docs**: Update `docs/api_reference.md`
4. **Examples**: Add to `examples/` directory

### Documentation Style

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep formatting consistent

## 🏗️ Architecture Decisions

For significant changes, create an Architecture Decision Record (ADR):

```markdown
# ADR-001: Title

## Status
Proposed/Accepted/Deprecated

## Context
Why this decision is needed

## Decision
What we're doing

## Consequences
Positive and negative outcomes
```

## 🔧 Development Tools

### Recommended VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "ms-toolsai.jupyter",
    "streetsidesoftware.code-spell-checker"
  ]
}
```

### Useful Commands

```bash
# Format code
black .
isort .

# Lint code
pylint src/
flake8 .

# Type checking
mypy src/

# Run specific test
pytest tests/test_module.py::TestClass::test_method

# Profile performance
python -m cProfile -o profile.prof main.py
```

## 📮 Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Multi-Model AI Development Assistant!