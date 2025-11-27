import mysql.connector


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="vIJAY@123",  
        database="restaurant_db"
    )


def admin_login():
    user = input("Admin username: ")
    pwd  = input("Password: ")
    db   = get_db()
    cur  = db.cursor()
    cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (user, pwd))
    if cur.fetchone():
        print("\nWelcome Admin!")
        admin_menu()
    else:
        print("Invalid admin credentials")
    db.close()

def admin_menu():
    while True:
        print("\nAdmin Menu: 1.Add Item 2.Delete Item 3.Modify Item 4.View Orders 5.Daywise Profit 6.Back")
        ch = input("Choice: ")
        db = get_db()
        cur = db.cursor()
        if ch == "1":
            name = input("Item name: ")
            cat  = input("Category: ")
            price= float(input("Price: "))
            cur.execute("INSERT INTO menu(item_name,category,price) VALUES(%s,%s,%s)", (name, cat, price))
            db.commit()
            print("Item added.")
        elif ch == "2":
            iid = input("Item id to delete: ")
            cur.execute("DELETE FROM menu WHERE item_id=%s", (iid,))
            db.commit()
            print("Item deleted.")
        elif ch == "3":
            iid   = input("Item id to modify price: ")
            price = float(input("New price: "))
            cur.execute("UPDATE menu SET price=%s WHERE item_id=%s", (price, iid))
            db.commit()
            print("Price updated.")
        elif ch == "4":
            cur.execute("SELECT * FROM orders")
            for r in cur.fetchall():
                print(r)
        elif ch == "5":
            cur.execute("SELECT DATE(order_date), SUM(total_amt) FROM orders GROUP BY DATE(order_date)")
            for r in cur.fetchall():
                print(f"Date: {r[0]}  Profit: ₹{r[1]}")
        elif ch == "6":
            db.close()
            break
        db.close()


def user_login():
    name   = input("Your Name: ")
    mobile = input("Mobile No: ")
    cart   = []
    while True:
        print("\nUser Menu: 1.View Menu 2.Add to Cart 3.Modify Cart 4.Bill & Checkout 5.Back")
        ch = input("Choice: ")
        db = get_db()
        cur = db.cursor()
        if ch == "1":
            cur.execute("SELECT * FROM menu")
            for r in cur.fetchall():
                print(f"{r[0]} - {r[1]} ({r[2]}) ₹{r[3]}")
        elif ch == "2":
            iid = input("Enter item id: ")
            qty = int(input("Qty: "))
            cur.execute("SELECT item_name, price FROM menu WHERE item_id=%s", (iid,))
            item = cur.fetchone()
            if item:
                cart.append({"id": iid, "name": item[0], "price": item[1], "qty": qty})
                print("Item added to cart.")
            else:
                print("Invalid item id.")
        elif ch == "3":
            print("Cart:", cart)
            rem = input("Item id to remove (or Enter to skip): ")
            if rem:
                cart = [c for c in cart if c["id"] != rem]
                print("Item removed.")
        elif ch == "4":
            total = sum(c["price"] * c["qty"] for c in cart)
            cur.execute(
                "INSERT INTO orders(user_name,mobile_no,total_amt) VALUES(%s,%s,%s)",
                (name, mobile, total)
            )
            order_id = cur.lastrowid
            for c in cart:
                cur.execute(
                    "INSERT INTO order_items(order_id,item_id,quantity,price) VALUES(%s,%s,%s,%s)",
                    (order_id, c["id"], c["qty"], c["price"])
                )
            db.commit()
            print("\n----- BILL -----")
            for c in cart:
                print(f"{c['name']} x{c['qty']} = ₹{c['price']*c['qty']}")
            print("Total: ₹", total)
            db.close()
            break
        elif ch == "5":
            db.close()
            break
        db.close()


if __name__ == "__main__":
    while True:
        print("\n*** Restaurant Management System ***")
        print("1.Admin Login  2.User Login  3.Exit")
        choice = input("Select: ")
        if choice == "1":
            admin_login()
        elif choice == "2":
            user_login()
        elif choice == "3":
            break
