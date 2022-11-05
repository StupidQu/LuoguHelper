from colorama import *

PREFIX = Fore.RED + Style.BRIGHT + "E: " + Style.RESET_ALL

def parameters_amount_error(parm_amount):
    return PREFIX + "Requires " + Fore.CYAN + parm_amount + Fore.RESET + " parameters, but provides more or less."

def file_do_not_exist_error(file_name):
    return PREFIX + "File " +  Fore.CYAN + file_name + Fore.RESET + " doesn\'t exist."
