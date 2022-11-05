import os
from colorama import Fore, Style
import colorama
import command

is_dev_ver = True
version = "0.0.1"


def print_copyright():
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT +
          "LuoGu Helper " + Fore.CYAN + version)
    if is_dev_ver:
        print(Fore.RED + "WARNING: " + Style.NORMAL +
              Fore.BLUE + "You are using the developing version.")
    print(Style.RESET_ALL)


if __name__ == "__main__":
    os.system("cls")
    colorama.init()
    print_copyright()
    while True:
        command.run_command(input(Fore.BLUE + ">> " + Fore.RESET))

