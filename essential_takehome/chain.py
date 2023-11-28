import json
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.prompts import PromptTemplate
from loguru import logger
# from pandas import read_json




load_dotenv()


analyst_prompt = PromptTemplate.from_template(
    """You are an analyst for an e-commerce store. Answer the following question.
    Question: {question}
    """
)

def run_chain(question: str, verbose: bool = False):
    callbacks = []
    if verbose:
        callbacks.append(ConsoleCallbackHandler())

    # this Langchain model relates to chat completions API
    # https://github.com/langchain-ai/langchain/blob/686162670e2fe15fb906999da84d36a273b2f25e/libs/langchain/langchain/chat_models/openai.py#L312
    llm = ChatOpenAI(verbose=True)
    chain = (analyst_prompt | llm | StrOutputParser())
    # chain = (
    #     {"synopsis": synopsis_prompt | llm | StrOutputParser()}
    #     | review_prompt
    #     | llm
    #     | StrOutputParser()
    # )
    res = chain.invoke(
        {"question": question},
        config={'callbacks': callbacks}
    )
    logger.info(res)
