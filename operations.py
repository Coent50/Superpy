import csv
from datetime import *

#This file contains the functions needed to perfom various operational activities

def main():
    pass

def buy_inventory(product_name,buy_price, expiration_date): # This function enables the user to add new data entries to the inventory 
 
    with open('inventory.csv', 'r+', newline='') as inventory:
        reader = csv.DictReader(inventory)
        rows = list(reader)

        buy_date = date.today().strftime('%Y-%m-%d')

        # Finding the highest id currently in the inventory ledger
        max_id = 0
        for row in rows: 
            if int(row["id"]) > max_id:
                max_id = int(row["id"])

        new_id = max_id + 1 # adds + 1 to the current highest id number 
        new_row = {'id': new_id, 'product_name': product_name, 'buy_date': buy_date, 'buy_price': buy_price, 'expiration_date': expiration_date}
        rows.append(new_row) # Adds a new row to the inventory based on the generated id number and the users data input regarding the product

        inventory.seek(0)
        writer = csv.DictWriter(inventory, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return product_name

def sell_inventory(product_name, sell_price): # this function allows the user to sell inventory and moves the product to the sales ledger
    with open('sales.csv', 'r+', newline='') as sales:
        sales_reader = csv.DictReader(sales)
        sales_rows = list(sales_reader)

        # Finding the highest sales-id currently in the sales ledger
        max_sales_id = 0
        for row in sales_rows: 
            if int(row["sales_id"]) > max_sales_id:
                max_sales_id = int(row["sales_id"])
        new_sales_id = max_sales_id + 1

        sell_date = date.today().strftime('%Y-%m-%d') #sets the sell date to the date on which the sale is executed

        sold_item = False
        with open('inventory.csv', 'r+', newline='') as inventory:
            inventory_reader = csv.DictReader(inventory)
            inventory_rows = list(inventory_reader)

            inventory_rows_updated =[]

            in_stock = False
            for row in inventory_rows:
                if row["product_name"] == product_name and not sold_item:
                    in_stock = True
                    expiration_date = row["expiration_date"]
                    expired = expiration_date < sell_date

                    if not expired:
                     inventory_id = row["id"]
                     buy_price = row["buy_price"]
                     new_row = {'sales_id': new_sales_id,'inventory_id': inventory_id, 'product_name': product_name, 'sell_date': sell_date, 'sell_price' : sell_price, 'buy_price': buy_price,}
                     sales_rows.append(new_row)
                     sold_item = True
                else:
                    inventory_rows_updated.append(row)

            if not in_stock:
                print("ERROR: This product is out of stock")
            elif not sold_item:
                print("ERROR: This product has expired and can therefore not be sold")
            else:
             sales.seek(0)
             sales_writer = csv.DictWriter(sales, fieldnames=sales_reader.fieldnames)
             sales_writer.writeheader()
             sales_writer.writerows(sales_rows)

             inventory.seek(0)
             inventory_writer = csv.DictWriter(inventory, fieldnames=inventory_reader.fieldnames)
             inventory_writer.writeheader()
             inventory_writer.writerows(inventory_rows_updated)
             inventory.truncate() #truncate method clears the file from any old data making sure only the updated entry is included in the inventory 

    return product_name

def remove_obsolete_inventory():
    with open('obsolete_inventory.csv', 'r+', newline='') as obs:
        obs_reader = csv.DictReader(obs)
        obs_rows = list(obs_reader)

        today = date.today().strftime('%Y-%m-%d') 
        period = today[:7]

        with open('inventory.csv', 'r+', newline='') as inventory:
            inventory_reader = csv.DictReader(inventory)
            inventory_rows = list(inventory_reader)

            inventory_rows_updated =[]

            for row in inventory_rows:
                    expiration_date = row["expiration_date"]
                    expired = expiration_date < today

                    if expired:
                     inventory_id = row["id"]
                     product_name = row ["product_name"]
                     buy_price = row["buy_price"]
                     new_row = {'inventory_id': inventory_id, 'product_name': product_name,'period': period,'buy_price': buy_price, 'expiration_date' : expiration_date}
                     obs_rows.append(new_row)
                    else:
                     inventory_rows_updated.append(row)

            obs.seek(0)
            obs_writer = csv.DictWriter(obs, fieldnames=obs_reader.fieldnames)
            obs_writer.writeheader()
            obs_writer.writerows(obs_rows)

            inventory.seek(0)
            inventory_writer = csv.DictWriter(inventory, fieldnames=inventory_reader.fieldnames)
            inventory_writer.writeheader()
            inventory_writer.writerows(inventory_rows_updated)
            inventory.truncate()

def change_data_inventory(id,product_name,buy_date,buy_price,expiration_date): # This function enables the user to change data in the inventory
    id = str(id)
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
    return id

def delete_inventory(id):
    id =str(id)
    with open('inventory.csv', 'r+', newline='') as inventory:
        reader = csv.DictReader(inventory)
        rows = list(reader)
        
        inventory.seek(0)
        writer = csv.DictWriter(inventory, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in rows:
            if row["id"] != id:
                writer.writerow(row)

        inventory.truncate() #truncate method clears the file from any old data making sure only the updated entry is included in the inventory 
    return id


def advance_time (days: int):
    with open('time.txt', 'r') as time:
        currect_date = time.readline()
        begin_date = datetime.strptime(currect_date, '%Y-%m-%d')
        delta = timedelta(days=days)
        new_date = begin_date + delta

    with open('time.txt', 'w') as time:
        time.write(new_date.strftime('%Y-%m-%d'))

if __name__ == "__main__":
    main()



