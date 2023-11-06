import argparse
import csv
from datetime import date

def main():
    pass


def inventory_report(): # This function gives the user a report of the current inventory 
    with open('inventory.csv', 'r', newline='') as inventory:
        reader = csv.reader(inventory)
    
        for line in reader:
         print(line)


def change_data_inventory(id,product_name,buy_date,buy_price,expiration_date): # This function enables the user to change data in the inventory
   with open ('inventory.csv', 'r+', newline='') as inventory:
        reader = csv.DictReader(inventory)
        rows =list(reader)

        for row in rows:
            if row ["id"] == id:
                row["product_name"] = product_name
                row["buy_date"] = buy_date
                row["buy_price"] = buy_price
                row["expiration_date"] = expiration_date
            break

        inventory.seek(0)
        writer = csv.DictWriter(inventory, fieldnames= reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def buy_inventory(product_name, buy_date, buy_price, expiration_date): # This function enables the user to add new data entries to the inventory 
 
    with open('inventory.csv', 'r+', newline='') as inventory:
        reader = csv.DictReader(inventory)
        rows = list(reader)

        max_id = 0
        for row in rows: # Finds the highest id number currently in the inventory file
            if int(row["id"]) > max_id:
                max_id = int(row["id"])

        new_id = max_id + 1 # adds + 1 to the current highest id number 
        new_row = {'id': new_id, 'product_name': product_name, 'buy_date': buy_date, 'buy_price': buy_price, 'expiration_date': expiration_date}
        rows.append(new_row) # Adds a new row to the inventory based on the generated id number and the users data input regarding the product

        inventory.seek(0)
        writer = csv.DictWriter(inventory, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def sell_inventory (product_name, inventory_id, sell_date, sell_price):
        
    with open('sales.csv', 'r+', newline='') as sales:
        reader = csv.DictReader(sales)
        rows = list(reader)

        max_sales_id = 0
        for row in rows: # Finds the highest id number currently in the sales file
            if int(row["sales_id"]) > max_sales_id:
                max_sales_id = int(row["sales_id"])

    new_sales_id = max_sales_id + 1
    

if __name__ == "__main__":
    main()