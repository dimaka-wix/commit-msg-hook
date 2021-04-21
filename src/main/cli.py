import sys

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
    if argv is None:
        commit_msg_path, max_msg_length = __extract_args()
        with open(commit_msg_path, "r", encoding="utf-8") as commit_msg:
            argv = commit_msg.read()
    check_commit_msg(argv, max_msg_length)


def check_commit_msg(msg=None, max_msg_length=None):
    __validate_input(msg)
    __check_msg_parts(msg, max_msg_length)
    print(f"{GREEN}- commit message matches the chaos-hub commit rules!\
            {DEFAULT}")
    sys.exit(0)


def show_example():
    print(f"{GREENFONE}EXAMPLE:\n{GREEN}Refactor{BLUE}\
 Z function {GREEN}in{BLUE}\
 X file {GREEN}from {BLUE}Y component\n\
 < empty line >\n\
 -{GREEN} Fix {BLUE}... 1\n\
 -{GREEN} Add {BLUE}... 2\n\
 -{GREEN} Remove {BLUE}... 3\n{DEFAULT}")


def __extract_args():
    max_msg_length = MAX_MSG_LENGTH
    commit_msg_path = sys.argv[1]
    if len(sys.argv) > 2:
        commit_msg_path = sys.argv[2]
        max_msg_length = int(sys.argv[1].split(sep="=")[1])

    return commit_msg_path, max_msg_length


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
                                               "Rename ", "Merge "))
    prefixes = ["Fix", "Add", "Refactor", "Update", "Remove",
                "Release", "Move", "Tslint", "Rename", "Merge"]
    if msg[0].islower():
        print(f"{RED}- capitalise the {segment}!{DEFAULT}")
        show_example()
        sys.exit(1)
    if not is_valid_prefix:
        print(f"{RED}- replace {segment} prefix\
 with one of the following:\n  {prefixes}{DEFAULT}")
        show_example()
        sys.exit(1)


def __check_in_from_format(subj, segment=""):
    if "in" not in subj or "from" not in subj:
        print(f"{RED}- use {GREEN}in/from {RED}format in {segment}\
 to add the place where the change was made (file/component)!{DEFAULT}")
        show_example()
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
        show_example()
        sys.exit(1)
    segment = "message body lines"
    for row in body[1:]:
        row = row.strip()
        row = row[1:].lstrip() if row[0] == "-" else row
        __check_content(row, segment)
        __check_prefix(row, segment)
        __check_ending(row, segment)


if __name__ == "__main__":
    main("Rename ")
