from jinja2 import Environment, PackageLoader, select_autoescape

class PromptManager:
    def __init__(self) -> None:
        self.env = Environment(
            loader=PackageLoader("essential_takehome"),
            autoescape=select_autoescape()
        )

    @property
    def gpt_instructions(self):
        return self.env.get_template("gpt_instructions.jinja")

    # maybe change to return a string, not jinja?
    @property
    def analyst_prompt(self):
        return self.env.get_template("analyst_prompt.jinja")


Prompts = PromptManager()
