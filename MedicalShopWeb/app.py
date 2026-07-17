from flask import Flask, render_template, request, session
import mysql.connector
from datetime import date

app = Flask(__name__)
app.secret_key = "medical_shop_secret"

# Database Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sql@Server#2025!Aa9",
    database="medical_shop"
)

cursor = connection.cursor()


# Login Page
@app.route("/")
def home():
    return render_template("login.html")


# Login Check
@app.route("/login", methods=["POST"])
def check_login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin123":
        session["user"] = username
        return render_template("dashboard.html")

    return "Invalid Username or Password"

@app.route("/add_medicine")
def add_medicine():
    return render_template("add_medicine.html")

@app.route("/save_medicine", methods=["POST"])
def save_medicine():

    medicine_name = request.form["medicine_name"]
    company = request.form["company"]
    price = request.form["price"]
    quantity = request.form["quantity"]
    expiry_date = request.form["expiry_date"]

    query = """
    INSERT INTO medicines
    (medicine_name, company, price, quantity, expiry_date)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        medicine_name,
        company,
        price,
        quantity,
        expiry_date
    )

    cursor.execute(query, values)
    connection.commit()

    return "Medicine Added Successfully!"

@app.route("/view_medicines")
def view_medicines():
       
    if "user" not in session:
        return render_template("login.html")

    query = "SELECT * FROM medicines"
    cursor.execute(query)

    medicines = cursor.fetchall()

    return render_template(
        "view_medicines.html",
        medicines=medicines
    )
@app.route("/search_medicine", methods=["GET", "POST"])
def search_medicine():

    if request.method == "POST":

        medicine_name = request.form["medicine_name"]

        query = "SELECT * FROM medicines WHERE medicine_name=%s"

        cursor.execute(query, (medicine_name,))

        medicine = cursor.fetchone()

        return render_template(
            "search_medicine.html",
            medicine=medicine
        )

    return render_template(
        "search_medicine.html",
        medicine=None
    )
@app.route("/dashboard")
def dashboard():

    cursor.execute("SELECT COUNT(*) FROM medicines")
    total_medicines = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total_amount) FROM sales")
    total_sales = cursor.fetchone()[0]

    if total_sales is None:
        total_sales = 0

    cursor.execute("SELECT COUNT(*) FROM medicines WHERE quantity < 10")
    low_stock = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM medicines
    WHERE expiry_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY)
    """)
    expiry = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_medicines=total_medicines,
        total_sales=total_sales,
        low_stock=low_stock,
        expiry=expiry
    )

@app.route("/update_medicine")
def update_medicine():
    return render_template("update_medicine.html")

@app.route("/update_medicine_data", methods=["POST"])
def update_medicine_data():

    medicine_id = request.form["medicine_id"]
    medicine_name = request.form["medicine_name"]
    company = request.form["company"]
    price = request.form["price"]
    quantity = request.form["quantity"]
    expiry_date = request.form["expiry_date"]


    query = """
    UPDATE medicines
    SET medicine_name=%s,
        company=%s,
        price=%s,
        quantity=%s,
        expiry_date=%s
    WHERE medicine_id=%s
    """

    values = (
        medicine_name,
        company,
        price,
        quantity,
        expiry_date,
        medicine_id
    )


    cursor.execute(query, values)
    connection.commit()


    return "Medicine Updated Successfully!"

@app.route("/delete_medicine")
def delete_medicine():
    return render_template("delete_medicine.html")


@app.route("/delete_medicine_data", methods=["POST"])
def delete_medicine_data():

    medicine_id = request.form["medicine_id"]

    query = "DELETE FROM medicines WHERE medicine_id=%s"

    cursor.execute(query, (medicine_id,))
    connection.commit()

    if cursor.rowcount > 0:
        return "Medicine Deleted Successfully!"
    else:
        return "Medicine ID Not Found"
@app.route("/billing")
def billing():
    return render_template("billing.html")

@app.route("/generate_bill", methods=["POST"])
def generate_bill():

    customer_name = request.form["customer_name"]
    medicine_name = request.form["medicine_name"]
    quantity = int(request.form["quantity"])

    query = "SELECT * FROM medicines WHERE medicine_name=%s"
    cursor.execute(query, (medicine_name,))

    medicine = cursor.fetchone()

    if medicine:

        price = medicine[3]
        stock = medicine[4]

        if quantity > stock:
            return "Not Enough Stock!"

        total = price * quantity
        sales_query = """
        INSERT INTO sales
        (customer_name, medicine_name, quantity, total_amount, sale_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        sales_values = (
            customer_name,
            medicine_name,
            quantity,
            total,
            date.today()
        )

        update_stock_query = """
        UPDATE medicines
        SET quantity = quantity - %s
        WHERE medicine_name = %s
        """

        cursor.execute(sales_query, sales_values)

        cursor.execute(update_stock_query, (quantity, medicine_name))

        connection.commit()

        return render_template(
            "bill.html",
            customer_name=customer_name,
            medicine_name=medicine_name,
            price=price,
            quantity=quantity,
            total=total
        )

    else:
        return "Medicine Not Found!"

@app.route("/sales_history")
def sales_history():

    query = "SELECT * FROM sales"

    cursor.execute(query)

    sales = cursor.fetchall()

    return render_template(
        "sales_history.html",
        sales=sales
    )
@app.route("/test")
def test():
    return "Test Working"

@app.route("/check")
def check():
    return "THIS IS MY CURRENT APP"
    
@app.route("/low_stock")
def low_stock():

    query = "SELECT * FROM medicines WHERE quantity < 10"

    cursor.execute(query)

    medicines = cursor.fetchall()

    return render_template(
        "low_stock.html",
        medicines=medicines
    )
@app.route("/today_sales")
def today_sales():

    query = """
    SELECT customer_name,
           medicine_name,
           quantity,
           total_amount,
           sale_date
    FROM sales
    WHERE sale_date = CURDATE()
    """

    cursor.execute(query)

    sales = cursor.fetchall()

    return render_template(
        "today_sales.html",
        sales=sales
    )
@app.route("/total_sales")
def total_sales():

    query = "SELECT SUM(total_amount) FROM sales"

    cursor.execute(query)

    total = cursor.fetchone()

    return render_template(
        "total_sales.html",
        total=total[0]
    )
@app.route("/expiry_medicines")
def expiry_medicines():

    query = """
    SELECT * FROM medicines
    WHERE expiry_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY)
    """

    cursor.execute(query)

    medicines = cursor.fetchall()

    return render_template(
        "expiry_medicines.html",
        medicines=medicines
    )
@app.route("/medicine_sales")
def medicine_sales():

    query = """
    SELECT medicine_name,
           SUM(quantity),
           SUM(total_amount)
    FROM sales
    WHERE medicine_name IS NOT NULL
    GROUP BY medicine_name
    """

    cursor.execute(query)

    report = cursor.fetchall()

    return render_template(
        "medicine_sales.html",
        report=report
    )
@app.route("/logout")
def logout():

    session.pop("user", None)

    return render_template("login.html")
if __name__ == "__main__":
    app.run(debug=True)