import csv
from datetime import *


# This file contains the functions needed to produce various reports

def main():
    pass


def inventory_report(): # This function gives the user a report of the inventory ledger 
    with open('inventory.csv', 'r', newline='') as inventory:
        reader = csv.reader(inventory)
    
        for row in reader:
         print(row)

def sales_report(): # This function gives the user a report of the sales ledger
    with open('sales.csv', 'r', newline='') as sales:
        reader = csv.reader(sales)
    
        for row in reader:
         print(row)

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

    return print(amounts)

def expired_report(): # This function gives the user a report of the expired items in the inventory ledger 

    with open('inventory.csv', 'r', newline='') as inventory:
        reader = csv.DictReader(inventory)

        date_today = date.today().strftime('%Y-%m-%d')
    
        for row in reader:
          expiration_date = row["expiration_date"]
          if expiration_date < date_today:
            print(row)
    
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

def monthly_report(month):
    profit = 0 
    revenue = 0 
    cogs = 0 

    with open('sales.csv', 'r', newline='') as sales:
        reader = csv.DictReader(sales)

        for row in reader:
            sell_date = row["sell_date"]
            sell_month = sell_date[:7] #slicing the str of sell date to only get the year and month 
            if month == sell_month:
                revenue += float(row['sell_price'])
                cogs += float(row['buy_price'])

    profit = revenue - cogs
    profit_margin = round((profit/revenue) * 100, 1) if revenue != 0 else 0 

    report_month = datetime.strptime(sell_month,'%Y-%m').strftime('%B %Y')

    report = f"""Dear stakeholder we are pleased to announce that {report_month} was another spectacular month. 
    Due to new negotiations with our suppliers we have realised very favourable buying prices. 
    This has led to a cost of goods sold of: {cogs}. Whilst being able to reduce buying prices, 
    we were on the other side able to squeeze more out of our customers. 
    This has led to revenue of: {revenue} and a profit of: {profit}. 
    With that we are pleased to report a profit margin of {profit_margin} percent."""

    return print(report)
    



if __name__ == "__main__":
    main()

monthly_report('2023-11')
