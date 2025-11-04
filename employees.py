from db_connect import DataConnect

class Employees:
  def __init__(self):
    self.db = DataConnect()

  def view_employees(self):
    query = "SELECT employee_id, last_name, first_name, title, title_of_courtesy FROM employees"
    self.db.cursor.execute(query)

    rows = self.db.cursor.fetchall()

    if not rows:
      print("no employee can be found")
    else:
      print("\n========= EMPLOYEES =========")

      for row in rows:
        employee_id = row[0]
        last_name = row[1]
        first_name = row[2]
        title = row[3]
        title_of_courtesy = row[4]
        print(f"{employee_id}. {title_of_courtesy} {first_name} {last_name}, {title}")
    
    return rows

  def view_employee_details(self):
    self.view_employees()
    while True:
      user_choice = input("enter the EMPLOYEE ID to view details (or type 'b' to go back): ").strip().lower()

      if user_choice == 'b':
        print("Going back...")
        return
      
      if not user_choice.isdigit():
          print("Invalid input. Please enter a number or 'b' to go back.")
          continue
      
      emp_id = int(user_choice)
      query = """
        SELECT employee_id, last_name, first_name, title, title_of_courtesy,
               birth_date, hire_date, address, city, region, postal_code,
               country, home_phone, extension, photo, notes
        FROM employees
        WHERE employee_id = %s
      """
      self.db.cursor.execute(query, (emp_id,))
      employee = self.db.cursor.fetchone()

      if not employee:
          print(f"No employee found with ID {emp_id}. Try again or type 'b' to go back.")
      else:
          print("\n========= EMPLOYEE DETAILS =========")
          fields = [
              "Employee ID", "Last Name", "First Name", "Title", "Title of Courtesy",
              "Birth Date", "Hire Date", "Address", "City", "Region", "Postal Code",
              "Country", "Home Phone", "Extension", "Photo", "Notes"
          ]
          for field, value in zip(fields, employee):
              print(f"{field}: {value}")

          input("\nPress Enter to continue...")
          return
  
  def add_employee(self,last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes):
    query = """
      INSERT INTO employees (last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes)
      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    self.db.cursor.execute(query, (last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes))
    self.db.connection.commit()
    print(f"Employee {title_of_courtesy} {first_name} {last_name} has been added successfully")
  
  def edit_employee(self, employee_id):
    self.db.cursor.execute("""
        SELECT last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes
        FROM employees
        WHERE employee_id = %s
    """, (employee_id,))
    employee = self.db.cursor.fetchone()

    if not employee:
      print(f"No employee found with ID {employee_id}.")
      return
    
    (last_name, first_name, title, title_of_courtesy, birth_date, hire_date,
     address, city, region, postal_code, country, home_phone, extension, photo, notes) = employee
    
    try:
      print(f"\nEditing Employee '{title_of_courtesy} {first_name} {last_name}'")

      new_last_name = input(f"(Current Last Name: {last_name})\nNew Last Name (or leave blank to keep current): ").strip() or last_name
      new_first_name = input(f"(Current First Name: {first_name})\nNew First Name (or leave blank to keep current): ").strip() or first_name
      new_title = input(f"(Current Title: {title})\nNew Title (or leave blank to keep current): ").strip() or title
      new_title_of_courtesy = input(f"(Current Title of Courtesy: {title_of_courtesy})\nNew Title of Courtesy (or leave blank to keep current): ").strip() or title_of_courtesy
      new_birth_date = input(f"(Current Birth Date: {birth_date})\nNew Birth Date (YYYY-MM-DD, or leave blank to keep current): ").strip() or birth_date
      new_hire_date = input(f"(Current Hire Date: {hire_date})\nNew Hire Date (YYYY-MM-DD, or leave blank to keep current): ").strip() or hire_date
      new_address = input(f"(Current Address: {address})\nNew Address (or leave blank to keep current): ").strip() or address
      new_city = input(f"(Current City: {city})\nNew City (or leave blank to keep current): ").strip() or city
      new_region = input(f"(Current Region: {region})\nNew Region (or leave blank to keep current): ").strip() or region
      new_postal_code = input(f"(Current Postal Code: {postal_code})\nNew Postal Code (or leave blank to keep current): ").strip() or postal_code
      new_country = input(f"(Current Country: {country})\nNew Country (or leave blank to keep current): ").strip() or country
      new_home_phone = input(f"(Current Home Phone: {home_phone})\nNew Home Phone (or leave blank to keep current): ").strip() or home_phone
      new_extension = input(f"(Current Extension: {extension})\nNew Extension (or leave blank to keep current): ").strip() or extension
      new_photo = input(f"(Current Photo: {photo})\nNew Photo (or leave blank to keep current): ").strip() or photo
      new_notes = input(f"(Current Notes: {notes})\nNew Notes (or leave blank to keep current): ").strip() or notes

      query = """
        UPDATE employees
        SET last_name = %s,
            first_name = %s,
            title = %s,
            title_of_courtesy = %s,
            birth_date = %s,
            hire_date = %s,
            address = %s,
            city = %s,
            region = %s,
            postal_code = %s,
            country = %s,
            home_phone = %s,
            extension = %s,
            photo = %s,
            notes = %s
        WHERE employee_id = %s
      """
      self.db.cursor.execute(query, (new_last_name, new_first_name, new_title, new_title_of_courtesy, new_birth_date, new_hire_date, new_address, new_city, new_region, new_postal_code, new_country, new_home_phone, new_extension, new_photo, new_notes, employee_id))

      self.db.connection.commit()
      print(f"Employee ID {employee_id} has been updated successfully")

    except Exception as e:
      self.db.connection.rollback()
      print(f"Error during edition: {e}")
  
  def delete_employee(self):
    employees = self.view_employees()
    if not employees:
        return

    emp_id_input = input("Enter employee ID to delete (or 'b' to go back): ").strip().lower()
    if emp_id_input == 'b':
        return
    if not emp_id_input.isdigit():
        print("Invalid ID")
        return

    emp_id = int(emp_id_input)
    self.db.cursor.execute(
        "SELECT title_of_courtesy, first_name, last_name FROM employees WHERE employee_id = %s",
        (emp_id,)
    )
    emp = self.db.cursor.fetchone()
    if not emp:
        print(f"No employee found with ID {emp_id}.")
        return

    title, first, last = emp
    confirm = input(f"Are you sure you want to delete {title} {first} {last}? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled")
        return

    self.db.cursor.execute("DELETE FROM employees WHERE employee_id = %s", (emp_id,))
    self.db.connection.commit()
    print(f"Employee '{title} {first} {last}' deleted successfully.")
  
  def get_input(self, prompt, allow_null=False):
    value = input(prompt).strip()
    if allow_null and value == "":
        return None
    return value
  
  def employee_manager(self):
    while True:
      print("\n ======================= Employees Manager =======================")
      print("1. View Employees\n2. View Employees in detail\n3. Add an Employee\n4. Edit an Employee\n5. Delete an Employee\n6. Go Back")
      
      choice = input("Enter your choice: ").strip()

      if choice == "1":
        self.view_employees()
      elif choice == "2":
         self.view_employee_details()
      elif choice == "3":
        last_name = input("Last Name: ")
        first_name = input("First Name: ")
        title = input("Title: ")
        title_of_courtesy = input("Title of Courtesy: ")
        birth_date = input("Birthdate: ")
        hire_date = input("Hire Date: ")
        address = input("Address: ")
        city = input("City: ")
        region = self.get_input("Region: ", allow_null=True)
        postal_code = input("Postal Code: ")
        country = input("Country: ")
        home_phone = input("Home Phone: ")
        extension = input("Extension: ")
        photo = self.get_input("Photo: ", allow_null=True)
        notes = self.get_input("Notes: ", allow_null=True)

        self.add_employee(last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes)
      elif choice == "4":
        self.view_employees()
        emp_id_input = input("Enter the Employee ID you want to edit: ").strip()
        if not emp_id_input.isdigit():
            print("Invalid Employee ID")
        else:
            emp_id = int(emp_id_input)
            self.edit_employee(emp_id)
      elif choice == "5":
         self.delete_employee()
      elif choice == '6':
        break
      else:
        print("Invalid choice. Try again.")