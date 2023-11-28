from json import loads
from pathlib import Path

import click
from loguru import logger

from essential_takehome.chain import run_chain
from essential_takehome.llm import (
    ASSISTANT_NAME,
    delete_all_files,
    delete_assistant,
    get_assistant,
    make_assistant,
    update_assistant
)

@click.group()
def cli():
    pass

@cli.command()
def deploy_agent():
    existing = get_assistant()
    if existing is not None:
        logger.info(f"Assistant {ASSISTANT_NAME} already exists, updating. {existing.id}")
        updated = update_assistant(existing.id)
        return updated.id

    logger.info(f"Assistant {ASSISTANT_NAME} does not exist, creating")
    created = make_assistant()
    logger.info(f"Created new assistant {ASSISTANT_NAME} with id {created.id}")
    return created.id

@cli.command()
def delete_agent():
    existing = get_assistant()
    if existing is None:
        logger.info(f"Cannot delete; {ASSISTANT_NAME} does not exist.")
        return

    response = delete_assistant(existing.id)
    logger.info(response)

    logger.info("Deleting project files")
    delete_all_files()

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
