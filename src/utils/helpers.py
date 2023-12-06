import os
import platform


def clear_console():
    # For Windows
    if platform.system() == "Windows":
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

