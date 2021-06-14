"""This is an commit-msg stage hook.

It is made as a custom plugin under the https://pre-commit.com
hook framework and checks if commit message matches
the chaos-hub team commit rules.
"""

import argparse
import sys

import nltk

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
ITALIC = "\033[3m"
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
GITHUB_LINK = "https://github.com/dimaka-wix/commit-msg-hook/blob/main/README.md#commit-rules"

HINT = f"\n{YELLOW}hint:\tto read chaos-hum team rules visit:  {BLUE}{GITHUB_LINK}{OFF}\n"


def main():
    """Perform validations of the commit message.

    Extract arguments from command line and run the hook logic
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=str, default=COMMIT_EDITMSG,
                        help="the path of commit message file")
    args = parser.parse_args()
    msg = read_msg(args.path)
    if not msg.strip():
        print(f"ֿ\n{RED}error:\tcommit message can't be empty{OFF}\n")
        sys.exit(1)
    run_hook(msg)


def read_msg(path: str) -> str:
    """Extract commit message content.

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
error:\tthe path  {CAYAN}{path}  not found!\n{YELLOW}\
hint:\tthe commit message is usually saved in  {CAYAN}{COMMIT_EDITMSG}{OFF}\n")
        sys.exit(1)
    return msg


def run_hook(msg: str):
    """Run the main logic of the hook.

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
    """Validate the subject line of a commit message.

    Slice subject line of commit message and validate it according to chaos-hub team commit rules

    Args:
        msg (str): The commit message

    Returns:
        str: The detected errors(empty in a case of no errors)
    """
    line = 1
    subject = msg.splitlines()[0]
    section = "subject"
    meaningful_errors = check_meaningful(subject)
    prefix_errors = check_prefix(subject)
    imperatives_errors = check_for_imperative(subject)
    ending_errors = check_ending(subject)
    errors = meaningful_errors + prefix_errors + imperatives_errors + ending_errors
    return errors


def validate_body(msg: str) -> str:
    """Validate the body of a commit message.

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
            errors += f"\n{RED}error:\tseparate the subject line from the message body with a blank line{OFF}\n"
        for i in range(len(body)):
            line_msg = body[i].strip()
            if line_msg:
                line_msg = remove_bullet(line_msg)
                if line_msg:
                    meaningful_errors = check_meaningful(line_msg)
                    prefix_errors = check_prefix(line_msg)
                    imperatives_errors = check_for_imperative(line_msg)
                    ending_errors = check_ending(line_msg)
                    errors += meaningful_errors + prefix_errors + imperatives_errors + ending_errors
                else:
                    errors += f"\n{RED}error:\tthe message body can't be empty{OFF}\n"
    return errors


def remove_bullet(body_line: str) -> str:
    """Remove line bullet if exist.

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


def check_meaningful(msg: str) -> str:
    """Check if a commit message less than 2 word.

    If message contains less than 2 words, generate an appropriate error message.

    Args:
        msg (str): The part of commit mesage(subject line or body).

    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    errors = ""
    words = msg.strip(string.punctuation).split()
    if len(words) < MIN_WORDS:
        errors += f"\n{RED}\
error:\tone-word message  {GREEN}{ITALIC}{words[0]}{RED}  is not informative, please add more details{OFF}\n"
    return errors


def check_prefix(msg: str) -> str:
    """Check if the prefix of the message is correct casefold.

    If validation failed, generate an appropriate error message.

    Args:
        msg (str): The part of commit mesage(subject line or body).

    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    errors = ""
    first_word = msg.split()[0].strip(string.punctuation)
    if first_word[0].islower():
        errors += f"\n{RED}error:\tcapitalise the word  {GREEN}{ITALIC}{first_word}{OFF}\n"
    if not first_word[1:].islower():
        errors += f"\n{RED}\
error:\tthe word  {GREEN}{ITALIC}{first_word}{RED}  must be in letter case and not uppercase or mixed{OFF}\n"
    return errors


def check_for_imperative(msg: str, words_limit: int = 2) -> str:
    """Check the given msg for imperative mood.

    Args:
        msg (str): The part of commit mesage(subject line or body).
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
            errors += f"\n{RED}\
error:\tthe word  {GREEN}{ITALIC}{word}{RED}  must be in imperative mood{OFF}\n"
    return errors


def check_ending(msg: str) -> str:
    """Check whether the message ends with a dot or not.

    If the message ends with a dot, generate an appropriate error message.

    Args:
        msg (str): The part of commit mesage(subject line or body).

    Returns:
        str: The detected errors(empty in a case of no errors).
    """
    errors = ""
    if msg != msg.strip(string.punctuation):
        errors += f"\n{RED}\
error:\tdo not end the line  {GREEN}{ITALIC}{msg}{RED}  with any punctuation character{OFF}\n"
    return errors


if __name__ == "__main__":
    exit(main())
