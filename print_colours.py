# -*- coding: utf-8 -*-

# @Time    : 2019/1/1 19:07
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : print_colours.py

from colorama import Fore, Back, Style


def print_green(s):
    print(Fore.GREEN + str(s) + Style.RESET_ALL)


def print_red(s):
    print(Fore.RED + str(s) + Style.RESET_ALL)


def print_yellow(s):
    print(Fore.YELLOW + str(s) + Style.RESET_ALL)


def print_blue(s):
    print(Fore.BLUE + str(s) + Style.RESET_ALL)
