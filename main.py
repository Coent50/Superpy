# Imports
import argparse
import csv
from datetime import date
from reports import *
from operations import *

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    pass

# parser to make program accessible through the CLI
parser = argparse.ArgumentParser(description="Welcome to superpy", epilog="Superpy is an inventory and sales management tool", add_help= True)
sub_parser = parser.add_subparsers(dest = "command", help="specify what operation you want superpy to perform")

# report subparser enbales the users to call a set of different report regarding the inventory/sales/revenue/profit
report_parser = sub_parser.add_parser("report", help="enables the user to select a number of different reports")
report_parser.add_argument("report_type", type=str, help="specify the type of report you want to acces")
report_parser.add_argument("--date", type=str, help="specify the date on which superpy needs to report")

# operation subparser enables the user to buy/sell/change inventory 
operation_parser = sub_parser.add_parser ("operation", help="enables the user to perfom a set of operations")
operation_parser.add_argument("operation_type", type=str, help= "specify the type of operation")
operation_parser.add_argument("--product_name", type=str, help="specify the name of the product")
operation_parser.add_argument("--buy_price", type=float, help="specify the price for which the product is bought as a float (decimal number)")
operation_parser.add_argument("--sell_price", type=float, help="specify the price for which the product is sold as a float (decimal number)")
operation_parser.add_argument("--expiration_date", type=str, help="specify the experation date of the product")
operation_parser.add_argument("--id", type=int,help= "specify the id number")
operation_parser.add_argument("--buy_date", type=str,help= "specify the date on which the item was bought")

args = parser.parse_args()

# if statments related to the report subparser after choosing report the users has to specify what report they would like to see
if args.command == "report":
    if args.report_type == "inventory": #provides a report on all entries in the inventory ledger at a given moment
        outcome = inventory_report()
    if args.report_type == "sales": #provides a report on all entries in the sales ledger at a given moment
        outcome = sales_report()
    if args.report_type == "product": #provides a report on what products are held and how many of them are held at a given moment
        outcome = product_report()
    if args.report_type == "revenue": #provides a report on the revenue at a given moment 
        outcome = revenue_report()
    if args.report_type == "profit": #provides a report on the profit at a given moment
        outcome = profit_report()

# if statements related to operation subparser users have to choose the operatioon they want to perfom 
# There are also several optional arguments that can be used based on the type of operation you want to perform
if args.command == "operation":
    if args.operation_type == "buy":
         outcome = buy_inventory(args.product_name, args.buy_price, args.expiration_date)
    if args.operation_type == "sell":
        outcome = sell_inventory(args.product_name, args.sell_price)
    if args.operation_type =="change":
        outcome = change_data_inventory(args.id, args.product_name, args.buy_date, args.buy_price, args.expiration_date)
    if args.operation_type == "delete":
        outcome = delete_inventory(args.id)
        
if __name__ == "__main__":
    main()


