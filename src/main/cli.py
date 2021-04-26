"""
This is an commit-msg stage hook.

It is made as custom plugins under the https://pre-commit.com
hook framework and checks if commit message matches
the chaos-hub team commit rules.
"""

import re
import sys

IS_EXIT_1 = False
COMMIT_EDITMSG = ".git/COMMIT_EDITMSG"
MAX_MSG_LENGTH = 72
PREFIXES = ["Add ", "Change ", "Create ", "Disable ", "Fix ",
            "Merge ", "Move ", "Refactor ", "Release ",
            "Remove ", "Rename ", "Tslint ", "Update "]

DEFAULT = "\033[0;0m"
WHITE = DEFAULT+'\033[37m'
BLACK = DEFAULT+'\033[30m'
RED = DEFAULT+'\033[31m'
BLUE = DEFAULT+'\033[34m'
CYAN = DEFAULT+'\033[36m'
GREEN = DEFAULT+'\033[32m'
VIOLET = DEFAULT+'\033[35m'
YELLOW = DEFAULT+'\033[33m'
FILLER = '\033[;7m'
WHITEFONE = FILLER+'\033[37m'
BLACKFONE = FILLER+'\033[30m'
REDFONE = DEFAULT+'\033[31m'
BLUEFONE = FILLER+'\033[34m'
GREENFONE = FILLER+'\033[32m'
YELLOWFONE = FILLER+'\033[33m'


def main(msg=None):
    """
    Entry point of commit-msg-hook.

    If `msg` argument is None,
    extract arguments from command line and run the hook logic

    Args:
        msg ([type], optional): Mainly used for testing in development.
                                Defaults to None.
    """
    if msg is None:
        msg = __get_commit_msg()
        __set_args()
    run_hook(msg)


def run_hook(msg: str):
    """
    Run the main logic of the hook.

    If one of the checks failed abort commit(exit nonzero),
    display appropriate errors and hints.
    Otherwise exit zero and allow the `commit` command

    Args:
        msg (str): The commit message to check.
    """
    global IS_EXIT_1
    __check_length(msg)
    __check_subject_line(msg)
    __check_body(msg)
    if IS_EXIT_1:
        show_example()
        sys.exit(1)
    else:
        print(f"\n{GREEN}\
CONGRATS! Commit message matches the chaos-hub commit rules 👍\n{DEFAULT}")
        sys.exit(0)


def show_example():
    """
    Display a commit message example.

    The example follows chaos-hub team commit rules.
    """
    print(f"{GREEN}\
EXAMPLE:\n\
  Refactor foo function in ...\n{BLUE}\
<body is optional, adding it leave an empty line here>\n{GREEN}\
  - Fix ...\n\
  - Add ...\n\
  - Remove ... \n{YELLOW}\
HINT:  to read chaos-hum team rules visit: {BLUE}\
https://github.com/dimaka-wix/commit-msg-hook.git \n{DEFAULT}")


def __get_commit_msg() -> str:
    """
    Extract commit message content.

    Try to extract the message on the path given in a command line.
    If fail, abort commit(exit nonzero), display appropriate error and hint.
    If there are no arguments, show information about the hook.

    Returns:
        str: The commit message.
    """
    args = sys.argv
    if len(args) < 2:
        print(f"\n{GREEN}\
This hook is made as custom plugins under the {BLUE}https://pre-commit.com \
{GREEN}hook framework\nand checks if commit message \
matches the chaos-hub team commit rules\n{YELLOW}\
HINT:  to read chaos-hum team rules visit {BLUE}\
https://github.com/dimaka-wix/commit-msg-hook.git \n{DEFAULT}")
        sys.exit(0)
    path = args[len(args) - 1]
    path = COMMIT_EDITMSG if path.upper() in COMMIT_EDITMSG else path
    try:
        with open(path, "r", encoding="utf-8") as msg:
            commit_msg = msg.read()
    except FileNotFoundError:
        print(f"\n{RED}\
ERROR: file '{path}' not found!\n{YELLOW}\
HINT:  the commit message is usually saved in {COMMIT_EDITMSG}\n{DEFAULT}")
        sys.exit(1)
    return commit_msg


def __set_args():
    """
    Set additional arguments if were passed.

    Set MAX_MSG_LENGTH and update the PREFIXES list
    according to the passed values.
    """
    global PREFIXES
    global MAX_MSG_LENGTH
    args = sys.argv
    if len(args) > 2:
        for arg in args[1:len(args)-1]:
            decimals = re.findall(r'\d+', arg)
            if len(decimals) == 0:
                arg = (arg.strip() + " ").lstrip()
                if len(arg) > 3:
                    PREFIXES.append(arg)
            else:
                MAX_MSG_LENGTH = int(decimals[0])


def __check_length(msg: str):
    """
    Check the length of a commit message.

    If the message is empty abort commit(exit nonzero) and
    display appropriate error.
    If length longer than `MAX_MSG_LENGTH`
    display appropriate error and continue with other checks.

    Args:
        msg (str): The commit message to check.
    """
    global IS_EXIT_1
    msg_length = len(msg)
    if not msg.strip():
        print(f"ֿ{RED}ERROR: commit message can't be empty!\n{DEFAULT}")
        sys.exit(1)
    if msg_length > MAX_MSG_LENGTH:
        print(f"{RED}\
ERROR: commit message is too long: {msg_length} > {MAX_MSG_LENGTH}{DEFAULT}\n")
        IS_EXIT_1 = True


def __check_subject_line(msg: str):
    """
    Check the subject line of a commit message.

    Extract subject line of commit message and
    check it according to chaos-hub team commit rules.

    Args:
        msg (str): The commit message.
    """
    subj = msg.splitlines()[0]
    segment = "subject line"
    __check_content(subj, segment)
    __check_prefix(subj, segment)
    __check_ending(subj, segment)


def __check_body(msg: str):
    """
    Check the body of a commit message.

    Extract body of commit message and
    check it according to chaos-hub team commit rules.

    Args:
        msg (str): The commit message.
    """
    global IS_EXIT_1
    if len(msg.splitlines()) > 1:
        body = msg.splitlines()[1:]
        if body[0].strip() != "":
            print(f"{RED}\
ERROR: separate subject from body with a blank line!\n{DEFAULT}")
            IS_EXIT_1 = True
        segment = "message body lines"
        for row in body[1:]:
            row = row.strip()
            row = row[1:].lstrip() if row[0] == "-" else row
            __check_content(row, segment)
            __check_prefix(row, segment)
            __check_ending(row, segment)


def __check_content(msg: str, segment=""):
    """
    Check if a commit message contains more then 1 word.

    If the message contains just 1 word
    display appropriate error and continue with other checks..

    Args:
        msg (str): The part of commit mesage(subject line or body).
        segment (str, optional): Segment to show in error message.
        Defaults to empty string.
    """
    global IS_EXIT_1
    words = msg.strip().split()
    words = words[:-1] if words[-1].strip() == "." else words
    if len(words) < 2:
        print(f"{RED}\
ERROR: one-word message is not informative, add more details to {segment}!\n\
{DEFAULT}")
        IS_EXIT_1 = True


def __check_prefix(msg: str, segment=""):
    """
    Check if a prefix of the message is valid.

    If tprefix of the message is invalid
    display appropriate error and hint and continue with other checks.

    Args:
        msg (str): The part of commit mesage(subject line or body).
        segment (str, optional): Segment to show in error message.
        Defaults to empty string.
    """
    global IS_EXIT_1
    is_valid_prefix = msg.lstrip().startswith(tuple(PREFIXES))
    if msg[0].islower():
        print(f"{RED}ERROR: capitalise {segment}!\n{DEFAULT}")
        IS_EXIT_1 = True
    if not is_valid_prefix:
        nl = "...\n       "
        print(f"{RED}\
ERROR: wrong {segment} prefix!\n{YELLOW}\
HINT:  you can add new prefixes as an {BLUE}args: {YELLOW}in {BLUE}\
.pre-commit-config.yaml\n{YELLOW}\
       otherwise, replace prefix with one of the following options:\n{YELLOW}\
       {nl.join(PREFIXES)}...{DEFAULT}\n")
        IS_EXIT_1 = True


def __check_ending(msg: str, segment=""):
    """
    Check whether the message specific part ends with a dot or not.

    If the message ends with a dot or not
    display appropriate error and hint and continue with other checks.

    Args:
        msg (str): The part of commit mesage(subject line or body).
        segment (str, optional): Segment to show in error message.
        Defaults to empty string.
    """
    global IS_EXIT_1
    if msg.rstrip().endswith("."):
        print(f"\n{RED}\
ERROR: do not end {segment} with a period!{DEFAULT}")
        IS_EXIT_1 = True


if __name__ == "__main__":
    exit(main("Add a "))
