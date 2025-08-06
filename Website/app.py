from flask import Flask, render_template, request, redirect, url_for, flash, session
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Pythoncode')))
import functions

app = Flask(__name__)
app.secret_key = 'devkey'


def get_clients():
    return session.get('clients', [])


def get_loans():
    return session.get('loans', [])


def get_treasury():
    return session.get('treasury_balance', 0.0)


def save_state(clients, loans, treasury_balance):
    session['clients'] = clients
    session['loans'] = loans
    session['treasury_balance'] = treasury_balance


@app.before_request
def ensure_data():
    if 'clients' not in session or 'loans' not in session:
        clients, loans = functions.load_mock_data_from_functions()
        session['clients'] = clients
        session['loans'] = loans
        session['treasury_balance'] = 0.0


@app.route('/')
def home():
    return render_template('index.html'), 200


@app.route('/clients')
def view_clients():
    return render_template('clients.html', clients=get_clients())


@app.route('/clients/add', methods=['GET', 'POST'])
def add_client():
    clients = get_clients()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        errors = functions.validate_client_data(name, email, phone)
        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template('add_client.html', name=name, email=email, phone=phone)

        functions.create_client(clients, name, email, phone)
        session['clients'] = clients
        flash("Client added successfully!", "success")
        return redirect(url_for('view_clients'))

    return render_template('add_client.html', name='', email='', phone='')


@app.route('/clients/<int:id>')
def client_details(id):
    clients = get_clients()
    loans = get_loans()
    client = next((c for c in clients if c['id'] == id), None)
    if not client:
        flash("Client not found.", "danger")
        return redirect(url_for('view_clients'))

    client_loans = functions.get_client_loans(id, loans)
    return render_template('client_detail.html', client=client, loans=client_loans)


@app.route('/loans')
def view_loans():
    clients = get_clients()
    loans = get_loans()
    loan_list = functions.build_loan_list_with_names(loans, clients)
    return render_template('loans.html', loans=loan_list)


@app.route('/loans/add', methods=['GET', 'POST'])
def add_loan():
    clients = get_clients()
    loans = get_loans()
    if request.method == 'POST':
        try:
            client_id = int(request.form.get('client_id', ''))
            amount = float(request.form.get('amount', ''))
            interest_rate = float(request.form.get('interest_rate', ''))
            term_months = int(request.form.get('term_months', ''))
        except (ValueError, TypeError):
            flash("Invalid input: all fields must be numbers.", "danger")
            return render_template('add_loan.html', clients=clients, form=request.form)

        errors = functions.validate_loan_data(client_id, amount, interest_rate, term_months, clients)
        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template('add_loan.html', clients=clients, form=request.form)

        functions.create_loan(loans, client_id, amount, interest_rate, term_months)
        session['loans'] = loans
        flash("Loan added successfully!", "success")
        return redirect(url_for('view_loans'))

    return render_template('add_loan.html', clients=clients, form={})


@app.route('/loans/amortization/<int:loan_id>')
def loan_amortization(loan_id):
    loans = get_loans()
    clients = get_clients()
    loan = next((l for l in loans if l['id'] == loan_id), None)
    if not loan:
        flash("Loan not found.", "danger")
        return redirect(url_for('view_loans'))

    client_name = functions.get_client_name(loan['client_id'], clients)
    return render_template('amortization.html', loan=loan, client_name=client_name, schedule=loan['schedule'])


@app.route('/bank')
def bank():
    clients = get_clients()
    loans = get_loans()
    treasury_balance = get_treasury()
    data = functions.get_bank_data(loans, clients)
    return render_template('bank.html',
                           treasury_balance=round(treasury_balance, 2),
                           total_loan_balance=round(data['total_loan_balance'], 2),
                           total_due=round(data['total_due'], 2),
                           payments=data['payments'])


@app.route('/bank/take', methods=['POST'])
def take_money():
    clients = get_clients()
    loans = get_loans()
    treasury_balance = get_treasury()
    taken_amount = functions.apply_payments(loans)
    treasury_balance += taken_amount
    save_state(clients, loans, treasury_balance)
    flash(f"Taken {taken_amount:.2f} to treasury!", "success")
    return redirect(url_for('bank'))


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
