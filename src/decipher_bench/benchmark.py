import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from openai import OpenAI
from dotenv import load_dotenv

from decipher_bench.models import (
    TestDefinition,
    TestCase,
    TestResult,
)
from . import evaluators
from .reporters import generate_html_report


class LLMBenchmark:
    """
    A class to run LLM benchmark tests from structured JSON files.
    """

    def __init__(
        self, api_key: str | None = None, base_url: str | None = None
    ):
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("BASE_URL")

        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in .env file as OPENAI_API_KEY"
            )

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def _load_test(self, test_path: Path) -> TestDefinition:
        """Loads a test definition from a JSON file."""
        with open(test_path, "r") as f:
            data = json.load(f)
        return TestDefinition(**data)

    def _call_llm(
        self, test_case: TestCase, model: str
    ) -> Dict[str, Any]:
        """Calls the LLM API with the provided test case."""
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": test_case.system_prompt,
                    },
                    {"role": "user", "content": test_case.user_prompt},
                ],
                temperature=test_case.parameters.temperature,
                max_tokens=test_case.parameters.max_tokens,
                top_p=test_case.parameters.top_p,
            )
            execution_time_ms = (time.time() - start_time) * 1000

            return {
                "actual_output": response.choices[0].message.content,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "execution_time_ms": execution_time_ms,
                "error": None,
            }
        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            return {
                "actual_output": "",
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "execution_time_ms": execution_time_ms,
                "error": str(e),
            }

    def run_test(self, test_path: Path, model: str) -> TestResult:
        """Runs a single test and returns the detailed result."""
        test_def = self._load_test(test_path)

        llm_result = self._call_llm(test_def.test_case, model)

        if llm_result["error"]:
            eval_result = {"score": 0.0, "passed": False, "error": None}
        else:
            eval_result = evaluators.evaluate_response(
                response=llm_result["actual_output"],
                evaluation=test_def.evaluation,
            )

        return TestResult(
            test_id=test_def.test_id,
            passed=eval_result["passed"],
            score=eval_result["score"],
            actual_output=llm_result["actual_output"],
            expected_output=test_def.evaluation.expected_answer,
            error_message=llm_result["error"],
            execution_time_ms=llm_result["execution_time_ms"],
            prompt_tokens=llm_result["prompt_tokens"],
            completion_tokens=llm_result["completion_tokens"],
        )

    def run_category(
        self, category_path: Path, model: str
    ) -> List[TestResult]:
        """Runs all tests in a given category directory."""
        results = []
        test_files = sorted(category_path.glob("*.json"))
        for test_file in test_files:
            results.append(self.run_test(test_file, model=model))
        return results

    def run_all(
        self, tests_dir: str = "tests", model: str = "gpt-4"
    ) -> List[TestResult]:
        """Runs all tests found in the tests directory."""
        results = []
        test_files = sorted(Path(tests_dir).rglob("*.json"))
        for test_file in test_files:
            results.append(self.run_test(test_file, model=model))
        return results

    def generate_report(self, results: List[TestResult], output_path: str):
        """Generates an HTML report from the test results."""
        generate_html_report(results, output_path)
        print(f"Report generated at: {output_path}")