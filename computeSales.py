from os import system, name

# function adopted from https://www.geeksforgeeks.org/clear-screen-python/
def clear_console():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

# main function
def run_app():
    while True:
        menu = "Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program)"
        choice = input(menu)
        switcher = MenuSwitcher()
        switcher.call_chosen_method(choice)

# Switcher class adopted from https://jaxenter.com/implement-switch-case-statement-python-138315.html
class MenuSwitcher(object):
    def call_chosen_method(self, choice):
        chosen_option = 'option_' + str(choice)
        option = getattr(self, chosen_option, lambda: "0")
        return option()

    def option_4(self):
        exit()

run_app()