class Payroll:
    def __init__(self, PayrollID, EmployeeID, PayPeriodStartDate, PayPeriodEndDate, BasicSalary, OvertimePay, Deductions, NetSalary):
        self.PayrollID = PayrollID
        self.EmployeeID = EmployeeID
        self.PayPeriodStartDate = PayPeriodStartDate
        self.PayPeriodEndDate = PayPeriodEndDate
        self.BasicSalary = BasicSalary
        self.OvertimePay = OvertimePay
        self.Deductions = Deductions
        self.NetSalary = NetSalary
