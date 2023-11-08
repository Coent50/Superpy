import csv
from datetime import date

# This file contains the functions needed to produce various reports

def main():
    pass


def inventory_report(): # This function gives the user a report of the inventory ledger 
    with open('inventory.csv', 'r', newline='') as inventory:
        reader = csv.reader(inventory)
    
        for line in reader:
         print(line)

def sales_report(): # This function gives the user a report of the sales ledger
    with open('sales.csv', 'r', newline='') as sales:
        reader = csv.reader(sales)
    
        for line in reader:
         print(line)

def revenue_report(): # This function gives the user a report of the revenue 
     revenue = 0

     with open('sales.csv', 'r', newline='') as sales:
        reader = csv.DictReader(sales)

        for row in reader:
            revenue += float(row['sell_price'])

     return print(revenue)

def profit_report(): # This function gives the user a report of the profit 
     profit = 0 
     revenue = 0 
     cogs = 0 

     with open('sales.csv', 'r', newline='') as sales:
        reader = csv.DictReader(sales)
    
        for row in reader:
         revenue += float(row['sell_price'])
         cogs += float(row['buy_price'])

     profit = revenue - cogs
     return print(profit)

if __name__ == "__main__":
    main()


