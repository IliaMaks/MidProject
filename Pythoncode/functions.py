def create_client(clients, name, email, phone):
    new_client = {
        "id": len(clients) + 1,
        "name": name,
        "email": email,
        "phone": phone
    }
    clients.append(new_client)
    return new_client

def validate_client_data(name, email, phone):
    errors = []
    if not name:
        errors.append("Name cannot be empty.")
    if len(email) < 5 or '@' not in email or '.' not in email:
        errors.append("Invalid email format.")
    if not phone.isdigit() or not (9 <= len(phone) <= 15):
        errors.append("Phone number must be digits only (9–15 digits).")
    return errors

def create_loan(loans, client_id, amount, interest_rate, term_months):
    new_loan = {
        "id": len(loans) + 1,
        "client_id": client_id,
        "amount": amount,
        "interest_rate": interest_rate,
        "term_months": term_months,
        "schedule": generate_schedule(amount, interest_rate, term_months)
    }
    loans.append(new_loan)
    return new_loan

def validate_loan_data(client_id, amount, interest_rate, term_months, clients):
    errors = []
    if not any(c['id'] == client_id for c in clients):
        errors.append("Client not found.")
    if amount <= 0:
        errors.append("Amount must be positive.")
    if interest_rate < 0:
        errors.append("Interest rate cannot be negative.")
    if term_months <= 0:
        errors.append("Term must be greater than 0.")
    return errors



def generate_schedule(amount, rate, months):
    annual_rate = rate / 100
    monthly_rate = annual_rate / 12
    try:
        monthly_payment = amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    except ZeroDivisionError:
        monthly_payment = 0

    balance = amount
    schedule = []
    for month in range(1, months + 1):
        interest = balance * monthly_rate
        principal_payment = monthly_payment - interest
        balance -= principal_payment
        schedule.append({
            'month': month,
            'payment': round(monthly_payment, 2),
            'principal': round(principal_payment, 2),
            'interest': round(interest, 2),
            'balance': round(max(balance, 0), 2),
            'status': 'pending'
        })
    return schedule


def get_client_loans(client_id, loans):
    return [loan for loan in loans if loan['client_id'] == client_id]



def get_client_name(client_id, clients):
    for c in clients:
        if c['id'] == client_id:
            return c['name']
    return 'Unknown'



def build_loan_list_with_names(loans, clients):
    loan_list = []
    for loan in loans:
        loan_copy = loan.copy()
        loan_copy['client_name'] = get_client_name(loan['client_id'], clients)
        loan_list.append(loan_copy)
    return loan_list


def apply_payments(loans):
    paid_clients = set()
    taken_amount = 0.0
    for loan in loans:
        client_id = loan['client_id']
        if client_id not in paid_clients:
            for row in loan['schedule']:
                if row['status'] == 'pending':
                    row['status'] = 'paid'
                    taken_amount += row['payment']
                    paid_clients.add(client_id)
                    break
    return taken_amount


def calculate_due_per_client(loans, clients):
    client_payments = []
    total = 0.0
    seen_clients = set()

    for client in clients:
        if client['id'] in seen_clients:
            continue
        client_loans = get_client_loans(client['id'], loans)
        for loan in client_loans:
            for row in loan['schedule']:
                if row['status'] == 'pending':
                    client_payments.append({
                        'client_name': client['name'],
                        'payment': row['payment']
                    })
                    total =total+ row['payment']
                    seen_clients.add(client['id'])
                    break
            if client['id'] in seen_clients:
                break

    return client_payments, total


def calculate_total_loan_balance(loans):
    total_balance = 0
    for loan in loans:
        for row in loan['schedule']:
            if row['status'] == 'pending':
                total_balance += row['balance']
    return total_balance


def get_bank_data(loans, clients):
    payments, total = calculate_due_per_client(loans, clients)
    total_loan_balance = calculate_total_loan_balance(loans)
    return {
        'payments': payments,
        'total_due': total,
        'total_loan_balance': total_loan_balance
    }


def load_mock_data_from_functions():
    clients = [
        {"id": 1, "name": "Basil", "email": "Basil@example.com", "phone": "0521234567"},
        {"id": 2, "name": "Eli", "email": "Eli@example.com", "phone": "0529876543"},
        {"id": 3, "name": "Avi", "email": "Avi@example.com", "phone": "0532223344"},
        {"id": 4, "name": "Alex", "email": "Eli@example.com", "phone": "0541112233"},
        {"id": 5, "name": "Desmond", "email": "Desmond@example.com", "phone": "0505566778"},
    ]
    raw_loans = [
        {"client_id": 1, "amount": 10000, "interest_rate": 5.0, "term_months": 12},
        {"client_id": 2, "amount": 8000, "interest_rate": 6.0, "term_months": 10},
        {"client_id": 3, "amount": 20000, "interest_rate": 3.5, "term_months": 36},
        {"client_id": 4, "amount": 12000, "interest_rate": 4.0, "term_months": 18},
        {"client_id": 5, "amount": 9000, "interest_rate": 5.5, "term_months": 20}
        
    ]
    loans = []
    for i, loan in enumerate(raw_loans):
        loan['id'] = i + 1
        loan['schedule'] = generate_schedule(loan['amount'], loan['interest_rate'], loan['term_months'])
        loans.append(loan)
    return clients, loans
