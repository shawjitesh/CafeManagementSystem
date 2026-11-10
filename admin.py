from database import create_connection
from computer_details import show_computers

def add_computer():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        name = input("Enter Computer Name: ")
        rate = float(input("Enter Hourly Rate: "))

        if not name.strip() or rate <= 0:
            print("Invalid computer name or hourly rate.")
            return

        query = """
            INSERT INTO computers
            (computer_name, status, hourly_rate)
            VALUES (%s, 'Available', %s)
        """

        cur.execute(query, (name, rate))
        con.commit()

        print("Computer added successfully!")

    except ValueError:
        print("Please enter a valid hourly rate.")

    except Exception as err:
        print("Error:", err)

    finally:
        con.close()


def update_computer():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        computer_id = int(input("Enter Computer ID: "))
        name = input("Enter New Computer Name: ")
        rate = float(input("Enter New Hourly Rate: "))

        if not name.strip() or rate <= 0:
            print("Invalid details.")
            return

        query = """
            UPDATE computers
            SET computer_name = %s, hourly_rate = %s
            WHERE computer_id = %s
        """

        cur.execute(query, (name, rate, computer_id))
        con.commit()

        if cur.rowcount > 0:
            print("Computer details updated successfully!")
        else:
            print("Computer ID not found.")

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as err:
        print("Error:", err)

    finally:
        con.close()


def delete_computer():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        computer_id = int(input("Enter Computer ID to delete: "))

        query = """
            DELETE FROM computers
            WHERE computer_id = %s AND status = 'Available'
        """

        cur.execute(query, (computer_id,))
        con.commit()

        if cur.rowcount > 0:
            print("Computer deleted successfully!")
        else:
            print("Computer not found or currently in use.")

    except ValueError:
        print("Enter a valid Computer ID.")

    except Exception as err:
        con.rollback()
        print("Unable to delete computer:", err)

    finally:
        con.close()


def view_all_sessions():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        query = """
            SELECT s.session_id, s.customer_name,
                   s.phone, c.computer_name,
                   s.start_time, s.end_time,
                   s.duration_minutes, s.total_amount,
                   s.status
            FROM sessions s
            JOIN computers c
            ON s.computer_id = c.computer_id
            ORDER BY s.session_id DESC
        """

        cur.execute(query)
        records = cur.fetchall()

        print("\n========== CUSTOMER SESSION REPORT ==========")

        for row in records:
            print("\nSession ID:", row[0])
            print("Customer:", row[1])
            print("Phone:", row[2])
            print("Computer:", row[3])
            print("Start Time:", row[4])
            print("End Time:", row[5])
            print("Duration:", row[6], "minutes")
            print("Amount: Rs.", row[7])
            print("Status:", row[8])

        if not records:
            print("No session records found.")

    except Exception as err:
        print("Error:", err)

    finally:
        con.close()


def revenue_report():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        query = """
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
            FROM sessions
            WHERE status = 'Completed'
        """

        cur.execute(query)
        result = cur.fetchone()

        print("\n========== REVENUE REPORT ==========")
        print("Total Completed Sessions:", result[0])
        print("Total Revenue: Rs.", result[1])
        print("====================================")

    except Exception as err:
        print("Error:", err)

    finally:
        con.close()


def admin_menu():

    admin_password = "admin@123"

    password = input("Enter Admin Password: ")

    if password != admin_password:
        print("Incorrect password!")
        return

    while True:

        print("\n========== ADMIN MENU ==========")
        print("1. Add Computer")
        print("2. Update Computer")
        print("3. Delete Computer")
        print("4. View All Computers")
        print("5. View Customer Sessions")
        print("6. Revenue Report")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_computer()

        elif choice == "2":
            update_computer()

        elif choice == "3":
            delete_computer()

        elif choice == "4":
            show_computers()

        elif choice == "5":
            view_all_sessions()

        elif choice == "6":
            revenue_report()

        elif choice == "7":
            break

        else:
            print("Invalid choice! Please try again.")
