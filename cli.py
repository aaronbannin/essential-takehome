from json import loads
from pathlib import Path

import click

from essential_takehome.chain import run_chain


@click.group()
def cli():
    pass

@cli.command()
@click.option("-v", "--verbose", is_flag=True)
def eval(verbose: bool):
    cwd = Path.cwd()
    questions_path = cwd / "questions.jsonl"
    with open(questions_path) as f:
        lines = f.read().splitlines()
        for q in lines:
            question_text = loads(q)["question"]
            run_chain(question_text, verbose)


if __name__ == "__main__":
    cli()
