import csv
from datetime import *
from rich.console import Console
#This file contains the functions needed to perfom various operational activities

def main():
    pass

with open('time.txt', 'r') as time: #opening the time.txt file to make the internal time of Superpy available to the functions
        current_date = time.readline()

def buy_inventory(product_name,buy_price, expiration_date): # This function enables the user to add new data entries to the inventory 
    console = Console()
    with open('inventory.csv', 'r+', newline='') as inventory: #opening the csv file with r+ in order to read and to write to the file. 
        reader = csv.DictReader(inventory)
        rows = list(reader)

        buy_date = current_date

        # Finding the highest id currently in the inventory ledger
        max_id = 0
        for row in rows: 
            if int(row["id"]) > max_id:
                max_id = int(row["id"])

        new_id = max_id + 1 # adds + 1 to the current highest id number 
        new_row = {'id': new_id, 'product_name': product_name, 'buy_date': buy_date, 'buy_price': buy_price, 'expiration_date': expiration_date}
        rows.append(new_row) # Adds a new row to the inventory based on the generated id number and the users data input regarding the product
        console.print(f"[bold green]Successfully bought: {product_name}")

        inventory.seek(0) #used to start writing from the top of the csv file. 
        writer = csv.DictWriter(inventory, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    

def sell_inventory(product_name, sell_price): # this function allows the user to sell inventory and moves the product to the sales ledger
    console = Console()
    with open('sales.csv', 'r+', newline='') as sales:
        sales_reader = csv.DictReader(sales)
        sales_rows = list(sales_reader)

        # Finding the highest sales-id currently in the sales ledger
        max_sales_id = 0
        for row in sales_rows: 
            if int(row["sales_id"]) > max_sales_id:
                max_sales_id = int(row["sales_id"])
        new_sales_id = max_sales_id + 1

        sell_date = current_date #sets the sell date to the date on which the sale is executed

        sold_item = False #variable used to make sure an item is not sold multiple times or multiple of the same are sold, default set False
        with open('inventory.csv', 'r+', newline='') as inventory:
            inventory_reader = csv.DictReader(inventory)
            inventory_rows = list(inventory_reader)

            inventory_rows_updated =[] #empty variable used to later store the new data that has to be written to the inventory csv

            in_stock = False # variable used to determine if something is in stock, default set at false
            for row in inventory_rows:
                if row["product_name"] == product_name and not sold_item:
                    in_stock = True #if product can be found in the rows it must mean it is in stock, therefore in_stock = True 
                    expiration_date = row["expiration_date"]
                    expired = expiration_date < sell_date

                    if not expired:
                     inventory_id = row["id"]
                     buy_price = row["buy_price"]
                     new_row = {'sales_id': new_sales_id,'inventory_id': inventory_id, 'product_name': product_name, 'sell_date': sell_date, 'sell_price' : sell_price, 'buy_price': buy_price,}
                     sales_rows.append(new_row)
                     sold_item = True #Found a row that meets the selling criteria, so we set it to sold so it does not sell more. 
                     console.print(f"[bold blue]Successfully sold: {product_name}")
                else:
                    inventory_rows_updated.append(row)

            if not in_stock:
                console.print("[bold red]ERROR: This product is out of stock")
            elif not sold_item: #Items is in stock? Item is not sold? That must mean it has expired
               console.print("[bold red]ERROR: This product has expired and can therefore not be sold")
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

def remove_obsolete_inventory(): #This function removes the expired items from the inventory to the obsolete inventory ledger
    with open('obsolete_inventory.csv', 'r+', newline='') as obs:
        obs_reader = csv.DictReader(obs)
        obs_rows = list(obs_reader)

        period = current_date[:7] #getting the current period by slicing the date 

        with open('inventory.csv', 'r+', newline='') as inventory:
            inventory_reader = csv.DictReader(inventory)
            inventory_rows = list(inventory_reader)

            inventory_rows_updated =[]

            for row in inventory_rows:
                    expiration_date = row["expiration_date"]
                    expired = expiration_date < current_date

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
            inventory.truncate() #truncate method clears the file from any old data making sure only the updated entry is included in the inventory 

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
                writer.writerow(row) #all rows are written to the csv except the one contaimng the desired id

        inventory.truncate() #truncate method clears the file from any old data making sure only the updated entry is included in the inventory 
    return id

def set_time (date): #sets internal time of superpy
    new_date = datetime.strptime(date, '%Y-%m-%d')

    with open('time.txt', 'w') as time: #opening the text file that contains the date in order to change it
        time.write(new_date.strftime('%Y-%m-%d'))
    return new_date.strftime('%Y-%m-%d')


def advance_time (days: int): #advances internal time of superpy
    console = Console()
    with open('time.txt', 'r') as time:
        current_date = time.readline()
        begin_date = datetime.strptime(current_date, '%Y-%m-%d')
        delta = timedelta(days=days)
        new_date = begin_date + delta

    with open('time.txt', 'w') as time:
        time.write(new_date.strftime('%Y-%m-%d'))
    return console.print(f'[bold yellow] Date succesfully advanced by {days} to {new_date.strftime("%Y-%m-%d")}')

def current_time(): #shows the current internal time of superpy
    with open('time.txt', 'r') as time:
        current_date = time.readline()
    return current_date

if __name__ == "__main__":
    main()



