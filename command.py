import os

from error import file_do_not_exist_error, parameters_amount_error
from submit import submit_code
from submissions import get_record_details


def run_command(cmd_raw):
    cmd = cmd_raw.split(" ")
    if cmd[0] == "submit":
        submit_problem(cmd_raw)
    elif cmd[0] == "record" or cmd[0] == "rec":
        view_score(cmd_raw)


def submit_problem(cmd_raw):
    cmd = cmd_raw.split(" ")
    if len(cmd) < 3 or len(cmd) > 4:
        print(parameters_amount_error("2 or 3"))
    else:
        # print("submit_code = ")
        # print(open(cmd[1]).read())
        if os.path.exists(cmd[1]) == False:
            print(file_do_not_exist_error(cmd[1]))
            return
        if len(cmd) == 4:
            submit_code(open(cmd[1], encoding="utf-8").read(), cmd[2], cmd[3])
        else:
            submit_code(open(cmd[1], encoding="utf-8").read(), cmd[2])


def view_score(cmd_raw):
    cmd = cmd_raw.split(" ")
    if len(cmd) != 2:
        print(parameters_amount_error("1"))
    else:
        # print("submit_code = ")
        # print(open(cmd[1]).read())
        get_record_details(cmd[1])
