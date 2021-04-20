# import color
import sys
from typing import Optional
MSG_MAX_LENGTH = 72


def main(argv: Optional[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1]
    check_commit_msg(argv)


def check_commit_msg(msg=None):
    __validate_input(msg)
    __check_msg_convention(msg)
    print(f"- commit message matches the chaos-hub commit rules!\
            ")


def show_example():
    print(f"EXAMPLE:\n\
 Z function in\
 X file from Y component\n\
 < empty line >\n\
 - Fix ... 1\n\
 - Fix ... 2\n\
 - Fix ... 3\n")


def __validate_input(input_arg):
    if input_arg is None or not input_arg:
        raise ValueError(
            f"- commit message can't be empty!")
        sys.exit(1)
    if not isinstance(input_arg, str):
        raise TypeError(
            f"- commit message must be a string!")
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
        print(f"- commit message is too long:\
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
        print(f"- capitalise the {segment}")
        show_example()
        sys.exit(1)
    if not is_valid_prefix:
        print(f"- replace {segment} prefix\
 with one of the following:\n  {prefixes}")
        show_example()
        sys.exit(1)


def __check_in_from_format(subj, segment=""):
    if "in" not in subj or "from" not in subj:
        print(f"- use in/from format in {segment}\
 to add the place where the change was made (file/component)")
        show_example()
        sys.exit(1)


def __check_ending(msg, segment=""):
    if msg.rstrip().endswith("."):
        print(f"- do not end the {segment} with a period\
                ")
        show_example()
        sys.exit(1)


def __check_body(body):
    if body[0].strip() != "":
        print(f" - separate subject from body with a blank line\
                ")
        show_example()
        sys.exit(1)
    segment = "message body lines"
    for row in body[1:]:
        row = row.strip()
        row = row[1:].lstrip() if row[0] == "-" else row
        __check_prefix(row, segment)
        __check_ending(row, segment)


if __name__ == "__main__":
    msg = "Add a in b from c\n\n - Fix a"
    main(msg)
