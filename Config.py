import os
import sys
import configparser
from Settings import *
from colorama import init, Fore, Back, Style

init(autoreset=True)

config = configparser.ConfigParser()
config.read(config_path)

os.system('cls' if os.name == 'nt' else 'clear')


def help_menu():
    print(Fore.GREEN + """
Available commands:
- exit()    : Exit the console
- set_res : Set Resolution for window
- build 'name project' : Build Your Project
""")


config_file = open(config_path, 'w')


def console():
    print(Fore.CYAN + "Engine Command.")
    help_menu()

    while True:
        command = input(Fore.YELLOW + ">>> ")

        if command.lower() == 'exit()':
            print(Fore.RED + "Exiting...")
            sys.exit()

        if command.lower() == 'set_res':
            current_res_x = config.getint('Window', 'win_res_x')
            current_res_y = config.getint('Window', 'win_res_y')
            print(Fore.BLUE +
                  f"Current Resolution: {current_res_x}x{current_res_y}")

            set_res = input(
                Fore.MAGENTA + f'Change Resolution (e.g : 1300x700): ')
            try:
                width, height = set_res.split('x')

                width = int(width)
                height = int(height)

                config['Window']['win_res_x'] = str(width)
                config['Window']['win_res_y'] = str(height)
                config.write(config_file)

                print(Fore.GREEN + f"Resolution updated to {width}x{height}\n")
            except ValueError:
                print(
                    Fore.RED + "Error: Invalid resolution format! Please enter in 'widthxheight' format (e.g. 1000x700).\n")

        else:
            print(Fore.RED + f'Error: Command is not valid!\n')


if __name__ == "__main__":
    console()
