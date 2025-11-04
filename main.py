# employees, orders, customers jadvallariga CRUD yozib kelish
# 1ta orderni ko'ryotganda -> order_detailsni to'la ko'rish
# 2ta sana qabul qilib, mana shu sana oraligidagi orderlar ro'yxatini chiqarib kelish

from employees import Employees
from customers import Customers

if __name__ == "__main__":
  employees = Employees()
  # # employees.view_employees()
  # employees.view_employee_details()
  # # employees.delete_employee(2, 'Mr.', 'Andrew', 'Fuller')
  # employees.employee_manager()
  # employees.employee_manager()

  customers = Customers()
  customers.customer_manager()