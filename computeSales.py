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
                    afm_sales[receipt.afm] += entry.total_price
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
                    product_sales[entry.product] += entry.total_price
                else:
                    product_sales[entry.product] = entry.total_price
            else:
                    product_sales = {entry.product : entry.total_price}
            self.afm_per_product_sales[receipt.afm] = product_sales

    # functions for preparing output
    def afm_to_string(self, product):
        afm_sales = self.product_per_afm_sales.get(product)
        if afm_sales:
            return "\n".join('{} {}'.format(afm, total_price) for afm, total_price in sorted(afm_sales.items()))

    def product_to_string(self, afm):
        product_sales = self.afm_per_product_sales.get(afm)
        if product_sales:
            return "\n".join('{} {}'.format(product, total_price) for product, total_price in sorted(product_sales.items()))

# model classes for parsing input files
class Receipt(object):
    def __init__(self, afm):
        self.total_price = 0.00
        self.entries = []
        self.afm = afm
        
    def add_entry(self, receipt_entry):
        self.entries.insert(receipt_entry)
        self.total_price += receipt_entry.total_price

    def has_correct_total(self, total_price):
        return self.total_price == total_price
class ReceiptEntry(object):
    def __init__(self, product, amount, unit_price, total_price):
        self.product = product
        self.amount = amount
        self.unit_price = unit_price
        self.total_price = total_price

def is_valid_afm(afm):
    try:
        int(afm)
        return len(afm) == 10 and "-" not in afm
    except ValueError:
        return False

class MenuHandler(object):
    def __init__(self, stats_handler):
        self.stats_handler = stats_handler

    def call_chosen_method(self, choice):
        chosen_option = 'option_' + str(choice)
        option = getattr(self, chosen_option, lambda: None)
        return option()

    def option_1(self):
        input_file = input(ASK_INPUT)

    def option_2(self):
        product = input(ASK_PRODUCT)
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