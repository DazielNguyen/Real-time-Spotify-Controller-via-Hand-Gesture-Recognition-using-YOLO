# Contributing to Real-time Spotify Controller

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful to all contributors
- Provide constructive feedback
- Help others in the community
- Report bugs responsibly

## Reporting Bugs

Before reporting a bug, please:

1. **Check** if the issue already exists
2. **Include** your system information (macOS version, Python version, etc.)
3. **Provide** step-by-step reproduction instructions
4. **Attach** error messages and logs
5. **Include** expected vs. actual behavior

### Bug Report Template

```markdown
## Description
Brief description of the bug

## System Information
- macOS version: 
- Python version: 
- YOLOv8 version: 
- OpenCV version: 

## Steps to Reproduce
1. 
2. 
3. 

## Expected Behavior

## Actual Behavior

## Error Messages / Logs

## Additional Context
```

## Feature Requests

We welcome feature requests! When submitting:

1. **Describe the use case** - Why is this feature needed?
2. **Provide examples** - How would users interact with it?
3. **Consider implementation** - Any technical thoughts on implementation?

## Development Setup

### Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/real-time-spotify-controller.git
cd real-time-spotify-controller

# Add upstream remote
git remote add upstream https://github.com/original-owner/real-time-spotify-controller.git
```

### Create Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .
pip install -r requirements.txt

# Install additional dev tools
pip install pytest black flake8 mypy
```

## Making Changes

### Branch Naming Convention

```bash
# Feature
git checkout -b feature/feature-name

# Bug fix
git checkout -b fix/bug-description

# Documentation
git checkout -b docs/documentation-update

# Performance improvement
git checkout -b perf/improvement-description
```

### Coding Standards

We follow PEP 8 with some additions:

```python
# Use type hints
def predict(image: np.ndarray) -> Dict[str, float]:
    """Predict gesture from image.
    
    Args:
        image: Input image array (H, W, 3)
        
    Returns:
        Dictionary with gesture predictions
    """
    pass

# Format with black
black src/

# Check style
flake8 src/

# Type checking
mypy src/
```

### Commit Messages

Follow conventional commit format:

```
type(scope): subject

body

footer
```

**Types**: feat, fix, docs, style, refactor, test, chore, perf

**Examples**:
```
feat(inference): add multi-hand detection support

fix(tracking): correct temporal stability calculation

docs(readme): improve installation instructions

perf(model): optimize preprocessing pipeline
```

## Pull Request Process

1. **Update** your local fork from upstream
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push** to your fork
   ```bash
   git push origin feature/your-feature
   ```

3. **Create** Pull Request on GitHub
   - Title: Clear, descriptive title
   - Description: Reference issues, explain changes
   - Screenshots: Include for UI changes

4. **PR Checklist**
   - [ ] Code follows PEP 8 style
   - [ ] Comments added for complex logic
   - [ ] Type hints included
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] No unrelated changes included

5. **Respond** to reviews promptly

## Testing

### Writing Tests

```python
# tests/test_hand_tracking.py
import pytest
from src.hand_tracking import GestureController

def test_gesture_detection():
    """Test basic gesture detection."""
    controller = GestureController()
    result = controller.detect_gesture(dummy_frame)
    assert result["gesture"] in ["fist", "palm", "peace", "one", "three", "four", "no_gesture"]

def test_cooldown_mechanism():
    """Test that cooldown prevents multiple triggers."""
    controller = GestureController(cooldown=2.0)
    # Rapid fire same gesture
    # Verify only first action executed
```

### Run Tests

```bash
pytest tests/
pytest tests/ -v  # Verbose
pytest tests/ --cov=src  # Coverage report
```

## Documentation

When adding features, update:

1. **README.md** - Usage and examples
2. **Docstrings** - Function documentation
3. **CHANGELOG.md** - What changed
4. **docs/report.md** - Technical details if applicable

**Docstring Format**:
```python
def function(param1: str, param2: int) -> bool:
    """Brief one-line description.
    
    Longer description explaining what this function does,
    any important behavior to note, and edge cases.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When X condition occurs
        TypeError: When Y condition occurs
        
    Example:
        >>> result = function("test", 42)
        >>> print(result)
        True
    """
    pass
```

## Release Process

Version numbering follows Semantic Versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking API changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in setup.py
- [ ] Tag created
- [ ] Release notes written

## Questions?

- **Create** an issue with "question" label
- **Join** discussions tab
- **Email** maintainers for private concerns

## Recognition

Contributors will be recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- GitHub contributors page
- Release notes

Thank you for contributing! 🎉

