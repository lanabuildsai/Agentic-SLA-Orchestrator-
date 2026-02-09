# Contributing to Agentic SLA Orchestrator

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

---

## 🎯 Ways to Contribute

- **Report bugs** - Found an issue? Open a bug report
- **Suggest features** - Have an idea? Open a feature request
- **Improve documentation** - Fix typos, add examples, clarify explanations
- **Submit code** - Fix bugs, add features, optimize performance
- **Share feedback** - Let us know how you're using the project

---

## 🐛 Reporting Bugs

**Before submitting:**
1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Collect relevant information (Python version, error messages, etc.)

**Create a bug report with:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, dependencies)
- Error messages or logs
- Screenshots (if applicable)

---

## 💡 Suggesting Features

**Before suggesting:**
1. Check existing issues and discussions
2. Consider if it aligns with project goals (governance-first enterprise AI)

**Create a feature request with:**
- Clear, concise description
- Use case and motivation
- Proposed solution (if you have one)
- Alternatives considered
- Impact on existing functionality

---

## 🔧 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/agentic-sla-orchestrator.git
cd agentic-sla-orchestrator
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .  # Install in editable mode
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your OpenAI API key (if needed)
```

### 5. Run Tests

```bash
pytest tests/
```

---

## 📝 Code Contribution Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number-description
```

**Branch naming:**
- `feature/` for new features
- `bugfix/` for bug fixes
- `docs/` for documentation
- `refactor/` for code refactoring

### 2. Make Your Changes

- Write clear, readable code
- Follow existing code style (PEP 8 for Python)
- Add docstrings to functions/classes
- Update documentation if needed
- Add tests for new functionality

### 3. Test Your Changes

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_confidence_engine.py
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "Clear description of what changed and why"
```

**Commit message format:**
```
<type>: <short summary>

<optional detailed description>

Fixes #<issue-number>
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

**Examples:**
- `feat: add reinforcement learning from human feedback`
- `fix: correct confidence calculation for edge cases`
- `docs: update README with installation instructions`

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference to related issue (if any)
- Summary of changes
- Screenshots (if UI changes)
- Confirmation that tests pass

---

## 🎨 Code Style Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable names
- Maximum line length: 100 characters
- Use type hints where appropriate

**Format your code:**
```bash
# Auto-format with black
black src/ tests/

# Sort imports
isort src/ tests/

# Check style
flake8 src/ tests/
```

### Docstring Style

Use Google-style docstrings:

```python
def calculate_confidence(rule_urgency: float, llm_urgency: float) -> float:
    """
    Calculate hybrid confidence score combining rules and LLM signals.
    
    Args:
        rule_urgency: Urgency score from deterministic rules (0-1)
        llm_urgency: Urgency score from LLM classification (0-1)
    
    Returns:
        Final confidence score (0-1)
    
    Examples:
        >>> calculate_confidence(0.7, 0.85)
        0.76
    """
    return (0.6 * rule_urgency) + (0.4 * llm_urgency)
```

### Testing Guidelines

- Write tests for new features
- Maintain or improve code coverage
- Use descriptive test names
- Test edge cases and error conditions

```python
def test_confidence_calculation_basic():
    """Test basic confidence calculation with typical inputs."""
    result = calculate_confidence(rule_urgency=0.7, llm_urgency=0.8)
    assert 0.7 <= result <= 0.8
    
def test_confidence_calculation_edge_case():
    """Test confidence calculation with zero urgency."""
    result = calculate_confidence(rule_urgency=0.0, llm_urgency=0.0)
    assert result == 0.0
```

---

## 📚 Documentation Guidelines

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples for new features
- Keep documentation clear and concise
- Use diagrams where helpful

---

## 🔍 Review Process

1. **Automated Checks**
   - Code style validation
   - Test suite execution
   - Coverage reporting

2. **Manual Review**
   - Code quality and clarity
   - Test coverage
   - Documentation completeness
   - Alignment with project goals

3. **Feedback & Iteration**
   - Address review comments
   - Update as needed
   - Re-request review

4. **Merge**
   - Squash commits if needed
   - Merge into main branch
   - Delete feature branch

---

## 🌟 Areas for Contribution

### High Priority

- **Real-time event streaming** (Kafka/Redis integration)
- **Reinforcement learning** from human feedback
- **Multi-agent orchestration** patterns
- **Advanced testing** (integration tests, load tests)
- **Performance optimization** (caching, batching)

### Medium Priority

- **Vector database integration** for similar ticket search
- **Additional LLM providers** (Claude, Gemini, local models)
- **Dashboard enhancements** (real-time updates, filters)
- **API development** (REST/GraphQL endpoints)
- **Deployment guides** (Docker, Kubernetes)

### Documentation

- **Tutorial notebooks** for specific use cases
- **Video walkthroughs** of key features
- **Architecture decision records** (ADRs)
- **Performance benchmarks** and comparisons
- **Case studies** from real-world applications

---

## ❓ Questions?

- **General questions:** Open a [GitHub Discussion](https://github.com/YOUR_USERNAME/agentic-sla-orchestrator/discussions)
- **Bug reports:** Open an [Issue](https://github.com/YOUR_USERNAME/agentic-sla-orchestrator/issues)
- **Security issues:** Email lanab.career@gmail.com directly

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Your contributions help make this project better for everyone. We appreciate your time and effort!

---

**Happy coding! 🚀**
