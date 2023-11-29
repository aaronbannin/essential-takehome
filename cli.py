from json import loads
from pathlib import Path

import click
from loguru import logger

import essential_takehome.questions as questions
from essential_takehome.chain import run_chain



@click.group()
def cli():
    pass

@cli.command()
@click.option("-v", "--verbose", is_flag=True)
def eval(verbose: bool):
    for q in questions.base:
        answer = run_chain(q["question"], verbose)

        logger.info(answer)


if __name__ == "__main__":
    cli()
