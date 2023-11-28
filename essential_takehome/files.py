from pathlib import Path

import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape
from loguru import logger


class ProjPaths:
    root = Path(__file__).parent
    data = root / "data"
    templates = root / "templates"

# def get_data_path():
#     cwd = Path.cwd()
#     # Path(__file__).parent
#     # return cwd / "essential_takehome" / "data"
#     return ProjPaths.data

# def get_local_files():
#     datapath = get_data_path()
#     return [f for f in ProjPaths.data.iterdir() if f.is_file()]

def load_dataframes() -> dict[str, pd.DataFrame]:
    """Load dataframes from local files and return them as a dictionary."""
    data_files = [f for f in ProjPaths.data.iterdir() if f.is_file()]
    datasets = {}
    for csv in data_files:
        df = pd.read_csv(csv)
        datasets[csv.name] = df

        logger.info(f"Loaded file {csv.name}")
    return datasets

class PromptManager:
    def __init__(self) -> None:
        self.env = Environment(
            loader=PackageLoader("essential_takehome"),
            autoescape=select_autoescape()
        )

    def _raw_text(self, prompt_name: str) -> str:
        filepath = ProjPaths.templates / (prompt_name + ".jinja")
        with open(filepath) as f:
            return f.read()


    @property
    def gpt_instructions(self):
        return self.env.get_template("gpt_instructions.jinja")

    @property
    def analyst_prompt(self):
        return self._raw_text("analyst_prompt")


Prompts = PromptManager()
