import re

# Constants for messages
MENU = "Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program)"
ASK_AFM = "Give the AFM: "
ASK_PRODUCT = "Give the product name: "
ASK_INPUT = "Give name/path to input file: "

class StatsHandler(object):
    def __init__(self):
        # data structures for total sales per product/AFM
        self.product_per_afm_sales = {}
        self.afm_per_product_sales = {}
    

    # functions for updating data structures
    def update_stats(self, receipt):
        self.update_product_per_afm(receipt)
        self.update_afm_per_product(receipt)

    def update_product_per_afm(self, receipt):
        for entry in receipt.entries:
            if entry.product in self.product_per_afm_sales:
                afm_sales = self.product_per_afm_sales.get(entry.product)
                if receipt.afm in afm_sales:
                    afm_sales[receipt.afm] = str(round(float(afm_sales[receipt.afm]) + float(entry.total_price), 2))
                else:
                    afm_sales[receipt.afm] = entry.total_price
            else:
                    afm_sales = {receipt.afm : entry.total_price}
            self.product_per_afm_sales[entry.product] = afm_sales
        
    def update_afm_per_product(self, receipt):
        for entry in receipt.entries:
            if receipt.afm in self.afm_per_product_sales:
                product_sales = self.afm_per_product_sales.get(receipt.afm)
                if entry.product in product_sales:
                    product_sales[entry.product] = str(round(float(product_sales[entry.product]) + float(entry.total_price), 2))
                else:
                    product_sales[entry.product] = entry.total_price
            else:
                    product_sales = {entry.product : entry.total_price}
            self.afm_per_product_sales[receipt.afm] = product_sales

    # functions for preparing output
    def afm_to_string(self, product):
        afm_sales = self.product_per_afm_sales.get(product)
        if afm_sales:
            return "\n".join('{} {:.2f}'.format(afm, float(total_price)) for afm, total_price in sorted(afm_sales.items()))

    def product_to_string(self, afm):
        product_sales = self.afm_per_product_sales.get(afm)
        if product_sales:
            return "\n".join('{} {:.2f}'.format(product, float(total_price)) for product, total_price in sorted(product_sales.items()))

# model classes for parsing input files
class Receipt(object):
    def __init__(self, afm):
        self.total_price = 0.00
        self.entries = []
        self.afm = afm
        
    def add_entry(self, receipt_entry):
        self.entries.append(receipt_entry)
        self.total_price = round(self.total_price + float(receipt_entry.total_price), 2)

    def has_correct_total(self, total_price):
        return self.total_price == float(total_price)
class ReceiptEntry(object):
    def __init__(self, product, amount, unit_price, total_price):
        self.product = product
        self.amount = amount
        self.unit_price = unit_price
        self.total_price = total_price

    def has_correct_total(self):
        try:
            return float(self.total_price) ==  round(float(self.unit_price) * float(self.amount), 2)
        except (OverflowError, ValueError):
            return False
    

def is_valid_afm(afm):
    try:
        int(afm)
        return len(afm) == 10 and "-" not in afm
    except ValueError:
        return False

class ReceiptParser(object):
    # Receipt parser states
    NOT_INITIALIZED = "not_initialized"
    INITIALIZED = "initialized"
    INVALID = "invalid"
    AFM_PROVIDED = "afm_provided"
    ENTRY_PROVIDED = "entry_provided"
    TOTAL_PROVIDED = "total_provided"
    COMPLETED = "completed"

    def __init__(self):
        self.state = self.NOT_INITIALIZED
        self.receipt = None

    def get_receipt(self):
        if self.state == self.COMPLETED:
            return self.receipt

    def update_not_initialized(self, line):
        if re.search("^-+$", line):
            self.state = self.INITIALIZED
 
    def update_initialized(self, line):
        if re.search(r"^ΑΦΜ:\s+\d{10}$", line):
            tokens = re.split(r"\s+", line)
            self.receipt = Receipt(tokens[1])
            self.state = self.AFM_PROVIDED
        elif not re.search("^-+$", line):
            self.state = self.INVALID
            self.receipt = None
        else:
            self.state = self.INITIALIZED
            self.receipt = None
    
    def update_completed(self, line):
        self.update_initialized(line)
    
    def update_entry_provided(self, line):
        if re.search(r"^\w+:\s+\d+\s+\d+\.\d{2}\s+\d+\.\d{2}$", line):
            tokens = re.split(r"\s+", line)
            entry = ReceiptEntry(tokens[0].strip(":").upper(), tokens[1], tokens[2], tokens[3])
            if (entry.has_correct_total()):
                self.receipt.add_entry(entry)
            else:
                self.state = self.INVALID
                self.receipt = None              
        elif re.search("^-+$", line):
            self.state = self.INITIALIZED
            self.receipt = None
        elif re.search(r"^ΣΥΝΟΛΟ:\s+\d+\.\d{2}$", line):
            tokens = re.split(r"\s+", line)
            if (self.receipt.has_correct_total(tokens[1])):
                self.state = self.TOTAL_PROVIDED
            else:
                self.state = self.INVALID
                self.receipt = None            
        else:
            self.state = self.INVALID
            self.receipt = None
    
    def update_afm_provided(self, line):
        if re.search(r"^\w+:\s+\d+\s+\d+\.\d{2}\s+\d+\.\d{2}$", line):
            tokens = re.split(r"\s+", line)
            entry = ReceiptEntry(tokens[0].strip(":").upper(), tokens[1], tokens[2], tokens[3])
            if (entry.has_correct_total()):
                self.receipt.add_entry(entry)
                self.state = self.ENTRY_PROVIDED
            else:
                self.state = self.INVALID
                self.receipt = None              
        elif re.search("^-+$", line):
            self.state = self.INITIALIZED
            self.receipt = None
        else:
            self.state = self.INVALID
            self.receipt = None
    
    def update_total_provided(self, line):
        if re.search("^-+$", line):
            self.state = self.COMPLETED
        else:
            self.state = self.INVALID
            self.receipt = None
    
    def update_invalid(self, line):
        if re.search("^-+$", line):
            self.state = self.INITIALIZED

    def update_state(self, line):
        update_method = getattr(self, 'update_' + self.state, lambda: None)
        update_method(line)

class MenuHandler(object):
    def __init__(self, stats_handler):
        self.stats_handler = stats_handler

    def call_chosen_method(self, choice):
        option = getattr(self, 'option_' + str(choice), lambda: None)
        return option()

    # reading input file line by line
    # ReceiptParser holds information for receipt validation
    # When ReceiptParser returns a valid receipt, StatsHandler takes care
    # of updating overall data for menu options 2 and 3
    def option_1(self):
        filename = input(ASK_INPUT)
        try:
            with open(filename, 'r', encoding="utf-8") as f:
                parser = ReceiptParser()
                for line in f:
                    parser.update_state(line)
                    receipt = parser.get_receipt()
                    if (receipt):
                        self.stats_handler.update_stats(receipt)
        except (FileNotFoundError, UnicodeDecodeError, MemoryError):
            return

    def option_2(self):
        product = input(ASK_PRODUCT).upper()
        return self.stats_handler.afm_to_string(product)

    def option_3(self):
        afm = input(ASK_AFM)
        if is_valid_afm(afm):
            return self.stats_handler.product_to_string(afm)

    def option_4(self):
        exit()

# main function
def run_app():
    stats_handler = StatsHandler()
    while True:
        choice = input(MENU)
        menu = MenuHandler(stats_handler)
        result = menu.call_chosen_method(choice)
        if result:
            print(result)

run_app()