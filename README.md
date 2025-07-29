# 🔍 Decipher Bench

An open-source LLM benchmarking framework that provides comprehensive evaluation metrics for Large Language Models. Built with Python 3.12 and designed for extensibility, Decipher Bench helps developers and researchers understand the true capabilities of their language models.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Features

- **Unified API Interface**: Use OpenAI library to interact with all LLMs
- **Comprehensive Test Suite**: Organized tests across multiple dimensions
- **Extensible Framework**: Easy to add new tests and evaluation metrics
- **Performance Tracking**: Monitor latency, consistency, and resource usage
- **Safety Evaluation**: Built-in bias and toxicity detection
- **Automated Scoring**: JSON-based test definitions with customizable validators

## 📋 Requirements

- Python 3.12+
- OpenAI API key (or compatible API endpoints)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/decipher-bench.git
cd decipher-bench

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install -e .[dev]
```

### Basic Usage

```python
from decipher_bench import LLMBenchmark

# Initialize benchmark
benchmark = LLMBenchmark(api_key="your-api-key")

# Run a specific test
result = benchmark.run_test("knowledge/factual/test_001.json")

# Run all tests in a category
results = benchmark.run_category("knowledge/factual")

# Generate report
benchmark.generate_report(results, output="report.html")
```

### Command Line Interface

```bash
# Run all tests
decipher-bench run --all

# Run specific test group
decipher-bench run --group knowledge

# Run specific test type
decipher-bench run --group knowledge --type factual

# Generate comparison report
decipher-bench compare gpt-4 gpt-3.5-turbo --output comparison.html
```

## 📁 Test Structure

Tests are organized in a hierarchical structure:

```
tests/
├── knowledge/          # Knowledge & Reasoning Tests
│   ├── factual/       # Factual accuracy
│   ├── reasoning/     # Logical reasoning
│   └── commonsense/   # Common sense understanding
├── generation/        # Content Generation Tests
│   ├── creative/      # Creative writing
│   ├── structured/    # Structured output (JSON, XML, etc.)
│   └── code/          # Code generation
├── safety/            # Safety & Ethics Tests
│   ├── bias/          # Bias detection
│   ├── toxicity/      # Harmful content filtering
│   └── alignment/     # Instruction following
└── performance/       # Performance Metrics
    ├── latency/       # Response time measurement
    └── consistency/   # Output consistency checks
```

## 📝 Test Definition Format

Each test is defined as a JSON file with the following structure:

```json
{
  "test_id": "knowledge_factual_001",
  "version": "1.0",
  "metadata": {
    "created_at": "2024-01-25",
    "author": "team_member_name",
    "tags": ["factual", "science", "basic"],
    "difficulty": "medium",
    "estimated_tokens": 150
  },
  "test_case": {
    "system_prompt": "You are a helpful assistant.",
    "user_prompt": "What is the capital of France?",
    "context": null,
    "parameters": {
      "temperature": 0.0,
      "max_tokens": 100,
      "top_p": 1.0
    }
  },
  "evaluation": {
    "type": "exact_match",
    "expected_answer": "Paris",
    "acceptable_variations": ["Paris, France", "The capital of France is Paris"],
    "scoring": {
      "correct": 1.0,
      "partial": 0.5,
      "incorrect": 0.0
    }
  }
}
```

## 🛠️ Development

### Code Quality

We use `ruff` for linting and formatting. All code must pass ruff checks:

```bash
# clean_up.sh
bash clean_up.sh .

# Check code
ruff check .

# Format code
ruff format .

# Run pre-commit hooks
pre-commit run --all-files
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_evaluation.py
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- All tests pass
- Code passes ruff checks
- Test coverage remains above 80%
- Commits follow conventional commit format

## 📊 Evaluation Metrics

### Supported Evaluation Types

- **Exact Match**: Direct string comparison
- **Semantic Similarity**: Using embeddings
- **Regex Patterns**: Pattern matching
- **Custom Validators**: Python functions for complex logic
- **Statistical Analysis**: Distribution and consistency checks

### Scoring System

Each test can define custom scoring rubrics:
- Binary (pass/fail)
- Scaled (0.0 - 1.0)
- Multi-dimensional (accuracy, relevance, safety)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-api-key
DEFAULT_MODEL=gpt-3.5-turbo
MAX_RETRIES=3
TIMEOUT_SECONDS=30
```

### Custom Model Endpoints

Support for OpenAI-compatible endpoints:

```python
benchmark = LLMBenchmark(
    api_key="your-key",
    base_url="https://your-endpoint.com/v1"
)
```

## 📈 Benchmarking Results

Results are saved in JSON format and can be visualized using our reporting tools:

```json
{
  "benchmark_id": "bench_20240125_100000",
  "timestamp": "2024-01-25T10:00:00Z",
  "llm_under_test": {
    "model": "gpt-4",
    "version": "gpt-4-0125-preview",
    "provider": "openai",
    "temperature": 0.7,
    "max_tokens": 2048
  },
  "summary": {
    "total_tests": 150,
    "passed": 142,
    "failed": 8,
    "average_score": 0.91,
    "execution_time": "45m 23s"
  },
  "results_by_category": {
    "knowledge": {
      "factual": {
        "score": 0.95,
        "tests_run": 25,
        "passed": 24,
        "failed_tests": ["knowledge_factual_017"]
      },
      "reasoning": {
        "score": 0.88,
        "tests_run": 20,
        "passed": 18,
        "failed_tests": ["knowledge_reasoning_003", "knowledge_reasoning_011"]
      },
      "commonsense": {
        "score": 0.92,
        "tests_run": 15,
        "passed": 14,
        "failed_tests": ["knowledge_commonsense_009"]
      }
    },
    "generation": {
      "creative": {
        "score": 0.90,
        "tests_run": 30,
        "passed": 27,
        "failed_tests": ["generation_creative_012", "generation_creative_021", "generation_creative_028"]
      },
      "structured": {
        "score": 0.94,
        "tests_run": 25,
        "passed": 24,
        "failed_tests": ["generation_structured_015"]
      },
      "code": {
        "score": 0.87,
        "tests_run": 35,
        "passed": 30,
        "failed_tests": ["generation_code_004", "generation_code_011", "generation_code_019", "generation_code_027", "generation_code_033"]
      }
    }
  },
  "detailed_results": [
    {
      "test_id": "knowledge_factual_001",
      "test_name": "Capital Cities - Basic",
      "category": "knowledge/factual",
      "score": 1.0,
      "passed": true,
      "execution_time_ms": 523,
      "prompt_tokens": 45,
      "completion_tokens": 12,
      "test_parameters": {
        "temperature": 0.0,
        "max_tokens": 100
      },
      "expected": "Paris",
      "actual": "Paris",
      "evaluation_method": "exact_match"
    },
    {
      "test_id": "generation_code_004",
      "test_name": "Binary Search Implementation",
      "category": "generation/code",
      "score": 0.0,
      "passed": false,
      "execution_time_ms": 2341,
      "prompt_tokens": 120,
      "completion_tokens": 450,
      "test_parameters": {
        "temperature": 0.2,
        "max_tokens": 1000
      },
      "error": "Code execution failed: IndexError on edge case",
      "evaluation_method": "code_execution"
    }
  ]
}
```

## 🤝 Sponsors

This project is proudly sponsored by [Decipher Something](https://www.deciphersomething.com) - Building AI that understands your ground truth.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the unified API interface
- The open-source community for invaluable feedback
- All contributors who help improve LLM evaluation

## 📞 Contact

- Issues: [GitHub Issues](https://github.com/yourusername/decipher-bench/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/decipher-bench/discussions)
- Email: team@deciphersomething.com

---

**Note**: This project is under active development. APIs and test formats may change. Please check the [CHANGELOG](CHANGELOG.md) for updates.