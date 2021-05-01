"""Resources Controller Module"""
__docformat__ = "numpy"

import argparse
import webbrowser
from typing import List
from prompt_toolkit.completion import NestedCompleter
from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.helper_funcs import get_flair
from gamestonk_terminal.menu import session


class ResourcesController:
    """Resources Controller class"""

    # Command choices
    CHOICES = [
        "help",
        "q",
        "quit",
        "hfletters",
    ]

    def __init__(self):
        """Constructor"""
        self.rsrc_parser = argparse.ArgumentParser(add_help=False, prog="rsrc")
        self.rsrc_parser.add_argument(
            "cmd",
            choices=self.CHOICES,
        )

    @staticmethod
    def print_help():
        """Print help"""

        print("\nResources:")
        print("   help          show this behavioural analysis menu again")
        print("   q             quit this menu, and shows back to main menu")
        print("   quit          quit to abandon program")
        print("")
        print("   hfletters     hedge fund letters or reports")
        print("")

    def switch(self, an_input: str):
        """Process and dispatch input

        Returns
        -------
        True, False or None
            False - quit the menu
            True - quit the program
            None - continue in the menu
        """
        (known_args, other_args) = self.rsrc_parser.parse_known_args(an_input.split())

        return getattr(
            self, "call_" + known_args.cmd, lambda: "Command not recognized!"
        )(other_args)

    def call_help(self, _):
        """Process Help command"""
        self.print_help()

    def call_q(self, _):
        """Process Q command - quit the menu"""
        return False

    def call_quit(self, _):
        """Process Quit command - quit the program"""
        return True

    def call_hfletters(self, other_args: List[str]):
        """Process hfletters command"""
        if other_args:
            print(f"The following args were unexpected: {other_args}")
        webbrowser.open(f"https://miltonfmr.com/hedge-fund-letters/")
        print("")


def menu():
    """Resources Menu"""

    rsrc_controller = ResourcesController()
    rsrc_controller.call_help(None)

    while True:
        # Get input command from user
        if session and gtff.USE_PROMPT_TOOLKIT:
            completer = NestedCompleter.from_nested_dict(
                {c: None for c in rsrc_controller.CHOICES}
            )
            an_input = session.prompt(
                f"{get_flair()} (rsrc)> ",
                completer=completer,
            )
        else:
            an_input = input(f"{get_flair()} (rsrc)> ")

        try:
            process_input = rsrc_controller.switch(an_input)

            if process_input is not None:
                return process_input

        except SystemExit:
            print("The command selected doesn't exist\n")
            continue
