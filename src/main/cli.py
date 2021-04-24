import sys
import re

MAX_MSG_LENGTH = 72

DEFAULT = "\033[0;0m"
VIOLET = DEFAULT+'\033[35m'
BLUE = DEFAULT+'\033[34m'
CYAN = DEFAULT+'\033[36m'
GREEN = DEFAULT+'\033[32m'
YELLOW = DEFAULT+'\033[33m'
RED = DEFAULT+'\033[31m'
FILLER = '\033[;7m'
WHITE = '\033[37m'
BLACK = '\033[30m'
BLACKFONE = FILLER+'\033[30m'
WHITEFONE = FILLER+'\033[37m'
GREENFONE = FILLER+'\033[32m'
BLUEFONE = FILLER+'\033[34m'


def main(argv=None):
    """
    Entery point of the hook
    Start the main logic of the entire commit-msg hook
    Args:
        argv: the commit message to check
        sys.argv:
    If argv is None extract commit message from the file
    that was passed
    """
    max_msg_length = MAX_MSG_LENGTH
    if argv is None:
        print(f">>>>> sys.argv: {sys.argv}")
        msg_path, max_msg_length = __extract_args()
        try:
            with open(msg_path, "r", encoding="utf-8") as commit_msg:
                argv = commit_msg.read()
        except FileNotFoundError:
            print(f"{RED}ERROR: file '{msg_path}' not found!\n{YELLOW}\
HINT:  the commit message is usually saved in .git/COMMIT_EDITMSG{DEFAULT}")
            sys.exit(1)
    check_commit_msg(argv, max_msg_length)


def check_commit_msg(msg=None, max_msg_length=None):
    """
    Create slack instance.
    Args:
        slack_client: Slack - The initialize slack instance.
    Returns:
        slack: slack instance.
    """
    __validate_input(msg)
    __check_lenth(msg, max_msg_length)
    msg_rows = msg.splitlines()
    __check_subject_line(msg_rows[0])
    if len(msg_rows) > 1:
        __check_body(msg_rows[1:])
    print(f"{GREEN}- commit message matches the chaos-hub commit rules!\
            {DEFAULT}")


def show_msg_template():
    print(f"{GREENFONE}EXAMPLE:\n{GREEN}Refactor{BLUE}\
 Z function {GREEN}in{BLUE}\
 X file {GREEN}from {BLUE}Y component\n\
 < <body is optional, but if you add it, leave an empty line here> >\n\
 -{GREEN} Fix {BLUE}... 1\n\
 -{GREEN} Add {BLUE}... 2\n\
 -{GREEN} Remove {BLUE}... 3\n{DEFAULT}")


def __extract_args():
    if len(sys.argv) < 2:
        print(f"{GREEN}This hook is made as custom plugins\
 under the https://pre-commit.com hook framework\nand checks\
 if commit message matches the chaos-hub team commit rules{DEFAULT}")
        sys.exit(0)
    path = sys.argv[len(sys.argv) - 1]
    argv1 = MAX_MSG_LENGTH
    if len(sys.argv) > 2:
        argv1 = re.findall(r'\d+', sys.argv[1])
        if len(argv1) > 0:
            argv1 = int(argv1[0])
        else:
            print(f"{RED}ERROR: '{argv1}' is a wrong argument!\n{YELLOW}\
HINT:  this argument must contain a number{DEFAULT}")
            sys.exit(1)
    return path, argv1


def __validate_input(input_arg):
    if input_arg is None or not input_arg:
        print(
            f"{RED}- commit message can't be empty!{DEFAULT}")
        sys.exit(1)
    if not isinstance(input_arg, str):
        print(
            f"{RED}- commit message must be a string!{DEFAULT}")
        sys.exit(1)


def __check_msg_parts(msg, max_msg_length):
    __check_lenth(msg, max_msg_length)
    msg_rows = msg.splitlines()
    __check_subject_line(msg_rows[0])
    if len(msg_rows) > 1:
        __check_body(msg_rows[1:])


def __check_lenth(msg, msg_limit):
    msg_length = len(msg)
    if msg_length > msg_limit:
        print(f"{RED}- commit message is too long: {msg_length} > {msg_limit}\
                {DEFAULT}")
        sys.exit(1)


def __check_subject_line(subj):
    segment = "subject line"
    __check_content(subj, segment)
    __check_prefix(subj, segment)
    if "Release" not in subj and "Merge" not in subj and "Rename" not in subj:
        __check_in_from_format(subj, segment)
    __check_ending(subj, segment)


def __check_content(msg, segment=""):
    words = msg.strip().split()
    if len(words) < 2:
        print(f"{RED} - a one-word message is not informative\
 add more details in {segment}!{DEFAULT}")
        sys.exit(1)


def __check_prefix(msg, segment=""):
    is_valid_prefix = msg.lstrip().startswith(("Fix ", "Add ", "Refactor ",
                                               "Update ", "Remove ",
                                              "Release ", "Move ", "Tslint ",
                                               "Rename ", "Merge ", "Disable "))
    prefixes = ["Fix", "Add", "Refactor", "Update", "Remove",
                "Release", "Move", "Tslint", "Rename", "Merge", "Disable"]
    if msg[0].islower():
        print(f"{RED}- capitalise the {segment}!{DEFAULT}")
        show_msg_template()
        sys.exit(1)
    if not is_valid_prefix:
        print(f"{RED}- replace {segment} prefix\
 with one of the following:\n  {prefixes}{DEFAULT}")
        show_msg_template()
        sys.exit(1)


def __check_in_from_format(subj, segment=""):
    if "in" not in subj or "from" not in subj:
        print(f"{RED}- use {GREEN}in/from {RED}format in {segment}\
 to add the place where the change was made (file/component)!{DEFAULT}")
        show_msg_template()
        sys.exit(1)


def __check_ending(msg, segment=""):
    if msg.rstrip().endswith("."):
        print(f"{RED}- do not end the {segment} with a period!\
                {DEFAULT}")
        sys.exit(1)


def __check_body(body):
    if body[0].strip() != "":
        print(f"{RED} - separate subject from body with a blank line!\
                {DEFAULT}")
        show_msg_template()
        sys.exit(1)
    segment = "message body lines"
    for row in body[1:]:
        row = row.strip()
        row = row[1:].lstrip() if row[0] == "-" else row
        __check_content(row, segment)
        __check_prefix(row, segment)
        __check_ending(row, segment)


if __name__ == "__main__":
    exit(main())
