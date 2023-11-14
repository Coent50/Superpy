# Imports
import argparse
from rich.console import Console
from reports import *
from operations import *

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    pass

console = Console()

# parser to make program accessible through the CLI
parser = argparse.ArgumentParser(description="Welcome to superpy", epilog="Superpy is an inventory and sales management tool", add_help= True)
sub_parser = parser.add_subparsers(dest = "command", help="specify what operation you want superpy to perform")

# report subparser enbales the users to call a set of different report regarding the inventory/sales/revenue/profit
report_parser = sub_parser.add_parser("report", help="enables the user to select a number of different reports")
report_parser.add_argument("report_type", type=str, help="specify the type of report you want to acces", choices=['inventory','sales','product','expired','revenue','profit','monthly'])
report_parser.add_argument("-d","--date", type=str, help="specify the date on which superpy needs to report")
report_parser.add_argument("-p","--period", type=str, help="specify the year followed by the month for which you would like to access the monthly reporty")

# operation subparser enables the user to buy/sell/change inventory 
operation_parser = sub_parser.add_parser ("operation", help="enables the user to perfom a set of operations")
operation_parser.add_argument("operation_type", type=str, help= "specify the type of operation", choices= ['buy', 'sell', 'change', 'delete', 'obsolete'])
operation_parser.add_argument("-pn","--product_name", type=str, help="specify the name of the product")
operation_parser.add_argument("-bp","--buy_price", type=float, help="specify the price for which the product is bought as a float (decimal number)")
operation_parser.add_argument("-sp","--sell_price", type=float, help="specify the price for which the product is sold as a float (decimal number)")
operation_parser.add_argument("-ed","--expiration_date", type=str, help="specify the experation date of the product")
operation_parser.add_argument("--id", type=int,help= "specify the id number")
operation_parser.add_argument("-bd","--buy_date", type=str,help= "specify the date on which the item was bought")

#time subparser enables the user to set and advance the internal date of superpy 
time_parser = sub_parser.add_parser("time", help="enables the user to set and advance the time")
time_parser.add_argument("time_operation", type=str, help="specify what you want to do with the time", choices= ['set','advance','current'])
time_parser.add_argument("-d","--date", type=str, help= "please specify to which date you want to set the time in the following format YYYY-MM-DD")
time_parser.add_argument ("-ds","--days", type=int, help="specify the amount of days by which you want to advance the time")



args = parser.parse_args()

# if statments related to the report subparser after choosing report the users has to specify what report they would like to see
if args.command == "report":
    if args.report_type == "inventory": 
        outcome = inventory_report(args.date)
    if args.report_type == "sales": 
        outcome = sales_report(args.date)
    if args.report_type == "product": 
        outcome = product_report()
    if args.report_type == "expired": 
        outcome = expired_report()
    if args.report_type == "revenue":  
        outcome = revenue_report(args.date)
    if args.report_type == "profit": 
        outcome = profit_report(args.date)
    if args.report_type == "monthly":
        outcome = monthly_report(args.period) 
        console.print(f"[bold green]Your report was created succesfully and has been stored in the current working directory")

# if statements related to operation subparser users have to choose the operation they want to perfom 
# There are also several optional arguments that can be used based on the type of operation you want to perform
if args.command == "operation":
    if args.operation_type == "buy" and (args.product_name is None or args.buy_price is None or args.expiration_date is None):
        parser.error("For 'buy' operation, you must provide --product_name, --buy_price, and --expiration_date.")
    elif args.operation_type == "sell" and (args.product_name is None or args.sell_price is None):
        parser.error("For 'sell' operation, you must provide --product_name and --sell_price.")
    elif args.operation_type == "change" and (args.id is None or args.product_name is None or args.buy_date is None or args.buy_price is None or args.expiration_date is None):
        parser.error("For 'change' operation, you must provide --id, --product_name, --buy_date, --buy_price, and --expiration_date.")
    elif args.operation_type == "delete" and args.id is None:
        parser.error("For 'delete' operation, you must provide --id.")
    elif args.operation_type == "obsolete":
    
        pass

if args.command == "operation":
    if args.operation_type == "buy":
         outcome = buy_inventory(args.product_name, args.buy_price, args.expiration_date)
    if args.operation_type == "sell":
        outcome = sell_inventory(args.product_name, args.sell_price)
    if args.operation_type =="change":
        outcome = change_data_inventory(args.id, args.product_name, args.buy_date, args.buy_price, args.expiration_date)
        console.print(f"[bold orange]Successfully changed id[/bold orange]: {outcome}")
    if args.operation_type == "delete":
        outcome = delete_inventory(args.id)
        console.print(f"[bold red]Successfully deleted id[/bold red]: {outcome}")
    if args.operation_type =="obsolete":
        outcome = remove_obsolete_inventory()
        console.print(f"[bold blue]Successfully moved obsolete iventory to obsolete inventory ledger")

# if statements related to the time subparser
if args.command == "time":
    if args.time_operation == "set":
        outcome = set_time(args.date)
        console.print(f'[bold green] Date succesfully set to {outcome}')
    if args.time_operation == "advance":
        outcome = advance_time(args.days)
    if args.time_operation == "current":
        outcome = current_time()
        console.print(f'[bold purple] The current internal date of superpy is {outcome}')
        
if __name__ == "__main__":
    main()


