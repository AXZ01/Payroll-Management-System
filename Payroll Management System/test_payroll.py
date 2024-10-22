import pytest
from dao.payroll_service import PayrollService


@pytest.fixture
def payroll_service():

    config_file = "config\db_config.properties"
    return PayrollService(config_file)


def test_calculate_gross_salary_for_employee(payroll_service):
    employee_id = '1'
    basic_salary = 5000
    allowances = 2000
    gross_salary = payroll_service.calculate_gross_salary(
        employee_id, basic_salary, allowances)
    assert gross_salary == 7000, f"Expected 7000, but got {gross_salary}"


def test_calculate_net_salary_after_deductions(payroll_service):
    employee_id = '1'
    gross_salary = 7000
    deductions = 1500
    net_salary = payroll_service.calculate_net_salary(
        employee_id, gross_salary, deductions)
    assert net_salary == 5500, f"Expected 5500, but got {net_salary}"


def test_verify_tax_calculation_for_high_income_employee(payroll_service):
    employee_id = '1'
    gross_salary = 100000
    expected_tax = payroll_service.calculate_tax(employee_id, gross_salary)
    assert expected_tax == 25000, f"Expected 25000, but got {expected_tax}"


def test_process_payroll_for_multiple_employees(payroll_service):
    employee_ids = ['1', '2', '3']  # Assume IDs 1, 2, 3 are valid
    payroll_results = payroll_service.process_payroll(employee_ids)
    assert '1' in payroll_results
    assert payroll_results['1']['gross_salary'] == 7000
    assert payroll_results['1']['net_salary'] == 5500


def test_verify_error_handling_for_invalid_employee_data(payroll_service):
    invalid_employee_id = '999'
    with pytest.raises(Exception) as exc_info:
        payroll_service.get_employee_by_id(invalid_employee_id)
    assert "Employee not found" in str(exc_info.value)
