from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt



def create_account(name):
    df = pd.DataFrame(columns=["Date", "Description", "Amount"])
    df.to_csv(f"accounts/{name}.csv", index=False)
    print(f"Account created: {name}")

def delete_account(name):
    try:
        os.remove(f"accounts/{name}.csv")
        print(f"Account deleted: {name}")
    except FileNotFoundError:
        print(f"Account '{name}' does not exist.")

def read_account(acc):
    df = pd.read_csv(f"accounts/{acc}.csv")
    return df

def add_transaction(df, acc):
    date = input("Enter Date (YYYY-MM-DD) or leave empty for current date: ")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    description = input("Enter Description: ")
    amount = float(input("Enter Amount: "))
    new_row = pd.DataFrame({"Date": [date], "Description": [description], "Amount": [amount]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(f"accounts/{acc}.csv", index=False)
    print("Transaction added")
    # return df

def remove_transaction(df, acc):
    date = input("Enter Date (YYYY-MM-DD) or leave empty for current date: ")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    description = input("Enter Description: ")
    df = df[~((df["Date"] == date) & (df["Description"] == description))]
    df.to_csv(f"accounts/{acc}.csv", index=False)

def view_transactions(df):
    pass

def edit_transaction(df):
    pass

def main():
    accounts_list = []

    def load_accounts():
        if not os.path.exists("accounts"):
            os.makedirs("accounts")
        for file in os.listdir("accounts"):
            if file.endswith(".csv"):
                accounts_list.append(file[:-4])
    load_accounts()

    print("ACCOUNT MENU")

    for i in accounts_list:
        print(i)

    print(""" 
    1. Create Account
    2. Delete Account
    Enter Account name to choose account or Q to quit
    \n""")
    inp = input("Enter your choice (1-2): ").lower()

    if inp == "1":
        name = input("Enter Account Name: ").lower()
        create_account(name)
    elif inp == "2":
        name = input("Enter Account Name: ").lower()
        inp = input("Are you sure you want to delete this account? (y/n): ").lower()
        if inp == "y":
            delete_account(name)
        else:
            print("Account deletion canceled.")
    elif inp in accounts_list:
        account_func(inp)
    elif inp == "q":
        print("Quitting...")
        exit()
    else:
        print("Invalid choice")

    print(accounts_list)

def account_func(acc):
    df = read_account(acc)
    print(f"{acc.upper()} ACCOUNT FUNCTION MENU")
    print("""
    1. Add Transaction
    2. Remove Transaction
    3. View Transactions
    4. Edit Transaction
    5. Back to Account Menu
    \n""")
    inp = input("Enter your choice (1-5): ").lower()

    if inp == "1":
        add_transaction(df, acc)
    elif inp == "2":
        remove_transaction(df, acc)
    elif inp == "3":
        view_transactions(df)
    elif inp == "4":
        edit_transaction(df)
    elif inp == "5":
        main()
    else:
        print("Invalid choice")

while True:
    main()
    