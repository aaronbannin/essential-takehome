# from json import loads
# from pathlib import Path
from dataclasses import dataclass
from typing import Any

import click
from langchain.chat_models import ChatOpenAI
from loguru import logger

import essential_takehome.questions as questions
from essential_takehome.chains import run_chain, run_judge
from essential_takehome.files import ProjPaths, load_dataframes

@dataclass
class Response:
    key: str
    difficulty: int
    score: int

    def as_row(self) -> str:
        return f"{self.key}\t\t{self.difficulty}\t{self.score}"

class ReportCard:
    def __init__(self):
        self.responses: list[Response] = []

    # def __str__(self):
    #     return "\n".join(str(r) for r in self.responses)

    def score_result(self, question: dict[str, Any], judge_response: str):
        key = question["key"]
        difficulty = int(question["difficulty"])
        score = 0

        if "yes" in judge_response:
            score = difficulty

        self.responses.append(Response(key, difficulty, score))

    def report(self) -> str:
        all_responses = "\n".join([r.as_row() for r in self.responses])
        diff = sum([r.difficulty for r in self.responses])
        scores = sum([r.score for r in self.responses])
        pct = scores / diff

        return f"Final Grade: {pct}\n{all_responses}"



@click.group()
def cli():
    pass

@cli.command()
@click.option("-v", "--verbose", is_flag=True)
def eval(verbose: bool):
    datasets = load_dataframes()
    llm = ChatOpenAI(verbose=True)
    report_card = ReportCard()

    for q in questions.base:
        llm_response = run_chain(llm, q["question"], datasets, verbose)

        logger.info(llm_response)

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
