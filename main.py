from admin import admin_menu
from customer import customer_menu

def main_menu():

    while True:

        print("\n")
        print("==========================================")
        print("       CYBER CAFE MANAGEMENT SYSTEM")
        print("==========================================")

        print("1. Administrator Login")
        print("2. Customer Menu")
        print("3. Exit")

        print("==========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            admin_menu()

        elif choice == "2":
            customer_menu()

        elif choice == "3":
            print("\nThank you for using Cyber Cafe Management System!")
            break

        else:
            print("Invalid choice! Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main_menu()
