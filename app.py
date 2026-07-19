import mysql.connector
from datetime import date

# Database Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="medical_shop"
)

cursor = connection.cursor()

# Login
username = input("Enter Username: ")
password = input("Enter Password: ")

query = "SELECT * FROM users WHERE username=%s AND password=%s"
cursor.execute(query, (username, password))

result = cursor.fetchone()

if result:

    print("\nLogin Successful!")

    print("\n=================================")
    print(" MEDICAL SHOP MANAGEMENT SYSTEM ")
    print("=================================")
    print("1. Add Medicine")
    print("2. View Medicines")
    print("3. Search Medicine")
    print("4. Update Medicine")
    print("5. Delete Medicine")
    print("6. Billing")
    print("7. View Sales History")
    print("8. Low Stock Medicines")
    print("9. Today's Sales Report")
    print("10. Total Sales Amount")
    print("11. Expiry Medicines Alert")
    print("12. Medicine Sales Report")

    choice = input("\nEnter Your Choice: ")

    # 1. Add Medicine
    if choice == "1":

        medicine_name = input("Enter Medicine Name: ")
        company = input("Enter Company Name: ")
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
        expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")

        query = """
        INSERT INTO medicines
        (medicine_name, company, price, quantity, expiry_date)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (medicine_name, company, price, quantity, expiry_date)

        cursor.execute(query, values)
        connection.commit()

        print("\nMedicine Added Successfully!")

    # 2. View Medicines
    elif choice == "2":

        query = "SELECT * FROM medicines"
        cursor.execute(query)

        medicines = cursor.fetchall()

        print("\n========== MEDICINES LIST ==========")

        for medicine in medicines:
            print(medicine)

    # 3. Search Medicine
    elif choice == "3":

        medicine_name = input("Enter Medicine Name: ")

        query = "SELECT * FROM medicines WHERE medicine_name=%s"

        cursor.execute(query, (medicine_name,))

        medicines = cursor.fetchall()

        if medicines:
            print("\n========== SEARCH RESULT ==========")

            for medicine in medicines:
                print(medicine)

        else:
            print("\nMedicine Not Found!")

    # 4. Update Medicine
    elif choice == "4":

        medicine_id = int(input("Enter Medicine ID: "))
        new_price = float(input("Enter New Price: "))
        new_quantity = int(input("Enter New Quantity: "))

        query = """
        UPDATE medicines
        SET price=%s, quantity=%s
        WHERE medicine_id=%s
        """

        values = (new_price, new_quantity, medicine_id)

        cursor.execute(query, values)
        connection.commit()

        print("\nMedicine Updated Successfully!")

    # Remaining Options
    elif choice == "5":

        medicine_id = int(input("Enter Medicine ID to Delete: "))

        query = "DELETE FROM medicines WHERE medicine_id=%s"

        cursor.execute(query, (medicine_id,))

        connection.commit()

        print("\nMedicine Deleted Successfully!")

    elif choice == "6":

        customer_name = input("Enter Customer Name: ")
        medicine_id = int(input("Enter Medicine ID: "))
        quantity = int(input("Enter Quantity: "))

        query = "SELECT medicine_name, price FROM medicines WHERE medicine_id=%s"

        cursor.execute(query, (medicine_id,))

        medicine = cursor.fetchone()

        if medicine:

            medicine_name = medicine[0]
            price = float(medicine[1])

            total = price * quantity

            print("\n======================================")
            print("       MEDICAL SHOP BILL")
            print("======================================")
            print("Customer Name :", customer_name)
            print("Medicine      :", medicine_name)
            print("Price         : ₹", price)
            print("Quantity      :", quantity)
            print("--------------------------------------")
            print("Total Amount  : ₹", total)
            print("======================================")
            print("      THANK YOU! VISIT AGAIN")
            print("======================================")

            query = """
            INSERT INTO sales
            (customer_name, total_amount, sale_date, medicine_name, quantity)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                customer_name,
                total,
                date.today(),
                medicine_name,
                quantity
            )

            cursor.execute(query, values)

            connection.commit()
            query = """
            UPDATE medicines
            SET quantity = quantity - %s
            WHERE medicine_id = %s
            """

            values = (quantity, medicine_id)

            cursor.execute(query, values)

            connection.commit()

            print("\nStock Updated Successfully!")
            print("\nBill Saved Successfully!")
        else:
            print("\nMedicine ID Not Found!")
    elif choice == "7":

        query = "SELECT * FROM sales"

        cursor.execute(query)

        sales = cursor.fetchall()

        print("\n========== SALES HISTORY ==========")

        if sales:
            for sale in sales:
                print(sale)
        else:
            print("\nNo Sales History Found!")

    elif choice == "8":

        query = "SELECT * FROM medicines WHERE quantity <= 10"

        cursor.execute(query)

        medicines = cursor.fetchall()

        print("\n========== LOW STOCK MEDICINES ==========")

        if medicines:
            for medicine in medicines:
                print(medicine)
        else:
            print("\nNo Low Stock Medicines.")
    elif choice == "9":

        query = "SELECT * FROM sales WHERE sale_date = CURDATE()"

        cursor.execute(query)

        sales = cursor.fetchall()

        print("\n========== TODAY'S SALES REPORT ==========")

        if sales:
            for sale in sales:
                print(sale)
        else:
            print("\nNo Sales Today.")
    elif choice == "10":

        query = "SELECT SUM(total_amount) FROM sales"

        cursor.execute(query)

        total = cursor.fetchone()

        print("\n========== TOTAL SALES ==========")

        if total[0]:
            print("Total Sales Amount : ₹", total[0])
        else:
            print("No Sales Found!")
    elif choice == "11":

        query = """
        SELECT * FROM medicines
        WHERE expiry_date <= CURDATE()
        """

        cursor.execute(query)

        medicines = cursor.fetchall()

        print("\n========== EXPIRED MEDICINES ==========")

        if medicines:
            for medicine in medicines:
                print(medicine)
        else:
            print("\nNo Expired Medicines.")
    elif choice == "12":

        query = """
        SELECT medicine_name, SUM(quantity)
        FROM sales
        WHERE medicine_name IS NOT NULL
        GROUP BY medicine_name
        """

        cursor.execute(query)

        sales = cursor.fetchall()

        print("\n========== MEDICINE SALES REPORT ==========")

        if sales:
            for sale in sales:
                print(sale[0], ":", sale[1], "Sold")
        else:
            print("\nNo Sales Found!")
                
    else:
        print("\nInvalid Choice!")

else:
    print("\nInvalid Username or Password!")

connection.close()