from datetime import date

class Employee:
    def __init__(self, EmployeeID, FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address, Position, JoiningDate, TerminationDate=None):
        self.EmployeeID = EmployeeID
        self.FirstName = FirstName
        self.LastName = LastName
        self.DateOfBirth = DateOfBirth
        self.Gender = Gender
        self.Email = Email
        self.PhoneNumber = PhoneNumber
        self.Address = Address
        self.Position = Position
        self.JoiningDate = JoiningDate
        self.TerminationDate = TerminationDate

    def calculate_age(self):
        today = date.today()
        age = today.year - self.DateOfBirth.year - ((today.month, today.day) < (self.DateOfBirth.month, self.DateOfBirth.day))
        return age
