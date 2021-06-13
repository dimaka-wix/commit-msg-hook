"""
This is an commit-msg stage hook.
It is made as a custom plugin under the https://pre-commit.com
hook framework and checks if commit message matches
the chaos-hub team commit rules.
"""

import argparse
import sys

import nltk
from nltk.tokenize import word_tokenize

import string

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
try:
    nltk.data.find("taggers/averaged_perceptron_tagger")
except LookupError:
    nltk.download("averaged_perceptron_tagger")

OFF = "\033[0m"
WHITE = OFF + "\033[97m"
BLACK = OFF + "\033[30m"
RED = OFF + "\033[31m"
GREEN = OFF + "\033[32m"
YELLOW = OFF + "\033[33m"
BLUE = OFF + "\033[34m"
MAGENTA = OFF + "\033[35m"
CAYAN = OFF + "\033[36m"
DEFAULT = OFF + "\033[39m"

FILLER = OFF + "\033[;7m"
WHITEFONE = FILLER + "\033[37m"
BLACKFONE = FILLER + "\033[30m"
REDFONE = FILLER + "\033[31m"
BLUEFONE = FILLER + "\033[34m"
GREENFONE = FILLER + "\033[32m"
VIOLETFONE = FILLER + "\033[35m"
YELLOWFONE = FILLER + "\033[33m"

MIN_WORDS = 2
COMMIT_EDITMSG = ".git/COMMIT_EDITMSG"
GITHUB_LINK = "https://github.com/dimaka-wix/commit-msg-hook.git"

HINT = f"{GREEN}\n\
EXAMPLE:\n\
\tRefactor foo function in ...\n{GREEN}\n\
\t* Fix ...\n\
\t* Add ...\n\
\t* Remove ...\n{YELLOW}\n\
hint:\tto read chaos-hum team rules visit: {BLUE}{GITHUB_LINK}{OFF}\n"


def main():
    """
    Perform validations of the commit message.
    Extract arguments from command line and run the hook logic
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=str, default=COMMIT_EDITMSG,
                        help="the path of commit message file")
    args = parser.parse_args()
    msg = read_msg(args.path)
    if not msg.strip():
        print(f"ֿ{RED}error:\tcommit message can't be empty!{OFF}\n")
        sys.exit(1)
    run_hook(msg)


def read_msg(path: str) -> str:
    """
    Extract commit message content.
    Try to read the message on the given path.
    If fail, abort commit(exit nonzero), display appropriate error and hint
    Args:
        path (str): The path of the file with commit message
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
    global default_prefixes
    subj_line_errors = validate_subj_line(msg)
    body_errors = validate_body(msg)
    if subj_line_errors or body_errors:
        print(subj_line_errors + body_errors + HINT)
        sys.exit(1)
    sys.exit(0)


def validate_subj_line(msg: str) -> str:
    """
    Validate the subject line of a commit message.
    Slice subject line of commit message and validate it according to chaos-hub team commit rules
    Args:
        msg (str): The commit message
    Returns:
        str: The detected errors(empty in a case of no errors)
    """
    line = 1
    subject = msg.splitlines()[0]
    section = "subject line"
    meaningful_errors = check_meaningful(subject, line, section)
    prefix_errors = check_prefix(subject, line, section)
    imperatives_errors = check_imperative_mode(subject, line, section)
    ending_errors = check_ending(subject, line, section)
    errors = meaningful_errors + prefix_errors + imperatives_errors + ending_errors
    return errors


def validate_body(msg: str) -> str:
    """
    Validate the body of a commit message.
    Slice body of commit message and validate it according to chaos-hub team commit rules.
    Args:
        msg (str): The commit message
    Returns:
        str: The detected errors(empty in a case of no errors)
    """
    errors = ""
    if len(msg.splitlines()) > 1:
        body = msg.splitlines()[1:]
        if body[0].strip() != "":
            errors += f"{RED}error:\tseparate the subject line from the message body with a blank line{OFF}\n"
        section = "body line"
        for i in range(len(body)):
            line_msg = body[i].strip()
            if line_msg:
                line_msg = remove_bullet(line_msg)
                if line_msg:
                    meaningful_errors = check_meaningful(
                        line_msg, i + 1, section)
                    prefix_errors = check_prefix(line_msg, i + 1, section)
                    imperatives_errors = check_imperative_mode(
                        line_msg, i + 1, section)
                    ending_errors = check_ending(line_msg, i + 1, section)
                    errors += meaningful_errors + prefix_errors + imperatives_errors + ending_errors
                else:
                    errors += f"{RED}error:\tmessage required [message {section}: line {i + 1}]{OFF}\n"
    return errors


def remove_bullet(body_line: str) -> str:
    """
    Remove line bullet if exist.
    Ex: get `* Fix bugs` return `Fix bugs`.
    Args:
        body_line (str): The single line of message body.
    Returns:
        str: The message without non-alpha characters at the beginning of the line.
    """
    content = ""
    if body_line:
        for i in range(len(body_line)):
            if body_line[i].isalpha():
                content = body_line[i:]
                break
    return content


def check_meaningful(msg: str, line: int, section: str = "") -> str:
    """
    Check if a commit message less than 2 word.
    If message contains less than 2 words, generate an appropriate error message.
    Args:
        msg (str): The part of commit mesage(subject line or body).
        line (int): The line where the error occurred.
        section (str, optional): The section where the error occurred. Defaults to empty string.
    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    errors = ""
    words = msg.strip(string.punctuation)
    if len(words) < MIN_WORDS:
        errors += f"\
{RED}error:\tone-word message is not informative, add more details [message {section}: line {line}]{OFF}\n"
    return errors


def check_prefix(msg: str, line: int, section: str = "") -> str:
    """
    Check if the prefix of the message is correct casefold.
    If validation failed, generate an appropriate error message.
    Args:
        msg (str): The part of commit mesage(subject line or body).
        line (int): The line where the error occurred.
        section (str, optional): The section where the error occurred. Defaults to empty string.
    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    errors = ""
    first_word = msg.split()[0].strip(string.punctuation)
    if first_word[0].islower():
        errors += f"\
{RED}error:\tcapitalise the word {CAYAN}{first_word} {RED}[message {section}: line {line}]{OFF}\n"
    if not first_word[1:].islower():
        errors += f"{RED}error:\tthe word {CAYAN}{first_word}{RED} \
must be in letter case and not in upper or mixed case [message {section}: line {line}]{OFF}\n"
    return errors


def check_imperative_mode(msg: str, line: int, section: str = "", words_limit: int = 2) -> str:
    """
    Check the given msg for imperative mode.
    Args:
        msg (str): The part of commit mesage(subject line or body).
        line (int): The line where the error occurred.
        section (str, optional): The section where the error occurred. Defaults to empty string.
        words_limit (int, optional): Check first `words_limit - 1` words of the given message. Defaults to 2.
    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    errors = ""
    words = nltk.word_tokenize(msg)
    # VBZ : Verb, 3rd person singular present, like "adds", "writes" etc.
    # VBD : Verb, Past tense , like "added", "wrote" etc.
    # VBG : Verb, Present participle, like "adding", "writing" ect.
    for word, tag in nltk.pos_tag(["I"]+words)[1:words_limit]:
        if word.endswith("ing") or tag.startswith("VBZ") or tag.startswith("VBD") or tag.startswith("VBG"):
            errors += f"\
{RED}error:\tthe word {CAYAN}{word} {RED}must be in imperative mode [message {section}: line {line}]{OFF}\n"
    return errors


def check_ending(msg: str, line: int, section: str = "") -> str:
    """
    Check whether the message ends with a dot or not.
    If the message ends with a dot, generate an appropriate error message.
    Args:
        msg (str): The part of commit mesage(subject line or body).
        line (int): The line where the error occurred.
        section (str, optional): The section where the error occurred. Defaults to empty string.
    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    errors = ""
    if msg != msg.strip(string.punctuation):
        errors += f"\
{RED}error:\tdo not end the line with any punctuation character [message {section}: line {line}]{OFF}\n"
    return errors


if __name__ == "__main__":
    exit(main())
