from db_connect import DataConnect

class Customers:
  def __init__(self):
    self.db = DataConnect()
  
  def view_customers(self):
    query = """
      SELECT customer_id, company_name, contact_name FROM customers
    """
    self.db.cursor.execute(query, ())

    rows = self.db.cursor.fetchall()

    if not rows:
      print("no customer can be found")
    else:
      print("\n========= CUSTOMERS =========")

      for row in rows:
        customer_id = row[0]
        contact_name = row[2]
        company_name = row[1]
        print(f"{customer_id}. {contact_name} from company '{company_name}'")
    
    return rows
  
  def view_customer_details(self):
    self.view_customers()
    while True:
      cust_id = input("enter the CUSTOMER ID to view details (or type 'b' to go back): ").strip()

      if cust_id == 'b':
        print("Going back...")
        return
      
      query = """
        SELECT customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax
        FROM customers
        WHERE customer_id = %s
      """
      self.db.cursor.execute(query, (cust_id, ))
      customer = self.db.cursor.fetchone()

      if not customer:
        print(f"No customer found with ID {cust_id}. Try again or type 'b' to go back.")
      else:
        print("\n========= CUSTOMER DETAILS =========")
        fields = [
            "Customer ID", "Company Name", "Contact Name", "Contact Title", "Address",
            "City", "Region", "Postal Code",
            "Country", "Phone", "Fax"
        ]
        for field, value in zip(fields, customer):
            print(f"{field}: {value}")
  
  def add_customer(self, customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax):
    query = """
      INSERT INTO customers
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    self.db.cursor.execute(query, (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax))
    self.db.connection.commit()
    print(f"Customer {contact_name} from company {company_name} has been added successfully")
  
  def edit_customer(self, customer_id):
    self.db.cursor.execute("""
        SELECT company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax
        FROM customers
        WHERE customer_id = %s
    """, (customer_id,))
    customer = self.db.cursor.fetchone()

    if not customer:
        print(f"No customer found with ID {customer_id}.")
        return

    (company_name, contact_name, contact_title, address, city, region,
     postal_code, country, phone, fax) = customer

    try:
        print(f"\nEditing Customer '{contact_name}' from '{company_name}'")

        new_company_name = input(f"(Current Company Name: {company_name})\nNew Company Name (or leave blank to keep current): ").strip() or company_name
        new_contact_name = input(f"(Current Contact Name: {contact_name})\nNew Contact Name (or leave blank to keep current): ").strip() or contact_name
        new_contact_title = input(f"(Current Contact Title: {contact_title})\nNew Contact Title (or leave blank to keep current): ").strip() or contact_title
        new_address = input(f"(Current Address: {address})\nNew Address (or leave blank to keep current): ").strip() or address
        new_city = input(f"(Current City: {city})\nNew City (or leave blank to keep current): ").strip() or city
        new_region = input(f"(Current Region: {region})\nNew Region (or leave blank to keep current): ").strip() or region
        new_postal_code = input(f"(Current Postal Code: {postal_code})\nNew Postal Code (or leave blank to keep current): ").strip() or postal_code
        new_country = input(f"(Current Country: {country})\nNew Country (or leave blank to keep current): ").strip() or country
        new_phone = input(f"(Current Phone: {phone})\nNew Phone (or leave blank to keep current): ").strip() or phone
        new_fax = input(f"(Current Fax: {fax})\nNew Fax (or leave blank to keep current): ").strip() or fax

        query = """
            UPDATE customers
            SET company_name = %s,
                contact_name = %s,
                contact_title = %s,
                address = %s,
                city = %s,
                region = %s,
                postal_code = %s,
                country = %s,
                phone = %s,
                fax = %s
            WHERE customer_id = %s
        """
        self.db.cursor.execute(query, (
            new_company_name, new_contact_name, new_contact_title,
            new_address, new_city, new_region, new_postal_code,
            new_country, new_phone, new_fax, customer_id
        ))

        self.db.connection.commit()
        print(f"Customer '{new_contact_name}' from '{new_company_name}' has been updated successfully.")

    except Exception as e:
        self.db.connection.rollback()
        print(f"Error during update: {e}")
  
  def delete_customer(self):
    customers = self.view_customers()
    if not customers:
      return
    
    cust_id_input = input("Enter Customer ID to delete or ('b' to go back): ")
    if cust_id_input == 'b':
      return
    
    self.db.cursor.execute("SELECT contact_name, company_name FROM customers WHERE customer_id = %s", (cust_id_input, ))
    customer = self.db.cursor.fetchone()
    if not customer:
      print(f"No Customer found with ID {cust_id_input}")
      return
    
    contact_name, company_name = customer
    confirm = input(f"Are you sure you want to delete {contact_name} from {company_name}? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled")
        return

    self.db.cursor.execute("DELETE FROM customers WHERE customer_id = %s", (cust_id_input, ))
    self.db.connection.commit()
    print(f"Customer {contact_name} from Company {company_name} has been deleted successfully")

  def get_input(self, prompt, allow_null=False):
    value = input(prompt).strip()
    if allow_null and value == "":
        return None
    return value
  
  def customer_manager(self):
    while True:
      print("======================= Customer Manager =======================")
      print("1. View Customers\n2. View Customers in detail\n3. Add a customer\n4. Edit a customer\n5. Delete a customer\n6. Go Back")

      choice = input("Enter your choice: ").strip()

      if choice == "1":
        self.view_customers()
      elif choice == "2":
        self.view_customer_details()
      elif choice == "3":
        customer_id = input("Customer ID: ")
        company_name = input("Company Name: ")
        contact_name = input("Contact Name: ")
        contact_title = input("Contact Title: ")
        address = input("Address: ")
        city = input("City: ")
        region = self.get_input("Region: ", allow_null=True)
        postal_code = input("Postal Code: ")
        country = input("Country: ")
        phone = input("Phone: ")
        fax = self.get_input("Fax: ", allow_null=True)

        self.add_customer(customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
      elif choice == "4":
        self.view_customers()
        cust_id_input = input("Enter the Customer ID you want to edit: ").strip()
        self.edit_customer(cust_id_input)
      elif choice == "5":
        self.delete_customer()
      elif choice == '6':
        break
      else:
        print("Invalid choice. Try again.")