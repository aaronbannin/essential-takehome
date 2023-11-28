from io import StringIO
import sys

from langchain.agents.tools import Tool
from loguru import logger

from essential_takehome.files import load_dataframes


class PythonREPL:
    """Simulates a standalone Python REPL."""

    def __init__(self):
        # Initialize the datasets dictionary in the constructor
        self.datasets = load_dataframes()

    @classmethod
    def as_tool(cls) -> Tool:
        return Tool(
            "Python REPL",
            PythonREPL().run,
            """A Python shell. Use this to execute python commands. Input should be a valid python command.
            If you expect output it should be printed out.""",
        )

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
