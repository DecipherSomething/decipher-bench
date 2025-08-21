#core.py
#Benchmark Runner
#loads test JSON files 
#evaluates BERTscore F1, ROUGE-L F1, and regex match 
#aggregates average score 

import argparse 
import json 
import re 
import glob 
from pathlib import Path 
from typing import Dict, List, Tuple
import time  



from bert_score import score as bert_scorer 
from rouge_score import rouge_scorer
import pandas as pd 
import torch 
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline 
from huggingface_hub import login


login("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") 



#loads tests into a list, if the json files don't exist, raises SystemExit error with error message 
#params:
#tests_dir (json files)
#output = tests (list of test inputs)

def load_tests(tests_dir : Path):
    tests = []
    for i in sorted(glob.glob(str(tests_dir / "*.json"))):
        with open(i, 'r', encoding = "utf-8") as file:
            tests.append(json.load(file))
    if not tests:
        raise SystemExit(f"No JSON files in {tests_dir}")
    return tests

#categorizing all three scores 
#raises ValueError if test input includes score other than 
#roue-l, bertscore, and regex_match 
def norm_type(t : str) -> str:
    t = t.strip().lower()
    if t in {"bertscore", "bert f1", "bert", "bert_f1"}:
        return "bertscore"
    if t in {"rouge_l", "rouge", "rouge-l", "rougel"}:
        return "rouge_l"
    if t in {"regex", "regex_match", "regex-match"}:
        return "regex_match" 
    raise ValueError(f"Invalid evaluation type: {t}")

def build_prompt(tokenizer, system: str, user: str, context: str | None) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system })
    if context:
        messages.append({"role": "user", "content": f"Context:\n{context}"})
    messages.append({"role": "user", "content": user})

    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        return tokenizer.apply_chat_template(messages, tokenize = False, add_generation_prompt=True)
    

    #fallback in case of plain prompt 
    parts = []
    if system:
        parts.append(f"[SYSTEM]\n{system}\n")
    if context:
        parts.append(f"[CONTEXT]\n{context}\n")
    parts.append(f"[USER]\n{user}\n\n[ASSISTANT]")
    return "\n".join(parts)



_rouge = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)

#evaluates bertscore
def eval_bertscore(candidate: str, reference: str) -> float:
    _, _, f1 = bert_scorer([candidate.strip()], [reference.strip()], lang="en", verbose=False)
    return float(f1.item())
#evaluates rouge-l score
def eval_rouge(candidate: str, reference: str) -> float:
    return float(_rouge.score(reference, candidate)["rougeL"].fmeasure)
#evaluates regex pattern
def eval_regex(candidate: str, pattern: str) -> float:
    if not pattern:
        raise ValueError("Regex pattern missing for regex_match test.")
    return 1.0 if re.search(pattern, candidate ) else 0.0


#model runner 

def load_pipeline(model_id :str, device: str | None):
    kwargs = {}
    if torch.cuda.is_available() and device != "cpu":
        kwargs.update(dict(torch_dtype = torch.float16, device_map = "auto"))
    else:
        kwargs.update(dict(torch_dtype = torch.float32, device_map = None))
    tok = AutoTokenizer.from_pretrained(model_id)
    mdl = AutoModelForCausalLM.from_pretrained(model_id, **kwargs)
    gen = pipeline("text-generation", model=mdl, tokenizer=tok)
    return gen, tok

def generate(gen_pipe, tokenizer, prompt: str, temperature: float | None, top_p: float | None, max_new_tokens: int | None) -> str:
    params = {}
    if temperature is not None:
        params["temperature"] = float(temperature)
    if top_p is not None:
        params["top_p"] = float(top_p)
    if max_new_tokens is not None:
        params["max_new_tokens"] = int(max_new_tokens)
    else:
        params["max_new_tokens"] = 64  

    with torch.inference_mode():
        out = gen_pipe(prompt, **params)
    text = out[0]["generated_text"]

    # If chat template was used, the model may echo the prompt; keep only the tail after the prompt
    if text.startswith(prompt):
        return text[len(prompt):].strip()
    return text.strip()

    
def run(models: List[str], tests: List[Dict], override_eval_type: str | None) -> Dict:
    per_model_details: Dict[str, List[Dict]] = {}
    per_model_scores: Dict[str, List[float]] = {}

    for model_id in models:
        print(f"\n=== Running model: {model_id} ===")
        gen, tok = load_pipeline(model_id, device=None)
        details = []
        scores = []

        
        #takes test input 
        for t in tests:
            tc = t["test_case"]
            system = tc.get("system_prompt", "")
            user = tc.get("user_prompt", "")
            context = tc.get("context")
            params = tc.get("parameters", {}) or {}
            prompt = build_prompt(tok, system, user, context)

            #generates the 
            t0 = time.time()
            actual = generate(
                gen_pipe=gen,
                tokenizer=tok,
                prompt=prompt,
                temperature=params.get("temperature"),
                top_p=params.get("top_p"),
                max_new_tokens=params.get("max_tokens"),
            )
            exec_ms = int((time.time() - t0) * 1000)

            #evaluates score for each 
            expected = str(t["evaluation"]["expected_answer"])
            etype = norm_type(override_eval_type or t["evaluation"]["type"])

            if etype == "bertscore":
                score = eval_bertscore(actual, expected)
                metric = "bert_f1"
            elif etype == "rouge_l":
                score = eval_rouge(actual, expected)
                metric = "rouge_l_f1"
            elif etype == "regex_match":
                score = eval_regex(actual, t["evaluation"].get("regex_pattern"))
                metric = "regex_match"
            else:
                raise ValueError(f"Unsupported eval type: {etype}")

            scores.append(score)
            details.append({
                "test_id": t["test_id"],
                "metric": metric,
                "score": score,
                "execution_time_ms": exec_ms,
                "expected": expected,
                "actual": actual,
            })

        per_model_details[model_id] = details
        per_model_scores[model_id] = scores

    #makes summary 
    summary = {
        mid: {
            "total_tests": len(per_model_scores[mid]),
            "average_score": (sum(per_model_scores[mid]) / len(per_model_scores[mid])) if per_model_scores[mid] else 0.0,
        }
        for mid in models
    }

    return {
        "summary_by_model": summary,
        "detailed_results": per_model_details,
    }


def main():
    ap = argparse.ArgumentParser(description="Compare small LLMs on JSON tests")
    ap.add_argument("--hf-token", default=None, help="Hugging Face access token (or set HF_TOKEN env and omit)")
    ap.add_argument("--tests-dir", type=Path, required=True, help="Folder containing test JSON files")
    ap.add_argument("--models", nargs="+", required=True,
                    help="Space-separated list of HF model ids, e.g. google/gemma-2-2b-it meta-llama/Llama-3.2-1B-Instruct")
    ap.add_argument("--eval-type", default=None,
                    help="Optional override: BERTscore, ROUGE_L, or regex_match")
    ap.add_argument("--output", type=Path, default=Path("compare_results.json"))
    args = ap.parse_args()

    if args.hf_token:
        login(args.hf_token)

    tests = load_tests(args.tests_dir)
    report = run(models= args.models, tests= tests, override_eval_type=args.eval_type)

    args.output.parent.mkdir(parents = True, exist_ok = True)
    with open(args.output, "w", encoding= "utf-8") as f:
        json.dump(report, f, indent = 2)

    print("\n=== Summary ===")
    for mid, row in report["summary_by_model"].items():
        print(f"{mid}: avg={row['average_score']:.4f} over {row['total_tests']} tests")
    print(f"Wrote {args.output}")

if __name__ == "__main__":
    main()
        




