from database import create_connection

def show_computers():

    con = create_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        query = """
            SELECT computer_id, computer_name, status, hourly_rate
            FROM computers
            ORDER BY computer_id
        """

        cur.execute(query)
        records = cur.fetchall()

        print("\n========== COMPUTER DETAILS ==========\n")

        if records:
            print("{:<15} {:<20} {:<15} {:<15}".format(
                "Computer ID", "Computer Name",
                "Status", "Hourly Rate"
            ))

            print("-" * 65)

            for row in records:
                print("{:<15} {:<20} {:<15} Rs. {:<10.2f}".format(
                    row[0], row[1], row[2], row[3]
                ))
        else:
            print("No computer records found.")

        print("\n======================================")

    except Exception as err:
        print("Error displaying computers:", err)

    finally:
        cur.close()
        con.close()


if __name__ == "__main__":
    show_computers()
