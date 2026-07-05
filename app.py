from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("erp.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def dashboard():

    conn = get_db()

    employee = conn.execute(
        "SELECT COUNT(*) FROM employees"
    ).fetchone()[0]

    customer = conn.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    product = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    supplier = conn.execute(
        "SELECT COUNT(*) FROM suppliers"
    ).fetchone()[0]

    inventory = conn.execute(
        "SELECT COUNT(*) FROM inventory"
    ).fetchone()[0]

    sales = conn.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    payment = conn.execute(
        "SELECT IFNULL(SUM(amount),0) FROM payments"
    ).fetchone()[0]

    revenue = conn.execute(
        "SELECT IFNULL(SUM(total),0) FROM sales"
    ).fetchone()[0]

    recent_sales = conn.execute(
        "SELECT * FROM sales ORDER BY id DESC LIMIT 5"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        employee=employee,
        customer=customer,
        product=product,
        supplier=supplier,
        inventory=inventory,
        sales=sales,
        payment=payment,
        revenue=revenue,
        recent_sales=recent_sales
    )


if __name__ == "__main__":
    app.run(debug=True)