import json
from os import getenv
# from time import sleep
from typing import Any, Optional

from dotenv import load_dotenv
# from loguru import logger
# from pandas import DataFrame
from openai import OpenAI
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
