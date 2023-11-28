import pandas as pd
from dotenv import load_dotenv
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.prompts import PromptTemplate
from loguru import logger

from essential_takehome.files import load_dataframes, Prompts
from essential_takehome.tools import PythonREPL


load_dotenv()


def summary_from_dataframe(name: str, df: pd.DataFrame):
    return f"""
    key
    {name}

    df.head()
    {df.head()}
"""


def run_chain(question: str, verbose: bool = False):
    callbacks = []
    analyst_prompt = PromptTemplate.from_template(
        Prompts.analyst_prompt,
        template_format="jinja2"
    )

    if verbose:
        callbacks.append(ConsoleCallbackHandler())

    datasets = load_dataframes()

    # this Langchain model relates to chat completions API
    # https://github.com/langchain-ai/langchain/blob/686162670e2fe15fb906999da84d36a273b2f25e/libs/langchain/langchain/chat_models/openai.py#L312
    llm = ChatOpenAI(verbose=True)
    chain = (analyst_prompt | llm | StrOutputParser() | PythonREPL.as_tool())

    summaries = "\n".join([summary_from_dataframe(name, df) for name, df in datasets.items()])
    res = chain.invoke(
        {"question": question, "summaries": summaries},
        config={'callbacks': callbacks}
    )
    logger.info(res)
