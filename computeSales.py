from os import system, name

# Constants for messages
MENU = "Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program)"
INVALID_OPTION = "invalidOption"
ASK_AFM = "Give the AFM: "
ASK_PRODUCT = "Give the product name: "
ASK_INPUT = "Give name/path to input file: "

def is_valid_afm(afm):
    try:
        int(afm)
        return len(afm) == 9 and "-" not in afm
    except ValueError:
        return False

# function adopted from https://www.geeksforgeeks.org/clear-screen-python/
def clear_console():
    # for windows 
    if name == 'nt': 
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

class MenuSwitcher(object):
    def call_chosen_method(self, choice):
        chosen_option = 'option_' + str(choice)
        option = getattr(self, chosen_option, lambda: None)
        return option()

    def option_1(self):
        input_file = input(ASK_INPUT)

    def option_2(self):
        product_name = input(ASK_PRODUCT)

    def option_3(self):
        afm = input(ASK_AFM)
        if is_valid_afm(afm):
            return "Placeholder for valid afm"

    def option_4(self):
        exit()

# main function
def run_app():
    while True:
        choice = input(MENU)
        switcher = MenuSwitcher()
        result = switcher.call_chosen_method(choice)
        if result != None:
            print(result)

run_app()