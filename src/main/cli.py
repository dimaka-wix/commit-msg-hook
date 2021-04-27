"""
This is an commit-msg stage hook.

It is made as a custom plugin under the https://pre-commit.com
hook framework and checks if commit message matches
the chaos-hub team commit rules.
"""

import sys
import argparse


__all__ = ["main"]
OFF = "\033[0;0m"
WHITE = '\033[37m'
BLACK = '\033[30m'
RED = '\033[31m'
BLUE = '\033[34m'
CYAN = '\033[36m'
GREEN = '\033[32m'
VIOLET = '\033[35m'
YELLOW = '\033[33m'
FILLER = '\033[;7m'
WHITEFONE = FILLER+'\033[37m'
BLACKFONE = FILLER+'\033[30m'
REDFONE = FILLER+'\033[31m'
BLUEFONE = FILLER+'\033[34m'
GREENFONE = FILLER+'\033[32m'
YELLOWFONE = FILLER+'\033[33m'

MIN_WORDS = 2
COMMIT_EDITMSG = ".git/COMMIT_EDITMSG"
GITHUB_LINK = "https://github.com/dimaka-wix/commit-msg-hook.git"
default_prefixes = ["Add ", "Change ", "Create ", "Disable ", "Fix ",
                    "Merge ", "Move ", "Refactor ", "Release ",
                    "Remove ", "Rename ", "Tslint ", "Update "]


def main():
    """
    Perform validations of the commit message.

    Extract arguments from command line and run the hook logic
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", nargs="+", type=str, default=[],
                        help=f"add new valid prefix/es to chaos-hab commit rules: {BLUE}{GITHUB_LINK}{OFF}")
    parser.add_argument("path", nargs="?", type=str, default=COMMIT_EDITMSG,
                        help="the path of commit message file")
    args = parser.parse_args()

    global default_prefixes
    default_prefixes = default_prefixes + args.prefix
    msg = read_msg(args.path)
    if not msg.strip():
        print(f"ֿ{RED}ERROR: commit message can't be empty!{OFF}\n")
        sys.exit(1)
    run_hook(msg)


def read_msg(path: str) -> str:
    """
    Get commit message content.

    Try to get the message on the given path. If fail, abort commit(exit nonzero), display appropriate error and hint.

    Args:
        path (str): The path of the file with commit message.

    Returns:
        str: The commit message.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            msg = file.read()
    except FileNotFoundError:
        print(f"\n{RED}\
ERROR: the path '{path}' not found!\n{YELLOW}\
HINT:  the commit message is usually saved in {COMMIT_EDITMSG}{OFF}\n")
        sys.exit(1)
    return msg


def run_hook(msg: str):
    """
    Run the main logic of the hook.

    If one of the validations failed, abort commit(exit nonzero), display appropriate errors and hints.
    Otherwise exit zero and allow the `git commit` command.

    Args:
        msg (str): The commit message to check.
    """
    if not is_valid_subj_line(msg) or not is_valid_body(msg):
        show_example()
        sys.exit(1)
    sys.exit(0)


def is_valid_subj_line(msg: str) -> bool:
    """
    Validate the subject line of a commit message.

    Extract subject line of commit message and validate it according to chaos-hub team commit rules.

    Args:
        msg (str): The commit message.
    Returns:
        bool: The result of the validation.
    """
    subj = msg.splitlines()[0]
    sect = "subject line"
    return is_meaningful(subj, sect) and is_valid_prefix(subj, sect) and is_valid_ending(subj, sect)


def is_valid_body(msg: str) -> bool:
    """
    Validate the body of a commit message.

    Extract body of commit message and validate it according to chaos-hub team commit rules.

    Args:
        msg (str): The commit message.
    Returns:
        bool: The result of the validation.
    """
    is_valid = True
    if len(msg.splitlines()) > 1:
        body = msg.splitlines()[1:]
        if body[0].strip() != "":
            print(f"{RED}ERROR: separate subject from body with a blank line!{OFF}\n")
            is_valid = False
        sect = "message body lines"
        for row in body[1:]:
            row = row.strip()
            row = row[1:].lstrip() if row[0] == "-" else row
            if not is_meaningful(row, sect) or not is_valid_prefix(row, sect) or not is_valid_ending(row, sect):
                is_valid = False
    return is_valid


def is_meaningful(msg: str, section="") -> bool:
    """
    Check if a commit message contains more than 1 word.

    If message contains less than 2 words, display appropriate error and continue with other checks.

    Args:
        msg (str): The part of commit mesage(subject line or body).
        section (str, optional): The section where the error occurred. Defaults to empty string.

    Returns:
        bool: The result of the validation.
    """
    is_valid = True
    words = msg.strip().split()
    # slice period at the end of the line
    words = words[:-1] if words[-1].strip() == "." else words
    if len(words) < MIN_WORDS:
        print(
            f"{RED}ERROR: one-word message is not informative, add more details to {section}!{OFF}\n")
        is_valid = False
    return is_valid


def is_valid_prefix(msg: str, section="") -> bool:
    """
    Validate the prefix of the message.

    If validation failed, display appropriate error and hint and continue with other checks.

    Args:
        msg (str): The part of commit mesage(subject line or body).
        section (str, optional): The section where the error occurred. Defaults to empty string.
    Returns:
        bool: The result of the validation.
    """
    global default_prefixes
    is_valid = True
    is_valid_prefix = msg.lstrip().startswith(tuple(default_prefixes))
    if msg[0].islower():
        print(f"{RED}ERROR: capitalise {section}!{OFF}\n")
        is_valid = False
    if not is_valid_prefix:
        nl = "...\n\t\t\t\t\t\t\t"
        print(f"{RED}\
ERROR: wrong {section} prefix!\n{YELLOW}\
HINT:  you can add new prefixes as an {BLUE}args: {YELLOW}in {BLUE}.pre-commit-config.yaml\n{YELLOW}\
       otherwise, replace prefix with one of the following options:\n{YELLOW}\
       {nl.join(default_prefixes)}...{OFF}")
        is_valid = False
    return is_valid


def is_valid_ending(msg: str, section="") -> bool:
    """
    Check whether the message ends with a dot or not.

    If the message ends with a dot display appropriate error and hint and continue validation.

    Args:
        msg (str): The part of commit mesage(subject line or body).
        section (str, optional): The section where the error occurred. Defaults to empty string.
    """
    is_valid = True
    if msg.rstrip().endswith("."):
        print(f"\n{RED}ERROR: do not end {section} with a period!{OFF}")
        is_valid = False
    return is_valid


def show_example():
    """
    Display a commit message example.

    The example follows chaos-hub team commit rules.
    """
    print(f"{GREEN}\n\
EXAMPLE:\n\
  Refactor foo function in ...\n{BLUE}\
<body is optional, adding it leave an empty line here>\n{GREEN}\
  - Fix ...\n\
  - Add ...\n\
  - Remove ... \n{YELLOW}\
HINT: to read chaos-hum team rules visit: {BLUE}{GITHUB_LINK}{OFF}\n")


if __name__ == "__main__":
    exit(main())
