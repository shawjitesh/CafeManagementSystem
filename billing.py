from database import create_connection
from datetime import datetime
import math

def view_active_sessions():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        query = """
            SELECT s.session_id, s.customer_name,
                   c.computer_name, s.start_time
            FROM sessions s
            JOIN computers c
            ON s.computer_id = c.computer_id
            WHERE s.status = 'Active'
        """

        cur.execute(query)
        records = cur.fetchall()

        print("\n========== ACTIVE SESSIONS ==========")

        if records:
            for row in records:
                print(
                    "Session ID:", row[0],
                    "| Customer:", row[1],
                    "| Computer:", row[2],
                    "| Started:", row[3]
                )
        else:
            print("No active sessions.")

    except Exception as err:
        print("Error:", err)

    finally:
        con.close()


def stop_session():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        session_id = int(input("Enter Session ID to stop: "))

        # Fetch active session details
        query = """
            SELECT s.computer_id, s.start_time,
                   c.hourly_rate
            FROM sessions s
            JOIN computers c
            ON s.computer_id = c.computer_id
            WHERE s.session_id = %s
            AND s.status = 'Active'
        """

        cur.execute(query, (session_id,))
        record = cur.fetchone()

        if record is None:
            print("Active session not found.")
            return

        computer_id = record[0]
        start_time = record[1]
        hourly_rate = record[2]

        end_time = datetime.now()

        # Calculate session duration
        seconds = (end_time - start_time).total_seconds()

        duration_minutes = max(1, math.ceil(seconds / 60))

        # Round billing time to the next full hour
        billed_hours = math.ceil(duration_minutes / 60)

        total_amount = billed_hours * hourly_rate

        # Update session details
        update_query = """
            UPDATE sessions
            SET end_time = %s,
                duration_minutes = %s,
                total_amount = %s,
                status = 'Completed'
            WHERE session_id = %s
        """

        cur.execute(
            update_query,
            (end_time, duration_minutes, total_amount, session_id)
        )

        # Make computer available again
        update_computer_query = """
            UPDATE computers
            SET status = 'Available'
            WHERE computer_id = %s
        """

        cur.execute(update_computer_query, (computer_id,))

        con.commit()

        print("\n========== CUSTOMER BILL ==========")
        print("Session ID:", session_id)
        print("Start Time:", start_time)
        print("End Time:", end_time)
        print("Duration:", duration_minutes, "minutes")
        print("Billed Hours:", billed_hours)
        print("Hourly Rate: Rs.", hourly_rate)
        print("Total Amount: Rs.", total_amount)
        print("===================================")

        print("Session completed successfully!")

    except ValueError:
        print("Please enter a valid Session ID.")

    except Exception as err:
        con.rollback()
        print("Billing error:", err)

    finally:
        con.close()
