import os
from colorama import Fore, Style
import colorama
import config
import command

is_dev_ver = True
version = "0.0.2"


def print_copyright():
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT +
          "LuoGu Helper " + Fore.CYAN + version)
    if is_dev_ver:
        print(Fore.RED + "WARNING: " + Style.NORMAL +
              Fore.BLUE + "You are using the developing version.")
    if config.is_section_exist('account') == False:
        print(Fore.YELLOW + "E:" + Fore.RESET + " Please, set your account before submit, for more infomation, see our" + Fore.BLUE +  " github wiki.")
    print(Style.RESET_ALL)


if __name__ == "__main__":
    os.system("cls")
    colorama.init()
    print_copyright()
    run_path = os.getcwd()
    while True:
        command.run_command(input("(" + run_path + ") " +  Fore.BLUE + ">> " + Fore.RESET))

