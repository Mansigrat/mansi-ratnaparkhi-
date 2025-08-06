import csv
import os
from datetime import datetime

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_data.csv")

# Utility functions
def clean_csv_dates():
    """Standardize date format in CSV to dd-mm-yyyy."""
    if not os.path.exists(FILE_PATH):
        return

    cleaned_rows = []
    with open(FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        if not fieldnames or "date" not in fieldnames:
            return

        for row in reader:
            original_date = row["date"].strip()
            date_formats = ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"]
            converted_date = None
            for fmt in date_formats:
                try:
                    converted_date = datetime.strptime(original_date, fmt)
                    break
                except ValueError:
                    continue

            if converted_date:
                row["date"] = converted_date.strftime("%d-%m-%Y")
                cleaned_rows.append(row)

    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

#Input functions
def get_amount():
    while True:
        try:
            return float(input("Enter the amount: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_category():
    while True:
        category = input("Enter the category ('I' for Income, 'E' for Expense): ").strip().upper()
        if category == 'I':
            return "Income"
        elif category == 'E':
            return "Expense"
        else:
            print("Invalid choice. Enter 'I' or 'E'.")

def get_date(prompt="Enter the date (dd-mm-yyyy): ", allow_default=False):
    while True:
        date_str = input(prompt).strip()
        if allow_default and date_str == "":
            return datetime.today()
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            print("Invalid format. Please enter date as dd-mm-yyyy.")

def get_description():
    return input("Enter a description (optional): ").strip()

#Core functions
def add_transaction():
    amount = get_amount()
    category = get_category()
    date = get_date(allow_default=True).strftime("%d-%m-%Y")
    description = get_description()

    header = ["date", "category", "amount", "description"]

    with open(FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({
            "date": date,
            "category": category,
            "amount": amount,
            "description": description
        })

    print(f"\n Transaction saved to {FILE_PATH}\n")

def view_transactions_in_range():
    start_str = input("Enter the start date (dd-mm-yyyy): ").strip()
    end_str = input("Enter the end date (dd-mm-yyyy): ").strip()

    try:
        start_date = datetime.strptime(start_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_str, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format.")
        return

    found = False
    with open(FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row_date = datetime.strptime(row["date"], "%d-%m-%Y")
            except ValueError:
                continue
            if start_date <= row_date <= end_date:
                print(f"{row['date']} | {row['category']} | {row['amount']} | {row['description']}")
                found = True

    if not found:
        print("No transactions found in the given date range.")

def view_all_transactions():
    if not os.path.exists(FILE_PATH):
        print(" No transactions found.")
        return

    with open(FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        if not rows:
            print(" No transactions found.")
            return

        print("\n All Transactions:")
        for row in rows:
            print(f"{row['date']} | {row['category']} | {row['amount']} | {row['description']}")

def delete_transaction():
    search_term = input("Enter date or description keyword to search for deletion: ").strip().lower()
    matches = []

    with open(FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        all_rows = list(reader)

        for idx, row in enumerate(all_rows, start=1):
            if search_term in row["date"].lower() or search_term in row["description"].lower():
                matches.append((idx, row))

    if not matches:
        print("No matching transactions found.")
        return

    print("\n Matching Transactions:")
    for i, (idx, row) in enumerate(matches, start=1):
        print(f"{i}. {row['date']} | {row['category']} | {row['amount']} | {row['description']}")

    choice = input("\nEnter numbers to delete (comma-separated) or 'all' to delete all matches: ").strip().lower()

    if choice == "all":
        to_delete_indices = {idx for idx, _ in matches}
    else:
        try:
            nums = [int(x.strip()) for x in choice.split(",")]
            to_delete_indices = {matches[n-1][0] for n in nums if 1 <= n <= len(matches)}
        except ValueError:
            print("Invalid input.")
            return

    updated_rows = [row for idx, row in enumerate(all_rows, start=1) if idx not in to_delete_indices]

    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print("Selected transaction(s) deleted successfully.")

#Main menu
def main():
    clean_csv_dates()  # Auto-fix date formats at start

    while True:
        print("\n Finance Tracker Menu")
        print("1. Add a new transaction")
        print("2. View transactions in date range")
        print("3. View all transactions")
        print("4. Delete transaction")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions_in_range()
        elif choice == "3":
            view_all_transactions()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
