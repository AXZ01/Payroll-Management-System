# dao/tax_service.py

from exceptions.custom_exceptions import TaxNotFoundException
from entities.tax import Tax
from utils.DBConnUtil import DBConnUtil
from abc import ABC, abstractmethod
from exceptions.custom_exceptions import EmployeeNotFoundException
from decimal import Decimal


class ITaxService(ABC):
    @abstractmethod
    def calculate_tax(self, employee_id, taxable_income, tax_rate):
        pass

    @abstractmethod
    def get_tax_by_id(self, tax_id):
        pass

    @abstractmethod
    def get_taxes_for_employee(self, employee_id):
        pass

    @abstractmethod
    def get_taxes_for_year(self, tax_year):
        pass


class TaxService(ITaxService):
    def __init__(self, config_file):
        self.conn = DBConnUtil.get_connection(
            config_file)  # Directly call the static method

    def calculate_tax(self, employee_id):
        cursor = self.conn.cursor()

        # Check if a payroll record already exists for the employee
        cursor.execute("""
            SELECT NetSalary
            FROM Payroll
            WHERE EmployeeID = ?
        """, employee_id)

        result = cursor.fetchone()

        if result:
            # Extract NetSalary from the result
            taxable_income = result.NetSalary if 'NetSalary' in result else result[0]

            # Convert taxable_income to Decimal if needed
            if not isinstance(taxable_income, Decimal):
                taxable_income = Decimal(taxable_income)

            # Determine the tax rate based on taxable income
            if taxable_income < Decimal('3000'):
                tax_rate = Decimal('0.03')
            elif Decimal('3000') <= taxable_income < Decimal('50000'):
                tax_rate = Decimal('0.05')
            else:
                tax_rate = Decimal('0.10')

            # Calculate the tax amount using Decimal
            tax_amount = taxable_income * tax_rate

            # Insert the calculated tax into the database
            cursor.execute("""
                INSERT INTO Tax (EmployeeID, TaxYear, TaxableIncome, TaxAmount)
                VALUES (?, YEAR(GETDATE()), ?, ?)
            """, employee_id, taxable_income, tax_amount)

            self.conn.commit()
            print(f"Tax for Employee {employee_id} calculated and saved: {tax_amount}")
        else:
            raise EmployeeNotFoundException(
                f"Employee with ID {employee_id} not found.")

    def get_tax_by_id(self, tax_id):
        cursor = self.conn.cursor()

        # Retrieve the tax record by ID
        cursor.execute("SELECT * FROM Tax WHERE TaxID = ?", tax_id)
        tax_record = cursor.fetchone()

        if not tax_record:
            raise TaxNotFoundException(f"Tax with ID {tax_id} not found.")

        return tax_record

    def get_taxes_for_employee(self, employee_id):
        cursor = self.conn.cursor()

        # Retrieve all tax records for a specific employee
        cursor.execute("SELECT * FROM Tax WHERE EmployeeID = ?", employee_id)
        taxes = cursor.fetchall()

        if not taxes:
            raise TaxNotFoundException(
                f"No taxes found for Employee ID {employee_id}.")

        return taxes

    def get_taxes_for_year(self, tax_year):
        cursor = self.conn.cursor()

        # Retrieve all tax records for a specific year
        cursor.execute("SELECT * FROM Tax WHERE TaxYear = ?", tax_year)
        taxes = cursor.fetchall()

        if not taxes:
            raise TaxNotFoundException(f"No taxes found for the year {tax_year}.")

        return taxes
