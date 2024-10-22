from dao.employee_service import EmployeeService
from dao.payroll_service import PayrollService
from dao.tax_service import TaxService
from dao.financial_reporting_service import FinancialRecordService
from entities.employee import Employee
from datetime import datetime
from entities.financial_record import FinancialRecord
from utils.DBConnUtil import DBConnUtil


def print_employee_details(employee):
    print("\n--- Employee Details ---")
    print(f"Employee ID: {employee.EmployeeID}")
    print(f"Name: {employee.FirstName} {employee.LastName}")
    print(f"DOB: {employee.DateOfBirth.strftime('%Y-%m-%d')}")
    print(f"Gender: {employee.Gender}")
    print(f"Email: {employee.Email}")
    print(f"Phone Number: {employee.PhoneNumber}")
    print(f"Address: {employee.Address}")
    print(f"Position: {employee.Position}")
    print(f"Joining Date: {employee.JoiningDate.strftime('%Y-%m-%d')}")
    print("-------------------------\n")


def print_pay_stub(pay_stub):
    print("\n--- Pay Stub ---")
    print(f"Employee ID: {pay_stub['EmployeeID']}")
    print(f"Name: {pay_stub['EmployeeName']}")
    print(f"Pay Period: {pay_stub['PayPeriodStart']} to {pay_stub['PayPeriodEnd']}")
    print(f"Basic Salary: ${pay_stub['BasicSalary']:.2f}")
    print(f"Overtime: {pay_stub['OvertimeHours']} hours @ ${pay_stub['OvertimeRate']:.2f}/hr")
    print(f"Deductions: ${pay_stub['Deductions']:.2f}")
    print(f"Net Salary: ${pay_stub['NetSalary']:.2f}")
    print("-------------------------\n")



def print_financial_record(record):
    print("\n--- Financial Record ---")
    print(f"Record ID: {record.RecordID}")
    print(f"Employee ID: {record.EmployeeID}")
    print(f"Date: {record.RecordDate.strftime('%Y-%m-%d')}")
    print(f"Amount: ${record.Amount:.2f}")
    print(f"Type: {record.RecordType}")
    print("-------------------------\n")


def main_menu():
    # Path to the properties file
    config_file = 'config/db_config.properties'
    employee_service = EmployeeService(config_file)

    # Initialize services
    payroll_service = PayrollService(config_file)
    tax_service = TaxService(config_file)
    financial_reporting_service = FinancialRecordService(config_file)

    while True:
        print("\nWelcome to the Payroll Management System")
        print("Please select an option:")
        print("1. Add Employee")
        print("2. View Employee by ID")
        print("3. View All Employees")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Calculate Salary")
        print("7. Generate Pay Stub")
        print("8. Generate Pay Stub by Payroll ID")
        print("9. Generate Pay Stub for All Employees")
        print("10. Calculate Tax")
        print("11. Calculate Tax by ID")
        print("12. Calculate Tax by Year")
        print("13. Add Financial Record")
        print("14. View Financial Record by ID")
        print("15. View Financial Records for Employee")
        print("16. View Financial Records for Date")
        print("17. Exit The System")

        choice = input("Enter your choice: ")

        # Option 1: Add Employee
        if choice == '1':
            print("\nAdding a new employee...")
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            dob = datetime.strptime(
                input("Enter Date of Birth (YYYY-MM-DD): "), "%Y-%m-%d")
            gender = input("Enter Gender: ")
            email = input("Enter Email: ")
            phone = input("Enter Phone Number: ")
            address = input("Enter Address: ")
            position = input("Enter Position: ")
            joining_date = datetime.strptime(
                input("Enter Joining Date (YYYY-MM-DD): "), "%Y-%m-%d")

            employee = Employee(None, first_name, last_name, dob,
                                gender, email, phone, address, position, joining_date)
            employee_service.add_employee(employee)
            print("\nEmployee added successfully! Thank you.")

        # Option 2: View Employee by ID
        elif choice == '2':
            employee_id = input("Enter Employee ID: ")
            print("Fetching employee details, please wait...")
            try:
                employee = employee_service.get_employee_by_id(employee_id)
                print_employee_details(employee)
                print("Thank you for using the system.")
            except Exception as e:
                print(f"Error: {str(e)}")

        # Option 3: View All Employees
        elif choice == '3':
            print("Fetching all employee details, please wait...")
            employees = employee_service.get_all_employees()
            print("\n--- Employee List ---")
            for emp in employees:
                print(f"{emp.EmployeeID}: {emp.FirstName} {emp.LastName}")
            print("-------------------------\nThank you for using the system.")

        # Option 4: Update Employee
        elif choice == '4':
            employee_id = input("Enter Employee ID to update: ")
            print("Fetching current employee details, please wait...")
            try:
                employee = employee_service.get_employee_by_id(employee_id)

                print("\nEnter new details (Leave blank to keep current value):")

                employee.FirstName = input(
                    f"First Name [{employee.FirstName}]: ") or employee.FirstName
                employee.LastName = input(
                    f"Last Name [{employee.LastName}]: ") or employee.LastName
                dob_input = input(f"Date of Birth [{employee.DateOfBirth}]: ")
                employee.DateOfBirth = datetime.strptime(
                    dob_input, "%Y-%m-%d") if dob_input else employee.DateOfBirth
                employee.Gender = input(
                    f"Gender [{employee.Gender}]: ") or employee.Gender
                employee.Email = input(
                    f"Email [{employee.Email}]: ") or employee.Email
                employee.PhoneNumber = input(
                    f"Phone Number [{employee.PhoneNumber}]: ") or employee.PhoneNumber
                employee.Address = input(
                    f"Address [{employee.Address}]: ") or employee.Address
                employee.Position = input(
                    f"Position [{employee.Position}]: ") or employee.Position
                joining_date_input = input(
                    f"Joining Date [{employee.JoiningDate}]: ")
                employee.JoiningDate = datetime.strptime(
                    joining_date_input, "%Y-%m-%d") if joining_date_input else employee.JoiningDate
                termination_date_input = input(
                    f"Termination Date [{employee.TerminationDate}]: ")
                employee.TerminationDate = datetime.strptime(
                    termination_date_input, "%Y-%m-%d") if termination_date_input else employee.TerminationDate

                employee_service.update_employee(employee)
                print("\nEmployee updated successfully! Thank you.")
            except Exception as e:
                print(f"Error: {str(e)}")

        # Option 5: Delete Employee
        elif choice == '5':
            employee_id = input("Enter Employee ID to delete: ")
            print("Processing deletion, please wait...")
            try:
                employee_service.remove_employee(employee_id)
                print("\nEmployee deleted successfully! Thank you.")
            except Exception as e:
                print(f"Error: {str(e)}")

        # Option 6: Calculate Salary
        elif choice == '6':
            employee_id = input("Enter Employee ID: ")
            print("Calculating salary, please wait...")
            x = payroll_service.net_salary(employee_id)
            if x != -1:
                print(f"\nNet Salary for Employee ID {employee_id}: ${x:.2f}")
            else:
                basic_salary = float(input("Enter Basic Salary: "))
                overtime_hours = float(input("Enter Overtime Hours: "))
                overtime_rate = float(input("Enter Overtime Rate: "))
                deductions = float(input("Enter Deductions: "))
                pay_period_start = input(
                    "Enter Pay Period Start Date (YYYY-MM-DD): ")
                pay_period_end = input(
                    "Enter Pay Period End Date (YYYY-MM-DD): ")
                y = payroll_service.generate_payroll(
                    employee_id, basic_salary, overtime_hours, overtime_rate, deductions, pay_period_start, pay_period_end)
                print(f"\nNet Salary for Employee ID {employee_id}: ${y:.2f}")

        # Option 7: Generate Pay Stub
        elif choice == '7':
            employee_id = input("Enter Employee ID: ")
            pay_period_start = input("Enter Pay Period Start Date (YYYY-MM-DD): ")
            pay_period_end = input("Enter Pay Period End Date (YYYY-MM-DD): ")

            try:
                # Call the generate_pay_stub method with required arguments
                pay_stub = payroll_service.generate_pay_stub(employee_id, pay_period_start, pay_period_end)
                print(pay_stub)
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '8':
            payroll_id = input("Enter Payroll ID: ")
            print("Fetching payroll record, please wait...")
            try:
                payroll_record = payroll_service.get_payroll_by_id(payroll_id)
                print(f"\nPayroll Record: {payroll_record}")
                print("Thank you for using the system.")
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '9':

            print("Generating pay stubs for all employees, please wait...")
            try:
                print("\n--- Pay Stubs ---")
                # Ensure this method exists
                pay_stubs = payroll_service.get_payrolls_for_all_employees()

                print("Thank you for using the system.")
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '10':
            employee_id = input("Enter Employee ID: ")
            print("Calculating tax, please wait...")
            try:
                tax = tax_service.calculate_tax(employee_id)
                print(f"\nTax for Employee ID {employee_id}: ${tax:.2f}")
                print("Thank you for using the system.")
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '11':
            employee_id = input("Enter Employee ID: ")
            print("Calculating tax, please wait...")
            try:
                tax = tax_service.calculate_tax(employee_id)
                print(f"\nTax for Employee ID {employee_id}: ${tax:.2f}")
                print("Thank you for using the system.")
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '12':
            tax_year = input("Enter Tax Year (YYYY): ")
            
            try:
                taxes = tax_service.get_taxes_for_year(tax_year)
                for tax in taxes:
                    print(tax)
            except Exception as e:
                print(str(e))

        elif choice == '13':
            # Add Financial Record
            employee_id = input("Enter Employee ID: ")
            record_date = datetime.strptime(input("Enter Record Date (YYYY-MM-DD): "), "%Y-%m-%d")
            description = input("Enter Description: ")
            amount = float(input("Enter Amount: "))
            record_type = input("Enter Record Type (e.g., Credit/Debit): ")

            financial_record = FinancialRecord(None, employee_id, record_date, description, amount, record_type)
            financial_reporting_service.add_financial_record(financial_record)
            print("Financial record added successfully.")

        elif choice == '14':
            record_id = input("Enter Financial Record ID: ")
            print("Fetching financial record, please wait...")
            try:
                financial_record = financial_reporting_service.get_financial_record_by_id(
                    record_id)
                print_financial_record(financial_record)
                print("Thank you for using the system.")
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '15':
            employee_id = input("Enter Employee ID: ")
            print("Fetching financial records, please wait...")
            try:
                records = financial_reporting_service.get_financial_records_for_employee(
                    employee_id)
                print("\n--- Financial Records ---")
                for record in records:
                    print_financial_record(record)
                print("Thank you for using the system.")
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '16':
            # View Financial Records for Date
            record_date = datetime.strptime(input("Enter Record Date (YYYY-MM-DD): "), "%Y-%m-%d")
            records = financial_reporting_service.get_financial_records_for_date(record_date)
            
            for record in records:
                print(record)  # Simply print the record if it's a tuple or list


        # Exit the system
        elif choice == '17':
            print("Thank you for using the Payroll Management System!")
            break

        # Invalid option
        else:
            print("Invalid option, please try again.")


if __name__ == '__main__':
    main_menu()
