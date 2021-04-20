import color
import sys
from typing import List
from typing import Optional
MSG_MAX_LENGTH = 72


def main(argv: Optional[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1]
    check_commit_msg(argv)


def check_commit_msg(msg=None):
    __validate_input(msg)
    __check_msg_convention(msg)
    print(f"{color.GREEN}- commit message matches the chaos-hub commit rules!\
            {color.RESET}")


def show_example():
    print(f"{color.GREENFONE}EXAMPLE:\n{color.GREEN}Refactor{color.BLUE}\
 Z function {color.GREEN}in{color.BLUE}\
 X file {color.GREEN}from {color.BLUE}Y component\n\
 < empty line >\n\
 -{color.GREEN} Fix {color.BLUE}... 1\n\
 -{color.GREEN} Fix {color.BLUE}... 2\n\
 -{color.GREEN} Fix {color.BLUE}... 3\n{color.RESET}")


def __validate_input(input_arg):
    if input_arg is None or not input_arg:
        raise ValueError(
            f"{color.RED}- commit message can't be empty!{color.RESET}")
        sys.exit(1)
    if not isinstance(input_arg, str):
        raise TypeError(
            f"{color.RED}- commit message must be a string!{color.RESET}")
        sys.exit(1)


def __check_msg_convention(msg):
    __check_lenth(msg, MSG_MAX_LENGTH)
    msg_rows = msg.splitlines()
    __check_subject_line(msg_rows[0])
    if len(msg_rows) > 1:
        __check_body(msg_rows[1:])


def __check_lenth(msg, delimiter):
    msg_length = len(msg)
    if msg_length > delimiter:
        print(f"{color.RED}- commit message is too long:\
                {msg_length} > {delimiter}")
        sys.exit(1)


def __check_subject_line(subj):
    segment = "subject line"
    __check_prefix(subj, segment)
    __check_in_from_format(subj, segment)
    __check_ending(subj, segment)


def __check_prefix(msg, segment=""):
    is_valid_prefix = msg.lstrip().startswith(("Fix ", "Add ", "Refactor ",
                                               "Update ", "Remove ",
                                               "Release ", "Move ", "Tslint ",
                                               "Rename ", "Merge "))
    prefixes = ["Fix", "Add", "Refactor", "Update", "Remove",
                "Release", "Move", "Tslint", "Rename", "Merge"]
    if msg[0].islower():
        print(f"{color.RED}- capitalise the {segment}{color.RESET}")
        show_example()
        sys.exit(1)
    if not is_valid_prefix:
        print(f"{color.RED}- replace {segment} prefix\
 with one of the following:\n  {prefixes}{color.RESET}")
        show_example()
        sys.exit(1)


def __check_in_from_format(subj, segment=""):
    if "in" not in subj or "from" not in subj:
        print(f"{color.RED}- use {color.GREEN}in/from {color.RED}format in {segment}\
 to add the place where the change was made (file/component){color.RESET}")
        show_example()
        sys.exit(1)


def __check_ending(msg, segment=""):
    if msg.rstrip().endswith("."):
        print(f"{color.RED}- do not end the {segment} with a period\
                {color.RESET}")
        show_example()
        sys.exit(1)


def __check_body(body):
    if body[0].strip() != "":
        print(f"{color.RED} - separate subject from body with a blank line\
                {color.RESET}")
        show_example()
        sys.exit(1)
    segment = "message body lines"
    for row in body[1:]:
        row = row.strip()
        row = row[1:].lstrip() if row[0] == "-" else row
        __check_prefix(row, segment)
        __check_ending(row, segment)


if __name__ == "__main__":
    main()
