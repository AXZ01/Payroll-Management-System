# dao/payroll_service.py
from utils.DBConnUtil import DBConnUtil
from exceptions.custom_exceptions import EmployeeNotFoundException, PayrollNotFoundException


class PayrollService:
    def __init__(self, config_file):
        self.conn = DBConnUtil.get_connection(config_file)

    def net_salary(self, employee_id):
        cursor = self.conn.cursor()

        # Check if a payroll record already exists for the employee
        cursor.execute("""
            SELECT NetSalary
            FROM Payroll
            WHERE EmployeeID = ?
        """, (employee_id,))

        existing_payroll = cursor.fetchone()

        if existing_payroll:
            # If a payroll record exists, return the existing net salary
            print(f"Payroll already exists for Employee ID: {
                  employee_id}. Net Salary: {existing_payroll[0]}")
            return existing_payroll[0]
        else:
            return -1

    def generate_payroll(self, employee_id, basic_salary, overtime_hours, overtime_rate, deductions, pay_period_start, pay_period_end):
        cursor = self.conn.cursor()

        # Calculate Overtime Pay
        overtime_pay = overtime_hours * overtime_rate

        # Calculate Total Salary
        net_salary = basic_salary + overtime_pay - deductions

        # Insert the payroll record into the Payroll table
        cursor.execute("""
            INSERT INTO Payroll (EmployeeID, PayPeriodStartDate, PayPeriodEndDate, BasicSalary, OvertimePay, Deductions, NetSalary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (employee_id, pay_period_start, pay_period_end, basic_salary, overtime_pay, deductions, net_salary))

        self.conn.commit()
        return net_salary

    def generate_pay_stub(self, employee_id, pay_period_start, pay_period_end):
        cursor = self.conn.cursor()

        # Fetch employee details
        cursor.execute(
            "SELECT * FROM Employee WHERE EmployeeID=?", (employee_id,))
        employee = cursor.fetchone()

        if not employee:
            raise EmployeeNotFoundException(
                f"Employee with ID {employee_id} not found.")

        # Fetch payroll details
        cursor.execute("""
            SELECT BasicSalary, OvertimePay, Deductions, NetSalary
            FROM Payroll
            WHERE EmployeeID = ? AND PayPeriodStartDate = ? AND PayPeriodEndDate = ?
        """, (employee_id, pay_period_start, pay_period_end))

        payroll = cursor.fetchone()

        if not payroll:
            raise PayrollNotFoundException(f"Payroll data for employee ID {
                                           employee_id} not found for the given pay period.")

        # Create pay stub string (customize the format as per your requirements)
        pay_stub = f"""
        Pay Stub for Employee ID: {employee_id}
        Name: {employee[1]} {employee[2]} (Position: {employee[8]})
        Pay Period: {pay_period_start} to {pay_period_end}
        --------------------------------------
        Basic Salary: ${payroll[0]:.2f}
        Overtime Pay: ${payroll[1]:.2f}
        Deductions: ${payroll[2]:.2f}
        Net Salary: ${payroll[3]:.2f}
        --------------------------------------
        """

        return pay_stub

    def get_payroll_by_id(self, payroll_id):
        cursor = self.conn.cursor()

        # Retrieve payroll record by payroll ID
        cursor.execute(
            "SELECT * FROM Payroll WHERE PayrollID = ?", (payroll_id,))
        payroll_record = cursor.fetchone()

        if not payroll_record:
            raise PayrollNotFoundException(
                f"Payroll with ID {payroll_id} not found.")

        return payroll_record

    def get_payrolls_for_all_employees(self):
        cursor = self.conn.cursor()

        # Retrieve payrolls along with employee details
        cursor.execute("""
            SELECT p.BasicSalary, p.OvertimePay, p.Deductions, p.NetSalary, p.PayPeriodStartDate, p.PayPeriodEndDate, 
                   e.EmployeeID, e.FirstName, e.LastName, e.Position
            FROM Payroll p
            JOIN Employee e ON p.EmployeeID = e.EmployeeID
        """)

        payrolls = cursor.fetchall()

        # Loop through payrolls and print in the desired format
        for payroll in payrolls:
            employee_id = payroll[6]
            employee_name = f"{payroll[7]} {payroll[8]}"
            position = payroll[9]
            pay_period_start = payroll[4]
            pay_period_end = payroll[5]
            basic_salary = payroll[0]
            overtime_pay = payroll[1]
            deductions = payroll[2]
            net_salary = payroll[3]

            # Display the payroll in the requested format
            print(f"\nPay Stub for Employee ID: {employee_id}")
            print(f"Name: {employee_name} (Position: {position})")
            print(f"Pay Period: {pay_period_start} to {pay_period_end}")
            print("--------------------------------------")
            print(f"Basic Salary: ${basic_salary:.2f}")
            print(f"Overtime Pay: ${overtime_pay:.2f}")
            print(f"Deductions: ${deductions:.2f}")
            print(f"Net Salary: ${net_salary:.2f}")
            print("--------------------------------------")

        return payrolls

    def get_payrolls_for_period(self, start_date, end_date):
        cursor = self.conn.cursor()

        # Retrieve payrolls within the given date range
        cursor.execute("""
            SELECT * FROM Payroll
            WHERE PayPeriodStartDate >= ? AND PayPeriodEndDate <= ?
        """, (start_date, end_date))

        payrolls = cursor.fetchall()

        if not payrolls:
            raise PayrollNotFoundException(f"No payrolls found for the period between {
                                           start_date} and {end_date}.")

        return payrolls

    def calculate_gross_salary(self, employee_id, basic_salary, allowances):
        # Example implementation for calculating gross salary
        return basic_salary + allowances

    def calculate_net_salary(self, employee_id, gross_salary, deductions):
        # Example implementation for calculating net salary
        return gross_salary - deductions

    def calculate_tax(self, employee_id, gross_salary):
        # Example implementation for tax calculation (25% rate)
        tax_rate = 0.25
        return gross_salary * tax_rate

    def process_payroll(self, employee_ids):
        # Example implementation to process payroll for multiple employees
        results = {}
        for emp_id in employee_ids:
            # This is just a mock example; you should replace it with actual data fetching
            basic_salary = 5000
            allowances = 2000
            deductions = 1500
            gross_salary = self.calculate_gross_salary(
                emp_id, basic_salary, allowances)
            net_salary = self.calculate_net_salary(
                emp_id, gross_salary, deductions)
            tax = self.calculate_tax(emp_id, gross_salary)
            results[emp_id] = {
                'gross_salary': gross_salary,
                'net_salary': net_salary,
                'tax': tax
            }
        return results

    def get_employee_by_id(self, employee_id):
        # Simulating fetching employee by ID
        if employee_id != '1':
            # Simulate error for invalid ID
            raise Exception("Employee not found")
        return {"id": employee_id, "name": "John Doe"}
