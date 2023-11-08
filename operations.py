import csv
from datetime import date

#This file contains the functions needed to perfom various operational activities

def main():
    pass

def buy_inventory(product_name,buy_price, expiration_date): # This function enables the user to add new data entries to the inventory 
 
    with open('inventory.csv', 'r+', newline='') as inventory:
        reader = csv.DictReader(inventory)
        rows = list(reader)

        buy_date = date.today()

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

def sell_inventory(product_name, sell_price): # this function allows the user to sell inventory and moves the product to the sales ledger
    # opening both the sales and the inventory id with r+ as both need to accessed and changed
    with open('sales.csv', 'r+', newline='') as sales:
        sales_reader = csv.DictReader(sales)
        sales_rows = list(sales_reader)

    with open('inventory.csv', 'r+', newline='') as inventory:
        inventory_reader = csv.DictReader(inventory)
        inventory_rows = list(inventory_reader)

        max_sales_id = 0
        for row in sales_rows: # Finds the highest id number currently in the sales file
            if int(row["sales_id"]) > max_sales_id:
                max_sales_id = int(row["sales_id"])
        new_sales_id = max_sales_id + 1

        sell_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #sets the sell date to the date on which the sale is executed

        sold_item = False
        for row in inventory_rows:
            if row["product_name"] == product_name:
                inventory_id = row["id"]
                buy_price = row["buy_price"]
        
                new_row = {'sales_id': new_sales_id,'inventory_id': inventory_id, 'product_name': product_name, 'sell_date': sell_date, 'sell_price' : sell_price, 'buy_price': buy_price,}
                sales_rows.append(new_row)
                sold_item = True

        if sold_item:
         with open('sales.csv', 'r+', newline='') as sales:
          sales_reader = csv.DictReader(sales)
          sales_rows = list(sales_reader)
          sales_writer = csv.DictWriter(sales, fieldnames=sales_reader.fieldnames)
          sales_writer.writeheader()
          sales_writer.writerows(sales_rows)

         with open('inventory.csv', 'r+', newline='') as inventory:
          inventory_reader = csv.DictReader(inventory)
          inventory_rows = list(inventory_reader)
          inventory_writer = csv.DictWriter(inventory, fieldnames=inventory_reader.fieldnames)
          inventory_writer.writeheader()
          for row in inventory_rows:
              if row["product_name"] != product_name:
                 inventory_writer.writerows(inventory_rows)

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

def delete_inventory(id):
    id = str(id)
    with open('inventory.csv', 'r+', newline='') as inventory:
        reader = csv.DictReader(inventory)
        rows = list(reader)
        
        inventory.seek(0)
        writer = csv.DictWriter(inventory, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in rows:
            if row["id"] != id:
                writer.writerow(row)

        inventory.truncate()

if __name__ == "__main__":
    main()
buy_inventory('knakworst','3','2025-01-01')

