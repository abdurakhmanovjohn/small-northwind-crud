# employees, orders, customers jadvallariga CRUD yozib kelish
# 1ta orderni ko'ryotganda -> order_detailsni to'la ko'rish
# 2ta sana qabul qilib, mana shu sana oraligidagi orderlar ro'yxatini chiqarib kelish

from employees import Employees
from customers import Customers
from orders import Orders

def main():
  employees = Employees()
  customers = Customers()
  orders = Orders()

  while True:
    print("\n ======================= The Manager =======================")
    print("1. Employees Manager\n2. Customers Manager\n3. Orders Manager\n4. Exit")
    
    choice = input("Enter your choice: ").strip()
    if choice == "1":
      employees.employee_manager()
    elif choice == "2":
      customers.customer_manager()
    elif choice == "3":
      orders.orders_manager()
    elif choice == "4":
      print("Exiting the program...")
      break
    else:
      print("Invalid choice. Please select again.")

if __name__ == "__main__":
  main()