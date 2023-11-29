# import pandas as pd
from dotenv import load_dotenv
from langchain.callbacks.tracers import ConsoleCallbackHandler
# from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.schema import StrOutputParser
from langchain.prompts import PromptTemplate
from loguru import logger
from pandas import DataFrame

from essential_takehome.files import Prompts
from essential_takehome.tools import PythonREPL


load_dotenv()


def summary_from_dataframe(name: str, df: DataFrame):
    return f"""
    key
    {name}

    df.head()
    {df.head()}
"""


def run_chain(llm: BaseChatModel, question: str, datasets: dict[str, DataFrame], verbose: bool = False):
    """
    To see fully rendered prompt, run in verbose mode and look for the following log line:
    [llm/start] [1:chain:RunnableSequence > 3:llm:ChatOpenAI] Entering LLM run with input:
    """
    callbacks = []
    analyst_prompt = PromptTemplate.from_template(
        Prompts.analyst_prompt,
        template_format="jinja2"
    )

    if verbose:
        callbacks.append(ConsoleCallbackHandler())

    # this Langchain model relates to chat completions API
    # https://github.com/langchain-ai/langchain/blob/686162670e2fe15fb906999da84d36a273b2f25e/libs/langchain/langchain/chat_models/openai.py#L312
    # llm = ChatOpenAI(verbose=True)
    chain = (analyst_prompt | llm | StrOutputParser() | PythonREPL.as_tool())

    summaries = "\n".join([summary_from_dataframe(name, df) for name, df in datasets.items()])
    result = chain.invoke(
        {"question": question, "summaries": summaries},
        config={"callbacks": callbacks}
    )

    return result

def run_judge(llm: BaseChatModel, answer: str, llm_response: str, verbose: bool = False):
    callbacks = []
    judge_prompt = PromptTemplate.from_template(
        Prompts.judge_prompt,
        template_format="jinja2"
    )

    if verbose:
        callbacks.append(ConsoleCallbackHandler())

    chain = (judge_prompt | llm | StrOutputParser())
    return chain.invoke(
        {"student_response": llm_response, "answer": answer },
        config={"callbacks": callbacks}
    )
