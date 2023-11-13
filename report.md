# Superpy Report 

**Implementation Rich**
I have chosen to implement rich into my Superpy application in order to make the CLI experience more pleasant. The initial output provided by Superpy was rather dry and not very user friendly. For example when the user would request the inventory report, Superpy would return every row in the inventory as a list in the following manner:

['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date']
['1', 'apple', '2023-11-01', '3', '2023-12-01']
['2', 'orange', '2023-11-01', '2', '2023-12-09']

While this is finely usable, it does not make for a pleasant user experience. For a better user experience a neatly formatted table is desirable. Rich allows for this implementation. The code below provides the formatting of the table:

table = Table(title="[bold green]Inventory Report")
        table.add_column("ID")
        table.add_column("Product Name")
        table.add_column("Buy Date")
        table.add_column("Buy Price")
        table.add_column("Expiration Date")

After this the .addrow function is used to add the desired rows to the table. Lastly the Console function is used to print the table. This has created the following table which is much more user friendly. 
┏━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Product Name ┃ Buy Date   ┃ Buy Price ┃ Expiration Date ┃
┡━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 1  │ apple        │ 2023-11-01 │ 3         │ 2023-12-01      │
│ 2  │ orange       │ 2023-11-01 │ 2         │ 2023-12-09      │
└────┴──────────────┴────────────┴───────────┴─────────────────┘

**Implementing Reportlab**
As I work in financial control I wanted to implement a little element of that. Because the end of month closing and report cycle is very important in this field I included a function that relates to this (report_monthly). I wanted the function to create a report in PDF format for the desired month. There are multiple modules that can create a PDF file in python. After doing some research I found Reportlab. I chose this module as it is regularly updated (last time Nov 8 2023), well documented and easy to implement. The creation of a PDF file with the desired content does not take a lot of effort and or knowledge and can be accomplished in only a few lines of code:

lines = report_content.split('\n')
    report = canvas.Canvas(f"Monthly Report {report_period}.pdf", pagesize= letter)
    text = report.beginText(100, 750)
    text.setFont("Times-Roman", 12)

    for line in lines:
        text.textLine(line)

    report.drawText(text)
    report.save()

 While the report_monthly function is still very limited it does provide some more information than the revenue and (gross) profit function do. 

 **Truncate**
 I had some problems with removing the sold items from the inventory ledger. After looking into some ways to solve this I came across the .truncate function. Which is in essence a function to resize a file. However if used without an argument it removes all contents that are beyond the position of the cursor. In combination with .seek(0), as this sets the cursor to the beginning of the file, it ensures all old data is removed and only the new data entry is included in the csv file. In this manner I managed to get rid of the items that were either sold/removed or moved to the obsolete inventory. 