# dao/financial_record_service.py
from utils.DBConnUtil import DBConnUtil
from exceptions.custom_exceptions import FinancialRecordNotFoundException


class FinancialRecordService:
    def __init__(self, config_file):
        self.conn = DBConnUtil.get_connection(config_file)
        if self.conn:
            print("Database connection successful!")
        else:
            raise Exception(
                "Database connection failed!")

    def add_financial_record(self, financial_record):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO FinancialRecord (EmployeeID, RecordDate, Description, Amount, RecordType)
            VALUES (?, ?, ?, ?, ?)
        """, financial_record.EmployeeID, financial_record.RecordDate, financial_record.Description,
             financial_record.Amount, financial_record.RecordType)
        self.conn.commit()

    def get_financial_record_by_id(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM FinancialRecord WHERE RecordID = ?", (record_id,))
        record = cursor.fetchone()

        if not record:
            raise FinancialRecordNotFoundException(
                f"Financial record with ID {record_id} not found.")

        return record

    def get_financial_records_for_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM FinancialRecord WHERE EmployeeID = ?", (employee_id,))
        records = cursor.fetchall()

        if not records:
            raise FinancialRecordNotFoundException(
                f"No financial records found for Employee ID {employee_id}.")

        return records
    def get_financial_records_for_date(self, record_date):
        cursor = self.conn.cursor()

        # Format the date to 'YYYY-MM-DD' to match the SQL date format
        formatted_date = record_date.strftime("%Y-%m-%d")

        cursor.execute("SELECT * FROM FinancialRecord WHERE RecordDate = ?", (formatted_date,))
        rows = cursor.fetchall()

        if not rows:
            print(f"No financial records found for the date {formatted_date}.")
            return []  # Return an empty list instead of raising an exception
        
        return rows
