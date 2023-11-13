import csv
from datetime import *
#importing the needed functions and variables from Reportlab
from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas
#importinjg the needed functions/classes from Rich 
from rich.console import Console 
from rich.table import Table
# This file contains the functions needed to produce various reports

def main():
    pass

with open('time.txt', 'r') as time: #opening the time.txt file to make the internal time of Superpy available to the functions
        current_date = time.readline()

# This function gives the user a report of the inventory ledger.
def inventory_report(buy_date=None): #Buy_date is set to None so all items in the iventory are shown if no date is specified
    console = Console()

    with open('inventory.csv', 'r', newline='') as inventory: #opening the inventory CSV to read its contents
        reader = csv.DictReader(inventory)
    
    # using rich to make a table 
        table = Table(title="[bold green]Inventory Report")
    
        table.add_column("ID")
        table.add_column("Product Name")
        table.add_column("Buy Date")
        table.add_column("Buy Price")
        table.add_column("Expiration Date")

        for row in reader:
            if buy_date is None or buy_date >= row['buy_date']:
                table.add_row(row['id'],
                    row['product_name'],
                    row['buy_date'],
                    row['buy_price'],
                    row['expiration_date'])

        console.print(table)  

# This function gives the user a report of the sales ledger
def sales_report(sell_date=None): #Sell_date=None for the same reason as with the inventory function 
    console = Console()
    
    with open('sales.csv', 'r', newline='') as sales:
        reader = csv.DictReader(sales)
        
        table = Table(title="[bold blue]Sales Report") # using rich to make a table
        table.add_column("Sales ID")
        table.add_column("Inventory ID")
        table.add_column("Product Name")
        table.add_column("Sell Date")
        table.add_column("Sell Price")
        table.add_column("Buy Price")

        for row in reader:
            if sell_date is None or sell_date >= row["sell_date"]:
             table.add_row(row['sales_id'],
                    row['inventory_id'],
                    row['product_name'],
                    row['sell_date'],
                    row['sell_price'],
                    row['buy_price'])

        console.print(table)
    
def product_report(): # This function gives the user a report of the inventory ledger 
    amounts = {}
    console = Console()
    with open('inventory.csv', 'r', newline='') as inventory:
        reader = csv.DictReader(inventory)
    
        for row in reader:
            product_name = row["product_name"]
            if product_name in amounts:
                amounts[product_name] += 1
            else:
                amounts[product_name] = 1 
    
    table = Table(title= "[bold green]Product Report") # using rich to make a table
    table.add_column ("Product Name")
    table.add_column ("Amount")

    for product_name, amount in amounts.items():
        table.add_row(product_name, str(amount))
    console.print(table)

def expired_report(): # This function gives the user a report of the expired items in the inventory ledger 
    console = Console()
    with open('inventory.csv', 'r', newline='') as inventory:
        reader = csv.DictReader(inventory)

        expired_products = [row for row in reader if row['expiration_date']< current_date]

        if expired_products:
            table = Table(title="[bold red]Expired Products") # using rich to make a table
            table.add_column("Product Name")
            table.add_column("Expiration Date")
        
            for product in expired_products:
                table.add_row(product["product_name"], product["expiration_date"])
            
            console.print(table)
        else:
            console.print(f"[bold green]There are currently no products in the inventory that have expired.")
    
def revenue_report(sell_date=None): # This function gives the user a report of the revenue 
    console = Console()
    revenue = 0

    with open('sales.csv', 'r', newline='') as sales:
        reader = csv.DictReader(sales)

        for row in reader:
            if sell_date is None or sell_date == row["sell_date"]:
                revenue += float(row['sell_price'])

    if sell_date is not None: console.print(f'The revenue on {sell_date} is: {revenue}')
    else: console.print(f'The total current revenue is: {revenue}')

def profit_report(sell_date=None): # This function gives the user a report on the gross profit 
    console = Console()
    profit = 0 
    revenue = 0 
    cogs = 0 

    with open('sales.csv', 'r', newline='') as sales:
        reader = csv.DictReader(sales)
    
        for row in reader:
            if sell_date is None or sell_date == row["sell_date"]:
                revenue += float(row['sell_price'])
                cogs += float(row['buy_price'])

    profit = revenue - cogs
    if sell_date is not None: console.print(f'The profit on {sell_date} is: {profit}')
    else: console.print(f'The total current profit is: {profit}')

def monthly_report(period:str):
    profit = 0 
    revenue = 0 
    cogs = 0
    obsolete_inventory = 0
    report_period = '' #setting report_period as an empty string in other to change it according to input period

    # calculating the cost of obsolete inventory 
    with open('obsolete_inventory.csv', 'r', newline='') as obs:
        obs_reader = csv.DictReader(obs)
        
        for row in obs_reader:
            if period == row['period']:
                obsolete_inventory += float (row['buy_price'])

    with open('sales.csv', 'r', newline='') as sales:
        sales_reader = csv.DictReader(sales)

        for row in sales_reader:
            sell_date = row["sell_date"]
            sell_period = sell_date[:7] #slicing the str of sell date to only get the year and month 
            if period == sell_period:
                revenue += float(row['sell_price'])
                cogs += float(row['buy_price'])
                report_period = datetime.strptime(sell_period,'%Y-%m').strftime('%B %Y') #transforming the report period to make for better readability in the PDF file

    profit = revenue - cogs - round(obsolete_inventory,1)
    profit_margin = round((profit/revenue) * 100, 1) if revenue != 0 else 0 #calculating profit margin only if revenue is not equal to 0, to eliominate 0 devision error

    
    report_content = f"""Dear stakeholder we are pleased to announce that {report_period} was another spectacular month. 
    Due to new negotiations with our suppliers we have realised very favourable buying prices. 
    This has led to a cost of goods sold of: {cogs}. Whilst being able to reduce buying prices, 
    we were on the other side able to squeeze more out of our customers. This has led to revenue of: {revenue}
    Because of the implementation of Superpy we have been better able to manage our inventory 
    reducing the cost of obsolete inventory to {round(obsolete_inventory,1 )}. All these efforts have led to a total profit of: {profit}. 
    With that we are pleased to report a gross profit margin of {profit_margin} percent."""

    # the section below uses Reportlab to write the lines from report_content to a pdf file and titles it according to the selected period
    lines = report_content.split('\n')
    report = canvas.Canvas(f"Monthly Report {report_period}.pdf", pagesize= letter)
    text = report.beginText(100, 750)
    text.setFont("Times-Roman", 12)

    for line in lines:
        text.textLine(line)

    report.drawText(text)
    report.save()
    

if __name__ == "__main__":
    main()


