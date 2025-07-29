# Developer Guide

This guide provides comprehensive information for developers working on the Decipher Bench project.

## Project Structure

```
decipher-bench/
├── src/                    # Main source code
│   ├── __init__.py        # Package initialization
│   ├── main.py            # Entry point (currently empty)
│   ├── benchmark.py       # Core benchmarking logic
│   ├── evaluators/        # Evaluation modules
│   └── utils/             # Utility functions
├── tests/                 # Test suite (organized by categories)
│   ├── knowledge/         # Knowledge & reasoning tests
│   ├── generation/        # Content generation tests
│   ├── safety/           # Safety & ethics tests
│   └── performance/      # Performance metric tests
├── docs/                 # Documentation
├── CLAUDE.md            # AI assistant instructions
├── README.md            # Project overview
├── LICENSE              # MIT license
└── clean_up.sh          # Code formatting script
```

## Development Environment Setup

### Prerequisites

- Python 3.12+
- Git
- Virtual environment tool (venv, conda, etc.)

### Initial Setup

1. **Clone and navigate to the repository:**
   ```bash
   git clone https://github.com/yourusername/decipher-bench.git
   cd decipher-bench
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode:**
   ```bash
   pip install -e .[dev]
   ```

## Code Quality and Standards

### Formatting and Linting

We use `ruff` for both linting and formatting. All code must pass ruff checks before commit.

**Primary method (recommended):**
```bash
bash clean_up.sh .
```

**Manual ruff commands:**
```bash
ruff check .          # Check for issues
ruff format .         # Format code
ruff check . --fix    # Auto-fix issues
```

### Code Style Guidelines

- Follow PEP 8 conventions
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Maximum line length: 88 characters (ruff default)
- Use meaningful variable and function names

### Pre-commit Hooks

Install pre-commit hooks to ensure code quality:
```bash
pre-commit install
pre-commit run --all-files  # Run on all files initially
```

## Testing

### Test Structure

Tests are organized by evaluation categories:

- `tests/knowledge/` - Factual accuracy, reasoning, common sense
- `tests/generation/` - Creative writing, structured output, code generation
- `tests/safety/` - Bias detection, toxicity filtering, alignment
- `tests/performance/` - Latency and consistency measurement

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_evaluation.py

# Run tests in specific directory
pytest tests/knowledge/

# Run tests with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_factual"
```

### Writing Tests

Follow these conventions when writing tests:

1. **Test file naming:** `test_*.py`
2. **Test function naming:** `test_*`
3. **Use descriptive test names:** `test_factual_accuracy_with_valid_input`
4. **Group related tests in classes:** `TestFactualEvaluation`
5. **Use fixtures for common setup:** Define in `conftest.py`

Example test structure:
```python
import pytest
from decipher_bench import LLMBenchmark

class TestFactualEvaluation:
    @pytest.fixture
    def benchmark(self):
        return LLMBenchmark(api_key="test-key")
    
    def test_exact_match_evaluation(self, benchmark):
        # Test implementation
        pass
```

## Development Workflow

### Branch Management

1. **Main branch:** `main` - production-ready code
2. **Feature branches:** `feature/feature-name` - new features
3. **Bug fixes:** `fix/bug-description` - bug fixes
4. **Documentation:** `docs/update-description` - documentation updates

### Commit Convention

Follow conventional commit format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(evaluation): add semantic similarity evaluator
fix(benchmark): handle API timeout errors correctly
docs(readme): update installation instructions
```

### Pull Request Process

1. **Create feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make changes and commit:**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

3. **Ensure code quality:**
   ```bash
   bash clean_up.sh .
   pytest
   ```

4. **Push and create PR:**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **PR Requirements:**
   - All tests pass
   - Code passes ruff checks
   - Test coverage remains above 80%
   - Clear description of changes
   - Reference related issues

## Package Architecture

### Core Components

1. **LLMBenchmark:** Main benchmarking class
2. **Evaluators:** Modules for different evaluation types
3. **Test Loader:** Loads and parses test definitions
4. **Report Generator:** Creates HTML/JSON reports
5. **CLI Interface:** Command-line tool

### Adding New Evaluators

1. **Create evaluator module:**
   ```python
   # src/evaluators/my_evaluator.py
   from .base import BaseEvaluator
   
   class MyEvaluator(BaseEvaluator):
       def evaluate(self, response, expected):
           # Implementation
           pass
   ```

2. **Register evaluator:**
   ```python
   # src/evaluators/__init__.py
   from .my_evaluator import MyEvaluator
   
   EVALUATORS = {
       'my_eval': MyEvaluator,
       # other evaluators...
   }
   ```

3. **Add tests:**
   ```python
   # tests/test_my_evaluator.py
   def test_my_evaluator():
       # Test implementation
       pass
   ```

### Configuration Management

Environment variables are managed through `.env` file:

```bash
OPENAI_API_KEY=your-api-key
DEFAULT_MODEL=gpt-3.5-turbo
MAX_RETRIES=3
TIMEOUT_SECONDS=30
LOG_LEVEL=INFO
```

Access configuration in code:
```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
```

## Debugging and Troubleshooting

### Common Issues

1. **Import errors:** Ensure package is installed in development mode (`pip install -e .`)
2. **Test failures:** Check test dependencies and environment variables
3. **Ruff errors:** Run `bash clean_up.sh .` to auto-fix formatting issues

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### IDE Configuration

**VS Code settings (.vscode/settings.json):**
```json
{
    "python.defaultInterpreter": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "ruff",
    "python.testing.pytestEnabled": true
}
```

## Release Process

### Version Management

1. **Update version in `pyproject.toml`**
2. **Update CHANGELOG.md**
3. **Create git tag:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

### Publishing to PyPI

```bash
# Build package
python -m build

# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

## Performance Considerations

### Optimization Guidelines

1. **Use async/await for API calls**
2. **Implement connection pooling**
3. **Cache evaluation results when possible**
4. **Profile code using `cProfile`**
5. **Monitor memory usage with `memory_profiler`**

### Benchmarking Performance

```python
import time
import cProfile

def profile_function():
    pr = cProfile.Profile()
    pr.enable()
    # Your code here
    pr.disable()
    pr.print_stats(sort='cumulative')
```

## Security Guidelines

1. **Never commit API keys or secrets**
2. **Use environment variables for sensitive data**
3. **Validate all user inputs**
4. **Sanitize file paths and names**
5. **Use secure HTTP connections only**

## Contributing Guidelines

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No sensitive data exposed
- [ ] Performance impact considered
- [ ] Backward compatibility maintained

### Getting Help

- **Issues:** GitHub Issues for bug reports and feature requests
- **Discussions:** GitHub Discussions for questions and ideas
- **Documentation:** Check existing docs and README
- **Code Review:** Request review from maintainers

## Maintenance Tasks

### Regular Maintenance

1. **Update dependencies monthly**
2. **Review and update documentation**
3. **Monitor test coverage**
4. **Check for security vulnerabilities**
5. **Clean up deprecated code**

### Dependency Updates

```bash
# Check outdated packages
pip list --outdated

# Update requirements
pip-compile --upgrade requirements.in

# Update development requirements
pip-compile --upgrade requirements-dev.in
```

This developer guide should be updated as the project evolves. For questions or suggestions, please open an issue or discussion on GitHub.