import json
from os import getenv
from pathlib import Path
# from time import sleep
from typing import Any, Optional

from dotenv import load_dotenv
from loguru import logger
# from pandas import DataFrame
from openai import OpenAI
from openai.types import FileObject
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.threads.run import RequiredAction, Run
from openai.types.beta.threads.runs.function_tool_call import Function as oaiFunction

# from bball_analysis.prompts import Prompts
from essential_takehome.prompts import Prompts


load_dotenv()
client = OpenAI()

ASSISTANT_NAME = getenv("ASSISTANT_NAME", "ASB Essentail Takehome")

assistant_config = {
    "name": ASSISTANT_NAME,
    "instructions": Prompts.gpt_instructions.render(),
    "model": "gpt-3.5-turbo-1106",
    "tools": [{"type": "retrieval"}]
}

def get_assistant() -> Optional[Assistant]:
    all = client.beta.assistants.list()
    existing = [a for a in all if a.name == ASSISTANT_NAME]
    if len(existing) == 0:
        return None

    return existing[0]

def update_assistant(assistant_id: str) -> Assistant:
    return client.beta.assistants.update(
        assistant_id=assistant_id,
        **assistant_config
    )

def make_assistant() -> Assistant:
    return client.beta.assistants.create(**assistant_config)

def delete_assistant(assistant_id: str) -> AssistantDeleted:
    return client.beta.assistants.delete(assistant_id=assistant_id)

def get_data_path():
    cwd = Path.cwd()
    return cwd / "essential_takehome" / "data"

def get_project_files():
    datapath = get_data_path()
    return [f for f in datapath.iterdir() if f.is_file()]

def get_file_metadata(filename: str):
    all = client.files.list()
    existing = [f for f in all if f.filename == filename]
    if len(existing) == 0:
        return None

    return existing[0]


def upload_file(filename: str) -> FileObject:
    filepath = get_data_path() / filename
    with open(filepath, "rb") as f:
        res = client.files.create(file=f, purpose="assistants")
        return res

def upload_files():
    # datapath = get_data_path()

    files = get_project_files()
    for file in files:
        metadata = get_file_metadata(file.name)
        if metadata is None:
            res = upload_file(file.name)
            logger.info(f"Uploaded {file.name} id={res.id}")
        else:
            logger.info(f"File {file.name} already exists, skipping")

def delete_all_files():
    openai_files = client.files.list()
    project_files = {f.name for f in get_project_files()}
    for file in openai_files:
        if file.filename in project_files:
            res = client.files.delete(file.id)
            logger.info(f"Deleted filename={file.filename} id={file.id} deleted={res.deleted}")
