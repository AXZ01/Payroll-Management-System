class EmployeeNotFoundException(Exception):
    def __init__(self, message="Employee not found"):
        self.message = message
        super().__init__(self.message)

class DatabaseConnectionException(Exception):
    def __init__(self, message="Database connection error"):
        self.message = message
        super().__init__(self.message)
class FinancialRecordNotFoundException(Exception):
    def __init__(self, message="Financial record not found"):
        self.message = message
        super().__init__(self.message)
class TaxNotFoundException(Exception):
    def __init__(self, message="Tax record not found"):
        self.message = message
        super().__init__(self.message)
class PayrollNotFoundException(Exception):
    def __init__(self, message="Payroll record not found"):
        self.message = message
        super().__init__(self.message)

