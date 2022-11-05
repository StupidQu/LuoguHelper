import os

from error import file_do_not_exist_error, parameters_amount_error
from submit import submit_code, get_cookie
from colorama import Fore, Style
from submissions import get_record_details
import config


def run_command(cmd_raw):
    cmd = cmd_raw.split(" ")
    if cmd[0] == "submit":
        submit_problem(cmd_raw)
    elif cmd[0] == "record" or cmd[0] == "rec":
        view_score(cmd_raw)
    elif cmd[0] == "setaccount":
        set_account(cmd_raw)
    elif cmd[0] == "getcookie":
        get_cookie()
    elif cmd[0] == 'script':
        run_script(cmd[1])


def run_script(file):
    f = open(file, encoding="utf-8").read()
    exec(f)


def set_account(cmd_raw):
    cmd = cmd_raw.split(' ')
    if len(cmd) != 3:
        print(parameters_amount_error('2'))
        return
    if config.is_section_exist("account"):
        print(Fore.YELLOW + "W:" + Fore.RESET + " The account already exists, whether to overwrite?")
        ch = input()
        if (ch.lower() != 'y' and ch.lower() != 'yes'):
            return
    else:
        config.create_section("account")
    config.set_config("account", "uid", cmd[1])
    config.set_config("account", "client_id", cmd[2])


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
            rid = submit_code(open(cmd[1], encoding="utf-8").read(), cmd[2], cmd[3])
        else:
            rid = submit_code(open(cmd[1], encoding="utf-8").read(), cmd[2])
        view_score('_ ' + str(rid))

def view_score(cmd_raw):
    cmd = cmd_raw.split(" ")
    if len(cmd) != 2:
        print(parameters_amount_error("1"))
    else:
        # print("submit_code = ")
        # print(open(cmd[1]).read())
        get_record_details(cmd[1])
