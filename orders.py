from db_connect import DataConnect

class Orders:
  def __init__(self):
    self.db = DataConnect()
  
  def view_orders(self):
    query = "SELECT order_id, customer_id, employee_id, order_date FROM orders"
    self.db.cursor.execute(query)

    rows = self.db.cursor.fetchall()

    if not rows:
      print("no orders can be found")
    else:
      print("========= ORDERS =========")
      for row in rows:
        order_id = row[0]
        customer_id = row[1]
        employee_id = row[2]
        order_date = row[3]
        print(f"order id: {order_id}, ordered by {customer_id}, delivered by {employee_id}, ordered on {order_date}")
  
  def view_order_details(self):
    self.view_orders()
    while True:
      user_choice = input("enter ORDER ID to view detials (or type 'b' to go back): ").strip().lower()

      if user_choice == 'b':
        print("Going back...")
        return
      
      if not user_choice.isdigit():
        print("Invalid input, Please enter a number or 'b' to go back.")
        continue
      
      order_id = int(user_choice)
      query = """
      SELECT order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country FROM orders
      WHERE order_id = %s
      """
      self.db.cursor.execute(query, (order_id, ))
      order = self.db.cursor.fetchone()

      if not order:
        print(f"No order found with ID {order_id} . Try again or type 'b' to go back.")
      else:
        print("\n========= ORDER DETAILS =========")
        fields = [
          "Order ID", "Customer ID", "Employee ID", "Order Date", "Required Date", "Shipped Date", "Ship Via", "Freight", "Ship Name", "Ship Address", "Ship City", "Ship Region", "Ship Postal Code", "Ship Country"
        ]
        for field, value in zip(fields, order):
          print(f"{field}: {value}")
        
        input("\nPress Enter to continue...")
        return
  
  def add_order(self):
    try:
        customer_id = input("Enter Customer ID: ").strip()
        employee_id = input("Enter Employee ID: ").strip()
        order_date = input("Enter Order Date (YYYY-MM-DD): ").strip()
        required_date = input("Enter Required Date (YYYY-MM-DD): ").strip()
        shipped_date = input("Enter Shipped Date (YYYY-MM-DD): ").strip()
        ship_via = input("Enter Ship Via (numeric): ").strip()
        freight = input("Enter Freight (numeric): ").strip()
        ship_name = input("Enter Ship Name: ").strip()
        ship_address = input("Enter Ship Address: ").strip()
        ship_city = input("Enter Ship City: ").strip()
        ship_region = input("Enter Ship Region: ").strip()
        ship_postal_code = input("Enter Ship Postal Code: ").strip()
        ship_country = input("Enter Ship Country: ").strip()

        query = """
        INSERT INTO orders 
        (customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, 
         ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        self.db.cursor.execute(query, (
            customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight,
            ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country
        ))
        self.db.connection.commit()
        print("Order added successfully.")
    except Exception as e:
        print(f"Error while adding order: {e}")

  def edit_order(self, order_id):
    self.db.cursor.execute("""
      SELECT customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country
      FROM orders
      WHERE order_id = %s
    """, (order_id,))
    order = self.db.cursor.fetchone()

    if not order:
      print(f"No order found with ID {order_id}.")
      return

    (customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country) = order

    try:
      print(f"\nEditing Order ID {order_id}")

      new_customer_id = input(f"(Current Customer ID: {customer_id})\nNew Customer ID (or leave blank to keep current): ").strip() or customer_id
      new_employee_id = input(f"(Current Employee ID: {employee_id})\nNew Employee ID (or leave blank to keep current): ").strip() or employee_id
      new_order_date = input(f"(Current Order Date: {order_date})\nNew Order Date (YYYY-MM-DD, or leave blank to keep current): ").strip() or order_date
      new_required_date = input(f"(Current Required Date: {required_date})\nNew Required Date (YYYY-MM-DD, or leave blank to keep current): ").strip() or required_date
      new_shipped_date = input(f"(Current Shipped Date: {shipped_date})\nNew Shipped Date (YYYY-MM-DD, or leave blank to keep current): ").strip() or shipped_date
      new_ship_via = input(f"(Current Ship Via: {ship_via})\nNew Ship Via (or leave blank to keep current): ").strip() or ship_via
      new_freight = input(f"(Current Freight: {freight})\nNew Freight (or leave blank to keep current): ").strip() or freight
      new_ship_name = input(f"(Current Ship Name: {ship_name})\nNew Ship Name (or leave blank to keep current): ").strip() or ship_name
      new_ship_address = input(f"(Current Ship Address: {ship_address})\nNew Ship Address (or leave blank to keep current): ").strip() or ship_address
      new_ship_city = input(f"(Current Ship City: {ship_city})\nNew Ship City (or leave blank to keep current): ").strip() or ship_city
      new_ship_region = input(f"(Current Ship Region: {ship_region})\nNew Ship Region (or leave blank to keep current): ").strip() or ship_region
      new_ship_postal_code = input(f"(Current Ship Postal Code: {ship_postal_code})\nNew Ship Postal Code (or leave blank to keep current): ").strip() or ship_postal_code
      new_ship_country = input(f"(Current Ship Country: {ship_country})\nNew Ship Country (or leave blank to keep current): ").strip() or ship_country

      query = """
        UPDATE orders
        SET customer_id = %s,
            employee_id = %s,
            order_date = %s,
            required_date = %s,
            shipped_date = %s,
            ship_via = %s,
            freight = %s,
            ship_name = %s,
            ship_address = %s,
            ship_city = %s,
            ship_region = %s,
            ship_postal_code = %s,
            ship_country = %s
        WHERE order_id = %s
      """
      self.db.cursor.execute(query, (new_customer_id, new_employee_id, new_order_date, new_required_date, new_shipped_date, new_ship_via, new_freight, new_ship_name, new_ship_address, new_ship_city, new_ship_region, new_ship_postal_code, new_ship_country, order_id))

      self.db.connection.commit()
      print(f"Order ID {order_id} has been updated successfully.")
    except Exception as e:
      self.db.connection.rollback()
      print(f"Error during edition: {e}")

  def delete_order(self):
    orders = self.view_orders()
    if not orders:
        return

    order_id_input = input("Enter Order ID to delete (or 'b' to go back): ").strip().lower()
    if order_id_input == 'b':
        return
    if not order_id_input.isdigit():
        print("Invalid ID")
        return

    order_id = int(order_id_input)
    self.db.cursor.execute(
        "SELECT customer_id, employee_id FROM orders WHERE order_id = %s",
        (order_id,)
    )
    order = self.db.cursor.fetchone()
    if not order:
        print(f"No order found with ID {order_id}.")
        return

    cust_id, emp_id = order
    confirm = input(f"Are you sure you want to delete order {order_id} for customer {cust_id} handled by employee {emp_id}? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled")
        return

    self.db.cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    self.db.connection.commit()
    print(f"Order ID {order_id} has been deleted successfully.")
  
  def search_orders_by_date(self):
    try:
      start_date = input("Enter start date (YYYY-MM-DD): ").strip()
      end_date = input("Enter end date (YYYY-MM-DD): ").strip()

      if not start_date or not end_date:
        print("Both dates are required.")
        return

      query = """
        SELECT order_id, customer_id, employee_id, order_date, shipped_date, ship_country
        FROM orders
        WHERE shipped_date BETWEEN %s AND %s
        ORDER BY shipped_date
      """
      self.db.cursor.execute(query, (start_date, end_date))
      rows = self.db.cursor.fetchall()

      if not rows:
        print(f"No orders delivered between {start_date} and {end_date}.")
      else:
        print(f"\nOrders delivered between {start_date} and {end_date}:")
        for row in rows:
          order_id, customer_id, employee_id, order_date, shipped_date, ship_country = row
          print(f"Order ID: {order_id}, Customer: {customer_id}, Employee: {employee_id}, Ordered: {order_date}, Delivered: {shipped_date}, Country: {ship_country}")

    except Exception as e:
      print(f"Error while searching orders: {e}")
  
  def orders_manager(self):
    while True:
      print("\n ======================= Orders Manager =======================")
      print("1. View Orders\n2. View Orders in detail\n3. Add an Order\n4. Edit an Order\n5. Delete an Order\n6. Search Orders by date\n7. Go Back")

      choice = input("Enter your choice: ").strip()

      if choice == "1":
        self.view_orders()
      elif choice == "2":
        self.view_order_details()
      elif choice == "3":
        self.add_order()
      elif choice == "4":
        self.edit_order()
      elif choice == "5":
        self.delete_order()
      elif choice == "6":
        self.search_orders_by_date()
      elif choice == "7":
        print("Going back...")
        return
      else:
        print("Invalid choice. Please select again.")