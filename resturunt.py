import mysql.connector



def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vijay@123",   # change if needed
        database="restaurant_db"
    )

def admin_login():
    user = input("Admin username: ")
    pwd = input("Password: ")

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (user, pwd)
        )
        if cur.fetchone():
            print("\n✅ Login successful. Welcome Admin!")
            admin_menu()
        else:
            print("\n❌ Invalid admin credentials")
    finally:
        cur.close()
        db.close()


def admin_menu():
    while True:
        print("\n------ ADMIN MENU ------")
        print("1. Add Item")
        print("2. Delete Item")
        print("3. Modify Item Price")
        print("4. View All Orders")
        print("5. Day-wise Profit")
        print("6. Back to Main Menu")

        ch = input("Enter your choice: ")

        if ch == "1":
            add_menu_item()
        elif ch == "2":
            delete_menu_item()
        elif ch == "3":
            modify_menu_item()
        elif ch == "4":
            view_all_orders()
        elif ch == "5":
            show_daywise_profit()
        elif ch == "6":
            break
        else:
            print("⚠️ Invalid choice. Try again.")


def add_menu_item():
    name = input("Enter item name: ")
    cat = input("Enter category: ")
    price = float(input("Enter price: "))

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            "INSERT INTO menu(item_name, category, price) VALUES (%s, %s, %s)",
            (name, cat, price)
        )
        db.commit()
        print(f"✅ Item '{name}' added successfully.")
    finally:
        cur.close()
        db.close()


def delete_menu_item():
    iid = input("Enter item ID to delete: ")

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM menu WHERE item_id=%s", (iid,))
        if cur.rowcount > 0:
            db.commit()
            print("✅ Item deleted successfully.")
        else:
            print("⚠️ No item found with that ID.")
    finally:
        cur.close()
        db.close()


def modify_menu_item():
    iid = input("Enter item ID to modify price: ")
    price = float(input("Enter new price: "))

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            "UPDATE menu SET price=%s WHERE item_id=%s",
            (price, iid)
        )
        if cur.rowcount > 0:
            db.commit()
            print("✅ Price updated successfully.")
        else:
            print("⚠️ No item found with that ID.")
    finally:
        cur.close()
        db.close()


def view_all_orders():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM orders")
        rows = cur.fetchall()

        print("\n------ ALL ORDERS ------")
        if not rows:
            print("No orders found.")
        else:
            for r in rows:
                # (order_id, user_name, mobile_no, total_amt, order_date)
                print(f"OrderID: {r[0]} | Name: {r[1]} | Mobile: {r[2]} | Total: ₹{r[3]} | Date: {r[4]}")
    finally:
        cur.close()
        db.close()


def show_daywise_profit():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            SELECT DATE(order_date) AS day, SUM(total_amt) 
            FROM orders 
            GROUP BY DATE(order_date)
        """)
        rows = cur.fetchall()

        print("\n------ DAY-WISE PROFIT ------")
        if not rows:
            print("No orders found.")
        else:
            for r in rows:
                print(f"Date: {r[0]}  |  Profit: ₹{r[1]}")
    finally:
        cur.close()
        db.close()


def user_login():
    print("\n------ USER SECTION ------")
    name = input("Your Name: ")
    mobile = input("Mobile No: ")

    cart = []  # list of dicts: {"id", "name", "price", "qty"}

    while True:
        print("\n------ USER MENU ------")
        print("1. View Menu")
        print("2. Add to Cart")
        print("3. Modify Cart")
        print("4. Bill & Checkout")
        print("5. Back to Main Menu")

        ch = input("Enter your choice: ")

        if ch == "1":
            show_menu()
        elif ch == "2":
            add_to_cart(cart)
        elif ch == "3":
            modify_cart(cart)
        elif ch == "4":
            if not cart:
                print("⚠️ Cart is empty. Add items before billing.")
            else:
                checkout(name, mobile, cart)
                break
        elif ch == "5":
            break
        else:
            print("⚠️ Invalid choice. Try again.")


def show_menu():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM menu")
        rows = cur.fetchall()

        print("\n------ MENU ------")
        if not rows:
            print("No items in menu.")
        else:
            for r in rows:
                # (item_id, item_name, category, price)
                print(f"{r[0]} - {r[1]} ({r[2]})  ₹{r[3]}")
    finally:
        cur.close()
        db.close()


def add_to_cart(cart):
    iid = input("Enter item ID to add: ")
    qty = int(input("Enter quantity: "))

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("SELECT item_name, price FROM menu WHERE item_id=%s", (iid,))
        item = cur.fetchone()
        if item:
            cart.append({
                "id": iid,
                "name": item[0],
                "price": item[1],
                "qty": qty
            })
            print(f"✅ {item[0]} x{qty} added to cart.")
        else:
            print("⚠️ Invalid item ID.")
    finally:
        cur.close()
        db.close()


def modify_cart(cart):
    if not cart:
        print("Cart is empty.")
        return

    print("\nCurrent Cart:")
    for c in cart:
        print(f"ID: {c['id']} | {c['name']} x{c['qty']} = ₹{c['price'] * c['qty']}")

    rem = input("Enter item ID to remove (or press Enter to cancel): ")
    if rem:
        new_cart = [c for c in cart if c["id"] != rem]
        if len(new_cart) == len(cart):
            print("⚠️ No item with that ID in cart.")
        else:
            cart[:] = new_cart  # modify in place
            print("✅ Item removed from cart.")


def checkout(name, mobile, cart):
    db = get_db()
    cur = db.cursor()
    try:
        total = sum(c["price"] * c["qty"] for c in cart)

        # Insert into orders
        cur.execute(
            "INSERT INTO orders(user_name, mobile_no, total_amt) VALUES (%s, %s, %s)",
            (name, mobile, total)
        )
        order_id = cur.lastrowid

        # Insert each item into order_items
        for c in cart:
            cur.execute(
                "INSERT INTO order_items(order_id, item_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, c["id"], c["qty"], c["price"])
            )

        db.commit()

        # Print Bill
        print("\n--------- BILL ---------")
        print(f"Customer: {name}")
        print(f"Mobile:   {mobile}\n")
        for c in cart:
            line_total = c["price"] * c["qty"]
            print(f"{c['name']} x{c['qty']} = ₹{line_total}")
        print("------------------------")
        print(f"TOTAL: ₹{total}")
        print("------------------------")
        print("✅ Order placed successfully!")
    finally:
        cur.close()
        db.close()


if __name__ == "__main__":
    while True:
        print("\n*** Restaurant Management System ***")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")

        choice = input("Select: ")

        if choice == "1":
            admin_login()
        elif choice == "2":
            user_login()
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")
