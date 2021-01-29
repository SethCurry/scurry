"""Utilities for gathering user input."""

import typing

PromptType = typing.TypeVar("PromptType")
ValidatorType = typing.Callable[[PromptType], None]


class Prompt(typing.Generic[PromptType]):
    """
    A saved prompt to show to users.

    ---
    **Attributes:**
    * question (str): The question to ask users.
    * validator(`ValidatorType`): The function to use to validate user input.

    """

    def __init__(self, question: str, validators: typing.List[ValidatorType] = []):
        """
        Create a new `Validator`.

        ---
        **Arguments:**
        * question (str): The question to ask the user.

        ---
        **Keywords:**
        * validators (typing.List[ValidatorType]): The function to use to validate the user's input.

        """
        self.question = question
        self.validators = validators

    def parse(self, item: str) -> PromptType:
        raise NotImplementedError()

    def validate(self, item: PromptType):
        for validator in self.validators:
            validator(item)
        return

    def run(self) -> PromptType:
        """
        Execute the prompt, and return the user's input.

        If `validator` is set and the user input fails to return True for the validator,
        the user will be re-prompted until their input passes.

        """
        is_valid = False
        while not is_valid:
            resp = input(self.question)
            parsed = self.parse(resp)

            try:
                self.validate(parsed)
                return parsed
            except Exception:
                continue

        return parsed


class IntPrompt(Prompt[int]):
    def parse(self, item: str) -> int:
        return int(item)
