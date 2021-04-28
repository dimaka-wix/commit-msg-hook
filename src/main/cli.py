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
WHITE = OFF + '\033[37m'
BLACK = OFF + '\033[30m'
RED = OFF + '\033[31m'
BLUE = OFF + '\033[34m'
CYAN = OFF + '\033[36m'
GREEN = OFF + '\033[32m'
VIOLET = OFF + '\033[35m'
YELLOW = OFF + '\033[33m'
FILLER = OFF + '\033[;7m'
WHITEFONE = FILLER + '\033[37m'
BLACKFONE = FILLER + '\033[30m'
REDFONE = FILLER + '\033[31m'
BLUEFONE = FILLER + '\033[34m'
GREENFONE = FILLER + '\033[32m'
VIOLETFONE = FILLER + '\033[35m'
YELLOWFONE = FILLER + '\033[33m'

MIN_WORDS = 2
COMMIT_EDITMSG = ".git/COMMIT_EDITMSG"
GITHUB_LINK = "https://github.com/dimaka-wix/commit-msg-hook.git"
MSG_EXAMPLE = f"{GREEN}\n\
EXAMPLE:\n{GREEN}\
\tRefactor foo function in ...\n{CYAN}\
<body is optional, adding it leave an empty line here>\n{GREEN}\
\t- Fix ...\n\
\t- Add ...\n\
\t- Remove ...\n{YELLOW}\
hint:\tto read chaos-hum team rules visit: {BLUE}{GITHUB_LINK}{OFF}\n"

default_prefixes = {"Add ", "Change ", "Create ", "Disable ", "Fix ",
                    "Merge ", "Move ", "Refactor ", "Release ",
                    "Remove ", "Rename ", "Tslint ", "Update "}


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

    # update valid prefixes pool
    global default_prefixes
    default_prefixes = default_prefixes.union(
        set(["{} ".format(pref.capitalize()) for pref in args.prefix]))
    msg = read_msg(args.path)
    if not msg.strip():
        print(f"ֿ{RED}error:\tcommit message can't be empty!{OFF}\n")
        sys.exit(1)
    run_hook(msg)


def read_msg(path: str) -> str:
    """
    Extract commit message content.

    Try to read the message on the given path.
    If fail, abort commit(exit nonzero), display appropriate error and hint.

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
error:\tthe path '{path}' not found!\n{YELLOW}\
hint:\tthe commit message is usually saved in {COMMIT_EDITMSG}{OFF}\n")
        sys.exit(1)
    return msg


def run_hook(msg: str):
    """
    Run the main logic of the hook.

    If one of the validations failed, abort commit(exit nonzero), display appropriate errors and hints.
    Otherwise exit zero and allow the `git commit` command.

    Args:
        msg (str): The commit message to validate.
    """
    subj_line_errors = validate_subj_line(msg)
    body_errors = validate_body(msg)
    if subj_line_errors or body_errors:
        print(subj_line_errors + body_errors + MSG_EXAMPLE)
        sys.exit(1)
    sys.exit(0)


def validate_subj_line(msg: str) -> str:
    """
    Validate the subject line of a commit message.

    Slice subject line of commit message and validate it according to chaos-hub team commit rules.

    Args:
        msg (str): The commit message.
    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    subject = msg.splitlines()[0]
    section = "subject line"
    meaningful_errors = check_meaningful(subject, section)
    prefix_errors = check_prefix(subject, section)
    ending_errors = check_ending(subject, section)
    errors = meaningful_errors + prefix_errors + ending_errors
    return errors


def validate_body(msg: str) -> str:
    """
    Validate the body of a commit message.

    Slice body of commit message and validate it according to chaos-hub team commit rules.

    Args:
        msg (str): The commit message.
    Returns:
        str: The detected errors(empty in a case of no errors)
    """
    errors = ""
    if len(msg.splitlines()) > 1:
        body = msg.splitlines()[1:]
        if body[0].strip() != "":
            errors += f"{RED}error:\tseparate subject from body with a blank line!{OFF}\n"
        section = "message body lines"
        for line in body:
            line = line.strip()
            if line:
                line = line[1:].lstrip() if line[0] == "-" else line
                meaningful_errors = check_meaningful(line, section)
                prefix_errors = check_prefix(line, section)
                ending_errors = check_ending(line, section)
                errors += meaningful_errors + prefix_errors + ending_errors
    return errors


def check_meaningful(msg: str, section="") -> str:
    """
    Check if a commit message less than 2 word.

    If message contains less than 2 words, generate an appropriate error message.

    Args:
        msg (str): The part of commit mesage(subject line or body).
        section (str, optional): The section where the error occurred. Defaults to empty string.

    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    errors = ""
    words = msg.strip().split()
    # slice period at the end of the line
    words = words[:-1] if words[-1].strip() == "." else words
    if len(words) < MIN_WORDS:
        errors += f"{RED}error:\tone-word message is not informative, add more details to {section}!{OFF}\n"
    return errors


def check_prefix(msg: str, section="") -> str:
    """
    Validate the prefix of the message.

    If validation failed, generate an appropriate error message and a hint.

    Args:
        msg (str): The part of commit mesage(subject line or body).
        section (str, optional): The section where the error occurred. Defaults to empty string.
    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    global default_prefixes
    errors = ""
    is_valid_prefix = msg.lstrip().startswith(tuple(default_prefixes))
    if msg[0].islower():
        errors += f"{RED}error:\tcapitalise {section}!{OFF}\n"
    if not is_valid_prefix:
        delimiter = "...\n\t"
        errors += f"{RED}\
error:\twrong {section} prefix!\n{YELLOW}\
hint:\tyou can add new prefixes as an {CYAN}args: {YELLOW}in {CYAN}.pre-commit-config.yaml\n{YELLOW}\
\totherwise, replace prefix with one of the following options:\n{CYAN}\
\t{delimiter.join(default_prefixes)}...{OFF}\n"
    return errors


def check_ending(msg: str, section="") -> str:
    """
    Check whether the message ends with a dot or not.

    If the message ends with a dot, generate an appropriate error message.

    Args:
        msg (str): The part of commit mesage(subject line or body).
        section (str, optional): The section where the error occurred. Defaults to empty string.
    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    errors = ""
    if msg.rstrip().endswith("."):
        errors += f"{RED}error:\tdo not end {section} with a period!{OFF}\n"
    return errors


if __name__ == "__main__":
    exit(main())
