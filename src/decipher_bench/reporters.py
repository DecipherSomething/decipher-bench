from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List, Dict, Any
from collections import defaultdict
import os
from datetime import datetime

def generate_html_report(results: List[Dict[str, Any]], output_path: str):
    """
    Generates an HTML report from a list of test results using a Jinja2 template.
    """

    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["passed"])
    failed_tests = total_tests - passed_tests
    average_score = sum(r["score"] for r in results if r["score"] is not None) / total_tests if total_tests > 0 else 0
    total_time_s = sum(r["execution_time_ms"] for r in results) / 1000

    results_by_category = defaultdict(list)
    for r in results:
        results_by_category[r['category']].append(r)

    summary_by_category = {}
    for category, cat_results in results_by_category.items():
        cat_total = len(cat_results)
        cat_passed = sum(1 for r in cat_results if r["passed"])
        summary_by_category[category] = {
            "score": sum(r["score"] for r in cat_results if r["score"] is not None) / cat_total if cat_total > 0 else 0,
            "tests_run": cat_total,
            "passed": cat_passed,
            "failed": cat_total - cat_passed,
        }

    summary = {
        "total_tests": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "average_score": f"{average_score:.2f}",
        "execution_time": f"{total_time_s:.2f}s",
    }
    

    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('report_template.html')

    html_content = template.render(
        benchmark_id=f"bench_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        timestamp=datetime.now().isoformat(),
        summary=summary,
        summary_by_category=summary_by_category,
        detailed_results=results
    )

    with open(output_path, 'w') as f:
        f.write(html_content)