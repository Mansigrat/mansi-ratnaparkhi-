import csv
from datetime import datetime

def get_amount():
    while True:
        try:
            amount = float(input("Enter the amount: "))
            return amount
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

def add_transaction():
    # Get inputs
    amount = get_amount()
    category = get_category()
    date = get_date(allow_default=True).strftime("%d-%m-%Y")
    description = get_description()

    file_name = "finance_data.csv"
    header = ["Date", "Category", "Amount", "Description"]

    with open(file_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow([date, category, amount, description])

    print(f"\n Transaction saved to {file_name}\n")
    view_transactions(file_name)

def view_transactions(file_name):
    try:
        with open(file_name, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                print(" | ".join(map(str, row)))
    except FileNotFoundError:
        print("No transactions found.")

if __name__ == "__main__":
    add_transaction()
