# Write a Python class Employee with attributes
# like emp_id, emp_name, emp_salary, and emp_department
# and methods like calculate_emp_salary, emp_assign_department,
# and print_employee_details.
# Sample Employee Data:
# "ADAMS", "E7876", 50000, "ACCOUNTING"
# "JONES", "E7499", 45000, "RESEARCH"
# "MARTIN", "E7900", 50000, "SALES"
# "SMITH", "E7698", 55000, "OPERATIONS"

class employee:
    def __init__(self, emp_name, emp_id, emp_salary, emp_dpt):
        self.emp_name = emp_name
        self.emp_id = emp_id
        self.emp_salary = emp_salary
        self.emp_dpt = emp_dpt

    def calculate_emp_salary(self):
        annual_salary = self.emp_salary * 12
        return annual_salary

    def emp_assign_department(self):
        return self.emp_dpt

employee_details = employee("ADAMS", "E7876", 50000,
                             "ACCOUNTING")


print('the employee name is {}\n'.format(
    employee_details.emp_name),
      'the employee id is {}\n'.format(employee_details.emp_id),
    'the employee annual salary is {}\n'.format(
        employee_details.calculate_emp_salary()), 'the '
                                                  'department '
                                                  'is {'
                                                  '}\n'.format(
        employee_details.emp_assign_department()))

print('----------')

employee_details = employee("JONES", "E7499", 45000, "RESEARCH")
print('the employee name is {}\n'.format(
    employee_details.emp_name),
      'the employee id is {}\n'.format(employee_details.emp_id),
    'the employee annual salary is {}\n'.format(
        employee_details.calculate_emp_salary()), 'the '
                                                  'department '
                                                  'is {'
                                                  '}\n'.format(
        employee_details.emp_assign_department()))

print('----------')

employee_details = employee("MARTIN", "E7900", 50000, "SALES")
print('the employee name is {}\n'.format(
    employee_details.emp_name),
      'the employee id is {}\n'.format(employee_details.emp_id),
    'the employee annual salary is {}\n'.format(
        employee_details.calculate_emp_salary()), 'the '
                                                  'department '
                                                  'is {'
                                                  '}\n'.format(
        employee_details.emp_assign_department()))