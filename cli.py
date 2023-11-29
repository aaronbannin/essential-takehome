from dataclasses import dataclass
from typing import Any

import click
from dotenv import load_dotenv
from langchain.chat_models import ChatAnthropic
from langchain.chat_models import ChatOpenAI
from loguru import logger
from tabulate import tabulate

import essential_takehome.questions as questions
from essential_takehome.chains import run_chain, run_judge
from essential_takehome.files import ProjPaths, load_dataframes


load_dotenv()


@dataclass
class Response:
    key: str
    difficulty: dict[str, int]
    is_correct: bool

    def as_row(self):
        return {
            "key": self.key,
            "rating": self.rating,
            "score": self.score,
            **self.difficulty
        }

    @property
    def bin(self) -> int:
        bin_size = len(self.difficulty.keys())
        bin_value = sum(int(v) for v in self.difficulty.values())
        if bin_value <= bin_size:
            return 1
        elif bin_value <= bin_size * 2:
            return 2
        else:
            return 3

    @property
    def max_possible_score(self):
        """For the bin, what is the best possible score?"""
        return self.bin * len(self.difficulty.keys())

    @property
    def score(self):
        return self.max_possible_score if self.is_correct else 0

    @property
    def rating(self) -> str:
        if self.bin == 1:
            return "easy"
        elif self.bin == 2:
            return "medium"
        else:
            return "hard"

class ReportCard:
    def __init__(self):
        self.responses: list[Response] = []

    def score_result(self, question: dict[str, Any], judge_response: str):
        key = question["key"]
        difficulty = self._get_difficulty(question)
        is_correct = "yes" in judge_response

        self.responses.append(Response(key, difficulty, is_correct))

    def _get_difficulty(self, question: dict[str, Any]) -> dict[str, int]:
        key = question["key"]
        if "total_difficulty" in question:
            return {"total_difficulty": question["total_difficulty"]}
        elif "difficulty" in question:
            return question["difficulty"]
        else:
            raise KeyError(f"Question {key} must have either difficulty or total_difficulty")

    def report(self) -> str:
        diff = sum([r.max_possible_score for r in self.responses])
        scores = sum([r.score for r in self.responses])
        pct = scores / diff

        table = tabulate([r.as_row() for r in self.responses], headers="keys")
        return f"Final Grade: {pct}\n{table}"


model_map ={
    "gpt3": "gpt-3.5-turbo",
    "gpt4": "gpt-4",
    "clau": "claude-2.1"
}

def get_llm(model: str):
    # this Langchain model relates to chat completions API
    # https://github.com/langchain-ai/langchain/blob/686162670e2fe15fb906999da84d36a273b2f25e/libs/langchain/langchain/chat_models/openai.py#L312
    if "gpt" in model:
        return ChatOpenAI(model_name=model)

    return ChatAnthropic(model=model)

@click.group()
def cli():
    pass

@cli.command()
@click.option('-m', '--model', default="gpt3", type=click.Choice(model_map.keys()))
@click.option("-v", "--verbose", is_flag=True)
def eval(model: str, verbose: bool):
    datasets = load_dataframes()
    llm = get_llm(model_map[model])
    report_card = ReportCard()

    logger.info(f"Using {model_map[model]}")
    for q in questions.base:
        llm_response = run_chain(llm, q["question"], datasets, verbose)

        logger.info("Result of Python returned from LLM")
        print(llm_response)

        answer_file = ProjPaths.answers / (q["key"] + ".txt")
        with open(answer_file) as a:
            answer = a.read()
            result = run_judge(llm, answer, llm_response, verbose)
            logger.info("Judge result")
            print(result)

            report_card.score_result(q, result)

    logger.info(report_card.report())


if __name__ == "__main__":
    cli()
