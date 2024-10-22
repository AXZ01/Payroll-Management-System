from entities.employee import Employee
from utils.DBConnUtil import DBConnUtil
from exceptions.custom_exceptions import EmployeeNotFoundException
from dao.employee_service_interface import IEmployeeService  # Import the interface


class EmployeeService(IEmployeeService):
    def __init__(self, config_file):
        self.conn = DBConnUtil.get_connection(config_file)

    def get_employee_by_id(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM Employee WHERE EmployeeID=?", (employee_id,))
        row = cursor.fetchone()
        if row:
            return Employee(*row)
        else:
            raise EmployeeNotFoundException(
                f"Employee with ID {employee_id} not found.")

    def add_employee(self, employee_data):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO Employee (FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address, Position, JoiningDate, TerminationDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                employee_data.FirstName,
                employee_data.LastName,
                employee_data.DateOfBirth,
                employee_data.Gender,
                employee_data.Email,
                employee_data.PhoneNumber,
                employee_data.Address,
                employee_data.Position,
                employee_data.JoiningDate,
                employee_data.TerminationDate,
            )
        )
        self.conn.commit()

    def update_employee(self, employee_data):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE Employee 
            SET FirstName=?, LastName=?, DateOfBirth=?, Gender=?, Email=?, PhoneNumber=?, Address=?, Position=?, JoiningDate=?, TerminationDate=? 
            WHERE EmployeeID=?
            """,
            (
                employee_data.FirstName,
                employee_data.LastName,
                employee_data.DateOfBirth,
                employee_data.Gender,
                employee_data.Email,
                employee_data.PhoneNumber,
                employee_data.Address,
                employee_data.Position,
                employee_data.JoiningDate,
                employee_data.TerminationDate,
                employee_data.EmployeeID
            )
        )
        self.conn.commit()

    def remove_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM Payroll WHERE EmployeeID=?", (employee_id,))
        cursor.execute("DELETE FROM Tax WHERE EmployeeID=?", (employee_id,))
        cursor.execute(
            "DELETE FROM FinancialRecord WHERE EmployeeID=?", (employee_id,))
        cursor.execute(
            "DELETE FROM Employee WHERE EmployeeID=?", (employee_id,))
        self.conn.commit()

    def get_all_employees(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Employee")
        rows = cursor.fetchall()
        employees = [Employee(*row) for row in rows]
        return employees
