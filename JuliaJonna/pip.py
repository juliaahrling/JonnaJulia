import pyodbc as db
import datetime
import random

def welcome():
    print('-' * 40)
    print('Welcome to Jonna och Julias OnlineStore')
    print('-' * 40)

def menu():
    print('1. Login')
    print('2. Create a Customer account')
    print('3. See a list of all products in the store')
    print('4. Exit OnlineStore')

def customer_menu():
    print('-' * 40)
    print('-'* 13 + 'Customer  menu' + '-'* 13)
    print('-' * 40)
    print('1. See a list of all products')
    print('2. See a list of all products currently on sale')
    print('3. Search for product')
    print('4. Add products to shopping cart')
    print('5. See order history')
    print('6. Go back to the start page')

def admin_menu():
    print('-' * 40)
    print('-'* 15 + 'Admin Menu' + '-'* 15)
    print('-' * 40)
    print('1. Add product') 
    print('1. Update quantity')
    print('3. Delete product')
    print('4. Add supplier')
    print('5. Add discount')
    print('6. Add discount to product')
    print('7. Confirm order')
    print('8. Go back to the start page')
def main():
    try: 
        server = 'localhost'
        username = 'SA'
        password = 'reallyStrongPwd#123'
        database = 'Onlineshop'
        connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' +
                                database + ';UID=' + username + ';PWD=' + password)
        
    except: 
        print("Woops! Ett undantag har uppstått")
        print("Undantagstyp: Error")

    cursor = connection.cursor() # type: db.Cursor

    while True:
        welcome()
        menu() 
        choice = input('Your choice: ')
        if choice == '1':
            log_in(cursor, connection) #Function handeling the admin-login
            #check_customer_or_admin()
        elif choice == '2':
            register_customer(cursor, connection) #Function handeling existing customers
        elif choice == '3':
            see_products(cursor, connection) #Function handeling creating a new customer account
        elif choice == '4':
            print('Goodbye!') #Ends the program
            break
        #If the user writes anything else than 1, 2, 3 or 4 the program prints the menu again and asks for new correct input
        else:
            print('The input was incorrect, please try again!')
            continue

def log_in(cursor, connection):
    try:
        user_id = input("Your id: ")

        cursor.execute(f"select [type] from [User] where id = {user_id}")

        user_type = cursor.fetchone()
        user_type_string = ''.join(user_type) 

    
        if user_type_string == 'A':
            print("Welcome Admin")
            get_admins_choice(cursor, connection)
        else:
            print("Welcome Customer")
            get_customers_choice(cursor, connection)
        
        
        connection.commit()  
    except: 
        print("You need to sign up first!")
        register_customer(cursor, connection)
def register_customer(cursor, connection): 

    user_id = int(input("User id: "))
    email = input("Email: ")
    f_name = input("Firstname: ")
    l_name = input("Lastname: ")
    address = input("Address: ")
    city = input("City: ")
    country = input("Country: ")
    phone = int(input("Phone: "))
    c_user = ('C')
    
    cursor.execute("INSERT INTO [User](id, email, f_name, l_name, [address], city, country, phone_number, [type]) values({}, '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}')".format(user_id, email, f_name, l_name, address, city, country, phone, c_user))
    connection.commit()
    print(f"Welcome {f_name}")


def see_products(cursor, connection):

    #Namn som visar vad varje kolumn är för ett värde
    print("{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}".format("Product ID", "Product name", "Category" ,"In Stock", "Price", "Supplier"))
    
    #Hämtar all information
    cursor.execute("select * from Showproducts")
    #connection.commit()
    #fetchall() hämtar allt
    show_products = cursor.fetchall()

    print("-"*88)
    #Måste använda sig av en for-loop för att kunna visa upp informationen bättre
    for r in show_products:
        print(f"{r[0]:<15} {r[1]:<15} {r[2]:<15} {r[3]:<10} {r[4]:<10} {r[5]:<15}")
    connection.commit()
    print("-"*88)


def get_admins_choice(cursor, connection):

    while True:
        admin_menu()    
        choice = input('Your choice: ')
        if choice == '1':
            add_product(cursor, connection) #Function that allows the Admin to add/delete products
            get_admins_choice(cursor, connection)
        elif choice == '2':
            update_quantity(cursor, connection)
            get_admins_choice(cursor, connection)    
        elif choice == '3':
            delete_product(cursor, connection) #Function that allows the Admin to add a list of possible discounts and assign the discounts to specific products
            get_admins_choice(cursor, connection)
        elif choice == '4':
            add_supplier(cursor, connection) #Function that allows the Admin to add suppliers
            get_admins_choice(cursor, connection)
        elif choice == '5':
            add_discount(cursor, connection) #Function that allows the Admin to se a list of new orders and confirm them
            discount_history(cursor, connection)
        elif choice == '6':
            add_discount_to_product(cursor, connection)
        elif choice == '7':
            update_order_status(cursor,connection)
            get_admins_choice(cursor, connection)
        elif choice == '8':
            break #Sends the user back to the start page and shows the start menu 
        #If the user writes anything else than 1, 2, 3 or 4 the program prints the menu again and asks for new correct input
        else:
            print('The input was incorrect, please try again!')
            continue
    
def get_customers_choice(cursor, connection):

    while True:   
        customer_menu()
        choice = input('Your choice: ')
        if choice == '1':
            see_products(cursor, connection)
            get_customers_choice(cursor, connection)
            #Function that shows a list of all products
        elif choice == '2':
            see_all_discounted_products(cursor, connection)
            get_customers_choice(cursor, connection) #Function that shows a list of all products on sale
        elif choice == '3':
            search_product(cursor, connection)
            get_customers_choice(cursor, connection) #Allows the user to search for a specifik product
        elif choice == '4':
            see_products(cursor, connection)
            add_shopping_list(cursor, connection) #Function that allows the customer to add products to a shopping cart
            see_shopping_list(cursor, connection) #See the shoppinglist
            get_customers_choice(cursor, connection)
        elif choice == '5':
            order_history(cursor, connection) #Allows the user to se his/hers order history
        elif choice == '6':
            #Sends the user back to the start page and shows the start menu 
            break
        #If the user writes anything else than 1, 2, 3 or 4 the program prints the menu again and asks for new correct input
        else:
            print('The input was incorrect, please try again!')
            continue
        main()    
def add_product(cursor, connection):

    new_product_id = int(input("Product id: "))
    new_product_name = input("Product name: ")
    new_type = input("Product type: ")
    quantity = int(input("Quantity: "))
    price = int(input("Price: "))
    supplier_id = int(input("Supplier id: "))

    cursor.execute("INSERT INTO Product(id, [name], [type], quantity, price, supplier_id) values({}, '{}', '{}', {}, {}, {})".format(new_product_id, new_product_name, new_type, quantity, price, supplier_id))
    connection.commit()
    
    #Visar upp det som registrerat
    print("Product id: {}, Product name: {}, Product type: {}, Quantity: {}, Price: {}, Supplier id: {} has been added!".format(new_product_id, new_product_name, new_type, quantity, price, supplier_id))
        
def add_supplier(cursor, connection):

    new_supplier_id = int(input("Supplier's id: "))
    new_supplier_name = input("Supplier's name: ")
    new_supplier_address = input("Supplier's address: ")
    new_supplier_phone = int(input("Supplier's phone number: "))

    cursor.execute("INSERT INTO Supplier(id, [name], [address], phone_number) values({}, '{}', '{}', {})".format(new_supplier_id, new_supplier_name, new_supplier_address, new_supplier_phone))
    connection.commit()
    

    #Visar upp det som registrerat
    print("Supplier id: {}, Name: {}, Address: {}, Phone number: {} has been added!".format(new_supplier_id, new_supplier_name, new_supplier_address, new_supplier_phone))
        
    main()

def add_shopping_list(cursor, connection):

    order_id = random.randint(1, 1999999)
    add_product_to_list = input("Product id: ")
    quantity = int(input("Add quantity: "))

    cursor.execute("INSERT INTO Order_item(order_id, product_id, quantity) values({}, '{}', '{}')".format(order_id, add_product_to_list, quantity))
    connection.commit()
    
def see_shopping_list(cursor, connection):
    cursor.execute("Select * from Order_item")
    connection.commit()     

def add_discount_to_product(cursor, connection):

    discount_id = int(input("Discount id: "))
    product_id = int(input("Product id:"))
    start_date = input("Start date (YYYY-MM-DD): ")
    end_date = input("End date (YYYY-MM-DD): ")

    converted_start_date = datetime(start_date, "%Y-%m-%d")
    converted_end_date = datetime(end_date, "%Y-%m-%d")
    print(type(converted_start_date)) 

    cursor.execute("INSERT INTO Discount_history(discount_id, product_id, [start_date], end_date) values({}, {}, '{}', '{}')".format(discount_id, product_id, converted_start_date, converted_end_date))
    connection.commit()
    
    print("Discount id: {}, Product id: {}, Start date: {}, End date: {} has been added!".format(discount_id, product_id, start_date, end_date))
       
def add_discount(cursor, connection):

    discount_id = int(input("Discount id: "))
    discount_reason = input("Discount name: ")
    percentage = int(input("Percentage: "))
    
    
    cursor.execute("INSERT INTO Discount(id, reason, [percentage]) values({}, '{}', '{}')".format(discount_id, discount_reason, percentage))
    connection.commit()
    
    #Visar upp det som registrerat
    print("Product id: {}, Discount name: {}, Percentage: {} has been added!".format(discount_id, discount_reason, percentage))
    
def see_all_discounted_products(cursor, connection):
  
    #Namn som visar vad varje kolumn är för ett värde
    print("{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}".format("Product ID", "Product name", "Category" ,"Supplier name", "In stock", "Regular price", "Discount in %"))
    
    #Hämtar all information
    cursor.execute("select * from products_sale")

    #fetchall() hämtar allt
    show_discounted_products = cursor.fetchall()

    print("-"*88)
    #Måste använda sig av en for-loop för att kunna visa upp informationen bättre
    for r in show_discounted_products:
        print(f"{r[0]:<15} {r[1]:<15} {r[2]:<15} {r[3]:<15} {r[4]:<15} {r[5]:<15} {r[6]:<15}")
    connection.commit()
    print("-"*88)
    

def discount_history(cursor, connection):
    #Namn som visar vad varje kolumn är för ett värde
    print("{:<15}{:<15}{:<15}{:<15}{:<15}".format("Reason", "Discount ID", "Product ID", "Start date" ,"End date"))
    
    #Hämtar all information
    cursor.execute("select * from discountshistory;")

    #fetchall() hämtar allt
    discount_history = cursor.fetchall()

    for s in discount_history:
        print(type(s[3]))

    print("-"*88)
    #Måste använda sig av en for-loop för att kunna visa upp informationen bättre
    for r in discount_history:
        print(f"{r[0]:<15} {r[1]:<15}{r[2]:<15} {r[3].strftime('%m/%d/%Y'):<15} {r[4].strftime('%m/%d/%Y'):<15}")
    connection.commit()
    print("-"*88)

def search_product(cursor, connection): 
    try:
        type = input("Product type: ")
        name = input("Product name: ")
        price = int(input("Price: "))
        supplier_id = int(input("Supplier id: "))

        cursor.execute(f"select * from Product where [type] = '{type}' or [name] = '{name}' or price = {price} or where [name] = '{name}' or supplier_id = {supplier_id}")

        user_type = cursor.fetchall()
        print(user_type)

    except: 
        print("Sorry, could not find the product!")

def update_quantity(cursor, connection):
    
    product_id = int(input("Product id: "))
    admin_input = int(input("New amount of quantity: "))

    cursor.execute(f"UPDATE product SET quantity = {admin_input} WHERE id = {product_id}")
    connection.commit()
def update_order_status(cursor,connection):
    
    order_id = int(input("Order id: "))

    cursor.execute(f"SELECT * FROM [Order] WHERE order_id = {order_id} and [status] = 'NO'; UPDATE [Order] SET [status] ='YES';")
    connection.commit()

    
def delete_product(cursor, connection): 

    product_id = int(input("Product id: "))
    cursor.execute(f"DELETE FROM Product where [id] = {product_id}")
    connection.commit()

    #Visar upp det som registrerat
    print("Product id: {} has been removed!".format(product_id))

main()

