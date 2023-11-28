from io import StringIO
import sys

import pandas as pd
from langchain.agents.tools import Tool
from loguru import logger

from essential_takehome.llm import get_local_files


class PythonREPL:
    """Simulates a standalone Python REPL."""

    def __init__(self):
        # Initialize the datasets dictionary in the constructor
        self.datasets = self.load_dataframes()

    def load_dataframes(self) -> dict:
        """Load dataframes from local files and return them as a dictionary."""
        data_files = get_local_files()
        datasets = {}
        for csv in data_files:
            df = pd.read_csv(csv)
            datasets[csv.name] = df

            # Assuming logger is set up elsewhere in your code
            logger.info(f"Loaded file {csv.name}")
        return datasets

    def run(self, command: str) -> str:
        """Run command and returns anything printed."""
        logger.info("Running Python command")
        print(command)
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            # Include datasets in the exec environment
            exec_globals = globals().copy()
            exec_globals['datasets'] = self.datasets
            exec(command, exec_globals)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            output = str(e)
        return output


python_repl = Tool(
    "Python REPL",
    PythonREPL().run,
    """A Python shell. Use this to execute python commands. Input should be a valid python command.
    If you expect output it should be printed out.""",
)


