import argparse

from scurry.prompt import Prompt, IntPrompt


def register_card_definition():
    name_prompt = Prompt("What is the name of the card? ")
    name = name_prompt.run()

    return


def register_card():
    return


def main():
    # register definition
    # register card
    # move
    # search
    parser = argparse.ArgumentParser(description="Manage pet records")

    subparsers = parser.add_subparsers()
    reg_parser = subparsers.add_parser("register", help="Register a resource")

    reg_subparser = reg_parser.add_subparsers()

    reg_definition_parser = reg_subparser.add_parser(
        "definition",
        help="Create a definition.",
    )
    reg_definition_parser.add_argument("name", help="The name of the card.")
    reg_definition_parser.set_defaults(func=register_card_definition)

    reg_card_parser = reg_subparser.add_parser(
        "card",
        help="Register a card",
    )
    reg_card_parser.add_argument("name", help="The name of the card.")
    reg_card_parser.set_defaults(func=register_card)

    return


if __name__ == "__main__":
    main()