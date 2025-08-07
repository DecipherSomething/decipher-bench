"""Functions for evaluating LLM responses against test cases."""

import re
from typing import Any, Dict

from bert_score import score as bert_scorer
from rouge_score import rouge_scorer

from decipher_bench.models import Evaluation


def evaluate_response(
    response: str, evaluation: Evaluation
) -> Dict[str, Any]:
    """
    Dispatch to the appropriate evaluation function.
    
    """
    eval_type = evaluation.type
    eval_functions = {
        "exact_match": exact_match_evaluator,
        "regex_match": regex_match_evaluator,
        "bert_score": bertscore_evaluator, 
    }

    if eval_type not in eval_functions:
        raise ValueError(f"Unknown evaluation type: {eval_type}")

    return eval_functions[eval_type](response, evaluation)


def bertscore_evaluator(
    response: str, evaluation: Evaluation
) -> Dict[str, Any]:
    """
    Evaluate semantic similarity using BERTScore.

    The F1 score is used as the primary metric. This evaluator does not
    determine a pass/fail status based on a threshold; it only returns the
    similarity score. The 'passed' field is always True to indicate a
    successful evaluation, and the score should be interpreted directly.
    """
    if not isinstance(evaluation.expected_answer, str):
        raise TypeError("expected_answer must be a string for BERTScore.")


    candidates = [response.strip()]
    references = [evaluation.expected_answer.strip()]

    _, _, f1 = bert_scorer(
        candidates, references, lang="en", verbose=False
    )

    f1_score = f1.item()

    return {"score": f1_score, "passed": True}


def exact_match_evaluator(
    response: str, evaluation: Evaluation
) -> Dict[str, Any]:
    """
    Evaluates the response based on exact match and ROUGE-L F1 score.
    """
    response_clean = response.strip()
    expected_answer = str(evaluation.expected_answer).strip()
    variations = evaluation.acceptable_variations or []

    passed = response_clean == expected_answer
    if not passed and variations:
        passed = any(
            response_clean == var.strip() for var in variations
        )

    
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    scores = scorer.score(expected_answer, response_clean)
    rouge_l_f1 = scores["rougeL"].fmeasure

    return {"score": rouge_l_f1, "passed": passed}


def regex_match_evaluator(
    response: str, evaluation: Evaluation
) -> Dict[str, Any]:
    """
    Evaluate if the response matches a given regex pattern.
    """
    if not evaluation.regex_pattern:
        raise ValueError("Regex pattern not provided for regex_match evaluator.")

    is_match = bool(re.search(evaluation.regex_pattern, response))
    score = 1.0 if is_match else 0.0
    passed = is_match
    return {"score": score, "passed": passed}