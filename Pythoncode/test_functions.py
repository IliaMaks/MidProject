import pytest
from functions import validate_client_data, generate_schedule

def test_validate_client_data():
    # Valid data
    errors = validate_client_data("John", "john@example.com", "0521234567")
    assert errors == []

    # Invalid name
    errors = validate_client_data("", "john@example.com", "0521234567")
    assert "Name cannot be empty." in errors

    # Invalid email
    errors = validate_client_data("John", "johnexample.com", "0521234567")
    assert "Invalid email format." in errors

    # Invalid phone
    errors = validate_client_data("John", "john@example.com", "abc123")
    assert "Phone number must be digits only (9–15 digits)." in errors

def test_generate_schedule():
    amount = 1200
    rate = 12  # 12% annual
    months = 12
    schedule = generate_schedule(amount, rate, months)
    
    # Check that the schedule has the correct number of months
    assert len(schedule) == months
    
    # Check that the first month's payment is positive
    assert schedule[0]['payment'] > 0
    
    # Check that the last month's balance is close to zero
    assert schedule[-1]['balance'] < 1
