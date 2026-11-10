from database import create_connection
from billing import view_active_sessions, stop_session
from datetime import datetime

def view_available_computers():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        query = """
            SELECT computer_id, computer_name, hourly_rate
            FROM computers
            WHERE status = 'Available'
        """

        cur.execute(query)
        records = cur.fetchall()

        print("\n========== AVAILABLE COMPUTERS ==========")

        if records:
            for row in records:
                print(
                    "ID:", row[0],
                    "| Computer:", row[1],
                    "| Hourly Rate: Rs.", row[2]
                )
        else:
            print("No computers are currently available.")

    except Exception as err:
        print("Error:", err)

    finally:
        con.close()


def start_session():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        customer_name = input("Enter Customer Name: ").strip()
        phone = input("Enter Phone Number: ").strip()

        if not customer_name or not phone:
            print("Customer name and phone are required.")
            return

        # Display available computers
        cur.execute("""
            SELECT computer_id, computer_name, hourly_rate
            FROM computers
            WHERE status = 'Available'
        """)

        records = cur.fetchall()

        if not records:
            print("No computers are available.")
            return

        print("\nAvailable Computers:")

        for row in records:
            print(
                "ID:", row[0],
                "| Name:", row[1],
                "| Rate: Rs.", row[2], "/hour"
            )

        computer_id = int(input("\nEnter Computer ID: "))

        # Lock and check selected computer
        cur.execute("""
            SELECT computer_name, status
            FROM computers
            WHERE computer_id = %s
            FOR UPDATE
        """, (computer_id,))

        computer = cur.fetchone()

        if computer is None or computer[1] != 'Available':
            print("Selected computer is not available.")
            con.rollback()
            return

        # Start new session
        cur.execute("""
            INSERT INTO sessions
            (customer_name, phone, computer_id,
             start_time, status)
            VALUES (%s, %s, %s, %s, 'Active')
        """, (
            customer_name,
            phone,
            computer_id,
            datetime.now()
        ))

        session_id = cur.lastrowid

        # Mark computer as occupied
        cur.execute("""
            UPDATE computers
            SET status = 'In Use'
            WHERE computer_id = %s
        """, (computer_id,))

        con.commit()

        print("\nComputer session started successfully!")
        print("Session ID:", session_id)
        print("Customer:", customer_name)
        print("Computer:", computer[0])

    except ValueError:
        print("Please enter a valid Computer ID.")

    except Exception as err:
        con.rollback()
        print("Error starting session:", err)

    finally:
        con.close()


def customer_history():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        phone = input("Enter your Phone Number: ").strip()

        query = """
            SELECT s.session_id, c.computer_name,
                   s.start_time, s.end_time,
                   s.duration_minutes, s.total_amount,
                   s.status
            FROM sessions s
            JOIN computers c
            ON s.computer_id = c.computer_id
            WHERE s.phone = %s
            ORDER BY s.session_id DESC
        """

        cur.execute(query, (phone,))
        records = cur.fetchall()

        print("\n========== CUSTOMER HISTORY ==========")

        if records:
            for row in records:
                print("\nSession ID:", row[0])
                print("Computer:", row[1])
                print("Start Time:", row[2])
                print("End Time:", row[3])
                print("Duration:", row[4], "minutes")
                print("Amount: Rs.", row[5])
                print("Status:", row[6])
        else:
            print("No previous sessions found.")

    except Exception as err:
        print("Error:", err)

    finally:
        con.close()


def give_feedback():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        name = input("Enter Customer Name: ").strip()
        phone = input("Enter Phone Number: ").strip()
        comments = input("Enter Your Feedback: ").strip()

        if not name or not phone or not comments:
            print("Please fill in all feedback details.")
            return

        query = """
            INSERT INTO feedback
            (customer_name, phone, comments)
            VALUES (%s, %s, %s)
        """

        cur.execute(query, (name, phone, comments))
        con.commit()

        print("Thank you! Your feedback has been submitted.")

    except Exception as err:
        print("Error submitting feedback:", err)

    finally:
        con.close()


def customer_menu():

    while True:

        print("\n========== CUSTOMER MENU ==========")
        print("1. View Available Computers")
        print("2. Start Computer Session")
        print("3. Stop Computer Session")
        print("4. View Active Sessions")
        print("5. View Session History")
        print("6. Submit Feedback")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_available_computers()

        elif choice == "2":
            start_session()

        elif choice == "3":
            view_active_sessions()
            stop_session()

        elif choice == "4":
            view_active_sessions()

        elif choice == "5":
            customer_history()

        elif choice == "6":
            give_feedback()

        elif choice == "7":
            break

        else:
            print("Invalid choice! Please try again.")
