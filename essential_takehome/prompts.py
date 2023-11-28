from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

class PromptManager:
    def __init__(self) -> None:
        self.env = Environment(
            loader=PackageLoader("essential_takehome"),
            autoescape=select_autoescape()
        )

    def _raw_text(self, prompt_name: str) -> str:
        filepath = Path.cwd() / "essential_takehome" / "templates" / (prompt_name + ".jinja")
        with open(filepath) as f:
            return f.read()


    @property
    def gpt_instructions(self):
        return self.env.get_template("gpt_instructions.jinja")

    @property
    def analyst_prompt(self):
        return self._raw_text("analyst_prompt")


Prompts = PromptManager()
