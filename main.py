import os
import sqlite3
import pandas as pd
from datetime import datetime

db_name = 'finance.db'


def accounts_check():
    with conn:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        num_tables = len(tables)
        if num_tables == 0:
            print("No accounts found....")
            create_account()
        else:
            account_menu()

def get_account():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [t[0] for t in tables]
    return table_names

def create_account():
    print("-----CREATE AN ACCOUNT-----")
    table_name = input("Enter an account name: ").strip()
    with conn:
        if table_name in get_account():
            print(f"Account with the name {table_name} already exists, Choose a different name.....")
            create_account()
        else:
            bal = float(input("Enter the initial balance (enter 0 if none): ").strip())
            cursor.execute(f'''
                CREATE TABLE {table_name} (
                    Date TEXT,
                    Description TEXT,
                    Amount REAL   
                )''')
            if bal != 0:
                cursor.execute(f"INSERT INTO {table_name} (Date, Description, Amount) VALUES (?, ?, ?)", ("0001-01-01", "Initial Balance", bal))
            print(f"Account '{table_name}' created...")
            account_menu()

def account_menu():
    accounts = get_account()
    print("-----YOUR ACCOUNTS-----")

    for i, name in enumerate(accounts, start=1):
        print(f"{i}. {name}")
    
    print('-----------------------------')

    response = input("Select an account by its 'number' \ntype 'new' to create a new account \ntype 'del' to delete an account \ntype 'q' to exit: ").strip().lower()
    if response == 'new':
        create_account()
    elif response == 'del':
        with conn:
            try:
                cursor.execute("DROP TABLE IF EXISTS " + accounts[int(input("Enter the account number to delete: ")) - 1])
                print("Account deleted...")
            except Exception as e:
                print(f"Account does not exist, Enter a valid number....")
        account_menu()
    elif response == 'q':
        print("Exiting...")
        exit()
    elif response.isdigit() and 1 <= int(response) <= len(accounts):
        selected_account = accounts[int(response) - 1]
        function_menu(selected_account)
    else:
        print("Invalid input, please try again...")
        account_menu()

def function_menu(selected_account):
    print(f"-----ACCOUNT: {selected_account}-----")
    print("-----FUNCTION MENU-----")
    response = int(input("Select a function: \n1. Add Transaction \n2. View Transactions \n3. Delete Transaction \n4. Export as CSV \n5. Back to Account Menu: ").strip())
    if response == 1:
        date = input("Enter the date (YYYY-MM-DD): ").strip()
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        description = input("Enter the description: ").strip()
        amount = float(input("Enter the amount: ").strip())
        with conn:
            cursor.execute(f"INSERT INTO {selected_account} (Date, Description, Amount) VALUES (?, ?, ?)", (date, description, amount))
        function_menu(selected_account)
    elif response == 2:
        print('-----VIEW TRANSACTIONS-----')
        view_choice = input("1. View all transactions \n2. View transactions by year \n3. Back to Function Menu: ").strip()

        with conn:
            cursor.execute(f"SELECT * FROM {selected_account}")
            transactions = cursor.fetchall()
            df = pd.DataFrame(transactions, columns=['Date', 'Description', 'Amount'])
            df.sort_values(by='Date', inplace=True)
        
        if view_choice == '1':
            df_view = df.copy()
            df_view.loc['Total'] = ['--------', '--------', df['Amount'].sum()]
            print(df_view)
        elif view_choice == '2':
            year = input("Enter the year (YYYY): ").strip()
            df_year = df[df['Date'].str.startswith(year)]
            if df_year.empty:
                print(f"No transactions found for the year {year}.")
            else:
                df_year.loc['Total'] = ['--------', '--------', df_year['Amount'].sum()]
                print(df_year)
        elif view_choice == '3':
            function_menu(selected_account)
            return
        else:
            print("Invalid choice, returning to Function Menu...")

        function_menu(selected_account)
    elif response == 3:
        date = input("Enter the date of the transaction to delete (YYYY-MM-DD): ").strip()
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        description = input("Enter the description of the transaction to delete: ").strip()
        with conn:
            cursor.execute(
                f"SELECT rowid, Date, Description, Amount FROM {selected_account} WHERE Date = ? AND Description = ?",
                (date, description)
            )
            matches = cursor.fetchall()

            if not matches:
                print("No matching transaction found....")
            elif len(matches) == 1:
                cursor.execute(f"DELETE FROM {selected_account} WHERE rowid = ?", (matches[0][0],))
                print("Transaction deleted...")
            else:
                print(f"Found {len(matches)} matching transactions:")
                for i, m in enumerate(matches, start=1):
                    print(f"{i}. Date: {m[1]}, Description: {m[2]}, Amount: {m[3]}")
                choice = input("Enter the number of the transaction to delete: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(matches):
                    row_id = matches[int(choice) - 1][0]
                    cursor.execute(f"DELETE FROM {selected_account} WHERE rowid = ?", (row_id,))
                    print("Transaction deleted...")
                else:
                    print("Invalid choice, cancelling delete....")

        function_menu(selected_account)
    elif response == 4:
        with conn:
            cursor.execute(f"SELECT * FROM {selected_account}")
            transactions = cursor.fetchall()
            df = pd.DataFrame(transactions, columns=['Date', 'Description', 'Amount'])
            df.sort_values(by='Date', inplace=True)
            df.loc['Total'] = ['', '', df['Amount'].sum()]
            csv = f"{selected_account}_transactions.csv"
            df.to_csv(csv, index=False)
            print(f"Transactions exported to {csv}...")
        function_menu(selected_account)
    elif response == 5:
        account_menu()

if os.path.exists(db_name):
    print('Database exists, connecting...\n')

else:
    print('Creating Main Database...\n')

conn = sqlite3.connect(db_name)
cursor = conn.cursor()
accounts_check()