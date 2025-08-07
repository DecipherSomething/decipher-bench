# src/decipher_bench/cli.py
"""Command-line interface for Decipher Bench."""

import os
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from decipher_bench.benchmark import LLMBenchmark


@click.group()
@click.version_option()
def main() -> None:
    """Decipher Bench: An open-source LLM benchmarking framework."""
    load_dotenv()


@main.command()
@click.option(
    "--test",
    "test_path",
    type=click.Path(exists=True, path_type=Path),
    help="Path to a single test JSON file.",
)
@click.option(
    "--category",
    "category_path",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Path to a directory of tests.",
)
@click.option(
    "--model",
    required=True,
    help="The model identifier, e.g., 'meta-llama/Llama-3.1-8B-Instruct'.",
)
@click.option(
    "--api-key",
    envvar="OPENAI_API_KEY",
    help="OpenAI API key. Can also be set via OPENAI_API_KEY env var.",
)
@click.option(
    "--base-url",
    help="The base URL for the LLM API.",
)
def run(
    test_path: Path | None,
    category_path: Path | None,
    model: str,
    api_key: str | None,
    base_url: str | None,
) -> None:
    """Run benchmarks on a specified model."""
    console = Console()
    if not api_key:
        console.print("[bold red]Error: API key not found.[/bold red]")
        console.print(
            "Please provide it with --api-key or set a DECIPHER_API_KEY env var."
        )
        return

    if not test_path and not category_path:
        console.print(
            "[bold red]Error: You must specify --test or --category.[/bold red]"
        )
        return

    benchmark = LLMBenchmark(api_key=api_key, base_url=base_url)
    results = []

    if test_path:
        with console.status(f"Running test [cyan]{test_path.name}[/cyan]..."):
            result = benchmark.run_test(test_path, model)
            results.append(result)

    if category_path:
        files = list(sorted(category_path.glob("**/*.json")))
        with console.status(
            f"Running {len(files)} tests in [cyan]{category_path.name}[/cyan]..."
        ) as status:
            for i, file in enumerate(files):
                status.update(
                    f"Running test {i+1}/{len(files)}: [cyan]{file.name}[/cyan]"
                )
                result = benchmark.run_test(file, model)
                results.append(result)

    # --- Display Results ---
    table = Table(
        title=f"Benchmark Results for [bold cyan]{model}[/bold cyan]"
    )
    table.add_column("Test ID", style="magenta")
    table.add_column("Passed", justify="center")
    table.add_column("Score", justify="right", style="green")
    table.add_column("Time (ms)", justify="right", style="yellow")

    if not results:
        console.print("[yellow]No tests were run.[/yellow]")
        return

    passed_count = sum(1 for res in results if res.passed)
    total_score = sum(res.score for res in results)

    for res in results:
        status = "[bold green]✔[/bold green]" if res.passed else "[bold red]✖[/bold red]"
        table.add_row(
            res.test_id, status, f"{res.score:.2f}", f"{res.execution_time_ms:.2f}"
        )

    console.print(table)
    summary_style = "bold green" if passed_count == len(results) else "bold yellow"
    console.print(
        f"[{summary_style}]Summary: "
        f"{passed_count}/{len(results)} tests passed. "
        f"Average Score: {total_score / len(results):.2f}[/{summary_style}]"
    )


if __name__ == "__main__":
    main()