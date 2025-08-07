# src/decipher_bench/models.py
"""Pydantic models for structuring test cases and results."""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class TestMetadata(BaseModel):
    """Metadata for a test case."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    author: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    difficulty: Literal["easy", "medium", "hard"] = "medium"


class TestCaseParameters(BaseModel):
    """LLM API parameters for a test case."""

    temperature: float = 0.0
    max_tokens: int = 512
    top_p: float = 1.0


class Evaluation(BaseModel):
    """Evaluation criteria for a test case."""

    type: str = Field(..., description="The evaluation method to use.")
    expected_answer: Any = Field(
        None, description="The ground truth answer."
    )
    acceptable_variations: Optional[List[str]] = Field(
        None, description="Acceptable string variations for matching."
    )
    regex_pattern: Optional[str] = Field(
        None, description="Regex pattern for matching."
    )


class TestCase(BaseModel):
    """A single, complete test case definition."""

    system_prompt: str = "You are a helpful assistant."
    user_prompt: str
    context: Optional[str] = None
    parameters: TestCaseParameters = Field(default_factory=TestCaseParameters)


class TestDefinition(BaseModel):
    """The complete structure of a test definition file."""

    test_id: str
    version: str = "1.0"
    metadata: TestMetadata = Field(default_factory=TestMetadata)
    test_case: TestCase
    evaluation: Evaluation


class TestResult(BaseModel):
    """The result of a single test run."""

    test_id: str
    passed: bool
    score: float
    actual_output: str
    expected_output: Any
    error_message: Optional[str] = None
    execution_time_ms: float
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None