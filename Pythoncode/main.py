
import functions

def display_welcome():
    print("Welcome to the Bank Loan Management System!")
    print("==========================================")

def display_menu():
    print("\nMenu:")
    print("1. Add a client")
    print("2. Display all clients")
    print("3. Add a loan")
    print("4. Display all loans")
    print("5. Take money (apply payments)")
    print("6. Show bank summary")
    print("7. Exit")

def input_client_data():
    name = input("Enter client name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone: ").strip()
    return name, email, phone

def input_loan_data():
    client_id = int(input("Enter client ID: "))
    amount = float(input("Enter loan amount: "))
    rate = float(input("Enter interest rate (%): "))
    term = int(input("Enter term (months): "))
    return client_id, amount, rate, term

def main():
    treasury_balance = 0.0
    clients, loans = functions.load_mock_data_from_functions()

    display_welcome()

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            name, email, phone = input_client_data()
            errors = functions.validate_client_data(name, email, phone)
            if errors:
                print("Errors:", "; ".join(errors))
            else:
                functions.create_client(clients, name, email, phone)
                print("Client added successfully.")

        elif choice == "2":
            for c in clients:
                print(f"{c['id']}: {c['name']} ({c['email']}, {c['phone']})")

        elif choice == "3":
            client_id, amount, rate, term = input_loan_data()
            errors = functions.validate_loan_data(client_id, amount, rate, term, clients)
            if errors:
                print("Errors:", "; ".join(errors))
            else:
                functions.create_loan(loans, client_id, amount, rate, term)
                print("Loan added successfully.")

        elif choice == "4":
            loans_with_names = functions.build_loan_list_with_names(loans, clients)
            for l in loans_with_names:
                print(f"Loan #{l['id']} for {l['client_name']} - ${l['amount']} at {l['interest_rate']}% for {l['term_months']} months")

        elif choice == "5":
            taken = functions.apply_payments(loans)
            treasury_balance += taken
            print(f"Collected ${taken:.2f}. Treasury now: ${treasury_balance:.2f}")

        elif choice == "6":
            bank_data = functions.get_bank_data(loans, clients)
            print(f"\nTreasury: ${treasury_balance:.2f}")
            print(f"Total loan balance: ${bank_data['total_loan_balance']:.2f}")
            print(f"Due this round: ${bank_data['total_due']:.2f}")
            for p in bank_data['payments']:
                print(f"{p['client_name']} owes ${p['payment']:.2f}")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
