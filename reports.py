import csv
from datetime import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rich.console import Console
from rich.table import Table


# This file contains the functions needed to produce various reports

def main():
    pass


def inventory_report(): # This function gives the user a report of the inventory ledger 
    console = Console()

    with open('inventory.csv', 'r', newline='') as inventory:
        reader = csv.reader(inventory)
    
        table = Table()
        header = next(reader, None)

        if header:
            table.add_column(header[0])
            table.add_column(header[1])
            table.add_column(header[2])
            table.add_column(header[3])
            table.add_column(header[4])

            for row in reader:
                table.add_row(*row)

            console.print(table)  

def sales_report(): # This function gives the user a report of the sales ledger
    console = Console()
    
    with open('sales.csv', 'r', newline='') as sales:
        reader = csv.reader(sales)
    
        table = Table()
        header = next(reader, None)

        if header:
            table.add_column(header[0])
            table.add_column(header[1])
            table.add_column(header[2])
            table.add_column(header[3])
            table.add_column(header[4])
            table.add_column(header[5])

            for row in reader:
                table.add_row(*row)

            console.print(table)
    
def product_report(): # This function gives the user a report of the inventory ledger 
    amounts = {}

    with open('inventory.csv', 'r', newline='') as inventory:
        reader = csv.DictReader(inventory)
    
        for row in reader:
            product_name = row["product_name"]
            if product_name in amounts:
                amounts[product_name] += 1
            else:
                amounts[product_name] = 1 
    
    console = Console()
    table = Table(title= "Product Report")
    table.add_column ("Product Name")
    table.add_column ("Amount")

    for product_name, amount in amounts.items():
        table.add_row(product_name, str(amount))
    console.print(table)

def expired_report(): # This function gives the user a report of the expired items in the inventory ledger 
    console = Console()
    with open('inventory.csv', 'r', newline='') as inventory:
        reader = csv.DictReader(inventory)

        date_today = date.today().strftime('%Y-%m-%d')

        expired_products = [row for row in reader if row['expiration_date']<date_today]

        if expired_products:
            table = Table(title="Expired Products")
            table.add_column("Product Name")
            table.add_column("Expiration Date")
        
            for product in expired_products:
                table.add_row(product["product_name"], product["expiration_date"])
            
            console.print(table)
        else:
            console.print(f"[bold green]There are currently no products in the inventory that have expired.")
    
def revenue_report(sell_date=None): # This function gives the user a report of the revenue 
    revenue = 0

    with open('sales.csv', 'r', newline='') as sales:
        reader = csv.DictReader(sales)

        for row in reader:
            if sell_date is None or sell_date == row["sell_date"]:
                revenue += float(row['sell_price'])

    return print(revenue)

def profit_report(sell_date=None): # This function gives the user a report on the gross profit 
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
    return print(profit)

def monthly_report(period:str):
    profit = 0 
    revenue = 0 
    cogs = 0
    obsolete_inventory = 0 
    report_period = ''

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
                report_period = datetime.strptime(sell_period,'%Y-%m').strftime('%B %Y')

    profit = revenue - cogs - obsolete_inventory
    profit_margin = round((profit/revenue) * 100, 1) if revenue != 0 else 0 

    
    report_content = f"""Dear stakeholder we are pleased to announce that {report_period} was another spectacular month. 
    Due to new negotiations with our suppliers we have realised very favourable buying prices. 
    This has led to a cost of goods sold of: {cogs}. Whilst being able to reduce buying prices, 
    we were on the other side able to squeeze more out of our customers. This has led to revenue of: {revenue}
    Because of the implementation of Superpy we have been better able to manage our inventory 
    reducing obsolete inventory to {obsolete_inventory}. All these efforts have led to a total profit of: {profit}. 
    With that we are pleased to report a gross profit margin of {profit_margin} percent."""

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


