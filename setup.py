#!/usr/bin/env python3
"""
Setup script for Decipher Bench - LLM Benchmarking Framework

This setup.py is maintained for backward compatibility.
For modern Python packaging, see pyproject.toml.
"""

import os

from setuptools import find_packages, setup


# Read long description from README
def read_readme():
    """Read the README file for long description."""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    try:
        with open(readme_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "An open-source LLM benchmarking framework"


# Read version from a separate file to avoid import issues
def read_version():
    """Read version from __init__.py or fallback to default."""
    version_file = os.path.join(os.path.dirname(__file__), "src", "__init__.py")
    try:
        with open(version_file, encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return "0.1.0"


# Core requirements
INSTALL_REQUIRES = [
    "openai>=1.0.0",
    "requests>=2.28.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "click>=8.0.0",
    "rich>=13.0.0",
    "jinja2>=3.1.0",
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "scikit-learn>=1.3.0",
]

# Development requirements
DEV_REQUIRES = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "twine>=4.0.0",
    "build>=0.10.0",
]

# Documentation requirements
DOCS_REQUIRES = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings[python]>=0.24.0",
]

# All extra requirements
EXTRAS_REQUIRE = {
    "dev": DEV_REQUIRES,
    "docs": DOCS_REQUIRES,
    "all": DEV_REQUIRES + DOCS_REQUIRES,
}

setup(
    name="decipher-bench",
    version=read_version(),
    author="Decipher Something Team",
    author_email="team@deciphersomething.com",
    description="An open-source LLM benchmarking framework",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/deciphersomething/decipher-bench",
    project_urls={
        "Homepage": "https://github.com/deciphersomething/decipher-bench",
        "Documentation": "https://decipher-bench.readthedocs.io/",
        "Repository": "https://github.com/deciphersomething/decipher-bench",
        "Issue Tracker": "https://github.com/deciphersomething/decipher-bench/issues",
        "Sponsor": "https://www.deciphersomething.com",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "decipher_bench": [
            "templates/*.html",
            "templates/*.css",
            "templates/*.js",
        ],
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Benchmark",
        "Typing :: Typed",
    ],
    keywords=[
        "llm",
        "benchmark",
        "evaluation",
        "ai",
        "machine-learning",
        "natural-language-processing",
        "openai",
        "testing",
        "performance",
        "metrics",
    ],
    entry_points={
        "console_scripts": [
            "decipher-bench=decipher_bench.cli:main",
        ],
    },
    zip_safe=False,
    platforms=["any"],
)
