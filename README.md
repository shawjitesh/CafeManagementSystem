# Cyber Cafe Management System

A menu-driven command-line application, written in Python and backed by MySQL, for running a cyber cafe. Administrators manage computers and view reports. Customers start and stop timed computer sessions, get billed, check their history and leave feedback.

---

## Project Structure

```text
CyberCafeManagementSystem/
├── main.py              # Entry point and main menu
├── database.py          # MySQL connection helper
├── admin.py             # Admin login, computer management and reports
├── customer.py          # Customer menu, starting sessions, history, feedback
├── billing.py           # Active sessions, stopping sessions, bill calculation
└── computer_details.py  # Table of all computers
```

---

## File Descriptions

### `main.py`

The entry point of the application. `main_menu()` shows the top-level menu in a loop:

1. **Administrator Login**: calls `admin_menu()` from `admin.py`
2. **Customer Menu**: calls `customer_menu()` from `customer.py`
3. **Exit**: closes the program

Run this file to start the system.

### `database.py`

Has a single helper, `create_connection()`, which opens a connection to the `cybercafe_management` MySQL database using `mysql.connector`. It returns the connection object, or prints an error and returns `None` if the connection fails. Every other module calls this function before it runs a query.

### `admin.py`

Holds all administrator features. `admin_menu()` asks for the admin password (hard-coded in this file) before it shows the menu.

| Function | Purpose |
| --- | --- |
| `add_computer()` | Adds a new computer with a name and hourly rate. It starts with the status `Available`. |
| `update_computer()` | Changes the name and hourly rate of an existing computer, looked up by ID. |
| `delete_computer()` | Deletes a computer by ID, but only if its status is `Available` (not in use). |
| `view_all_sessions()` | Shows every customer session (customer, phone, computer, times, duration, amount, status), newest first. |
| `revenue_report()` | Shows the number of completed sessions and the total revenue from them. |
| `admin_menu()` | Password-protected menu that links to all the functions above, plus *View All Computers* from `computer_details.py`. |

Input checks reject empty names, rates of zero or less, and values that are not numbers.

### `customer.py`

Holds the customer-facing features.

| Function | Purpose |
| --- | --- |
| `view_available_computers()` | Lists the computers whose status is `Available`, with their hourly rates. |
| `start_session()` | Asks for the customer's name and phone number, shows the available computers and lets the customer pick one. It locks the chosen row with `SELECT ... FOR UPDATE` so two customers can't book the same machine. It then creates an `Active` session and marks the computer `In Use`, all in one transaction. |
| `customer_history()` | Shows all past and current sessions for a phone number. |
| `give_feedback()` | Saves the customer's name, phone number and comments in the `feedback` table. |
| `customer_menu()` | Menu that links to the functions above and to the billing functions (*Stop Session*, *View Active Sessions*). |

### `billing.py`

Handles active sessions and billing.

| Function | Purpose |
| --- | --- |
| `view_active_sessions()` | Lists all sessions whose status is `Active`, with the customer, the computer and the start time. |
| `stop_session()` | Ends an active session and prints the customer's bill. |

**Billing rules in `stop_session()`:**

- Duration = current time − start time, rounded **up** to the next whole minute (at least 1 minute).
- Billed hours = duration rounded **up** to the next whole hour.
- Total amount = billed hours × the computer's hourly rate.
- The session is marked `Completed` and the computer goes back to `Available`. Both changes are saved in one transaction, and the transaction is rolled back if an error occurs.

### `computer_details.py`

Has `show_computers()`, which prints a formatted table of every computer (ID, name, status, hourly rate) sorted by ID. The admin menu uses it, and it can also be run on its own:

```bash
python computer_details.py
```

---

## Database Schema

The code expects a MySQL database named `cybercafe_management` with the tables below. This schema is inferred from the queries in the code, so adjust the column types as needed.

```sql
CREATE DATABASE IF NOT EXISTS cybercafe_management;
USE cybercafe_management;

CREATE TABLE computers (
    computer_id   INT AUTO_INCREMENT PRIMARY KEY,
    computer_name VARCHAR(100) NOT NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'Available',  -- 'Available' / 'In Use'
    hourly_rate   DECIMAL(10,2) NOT NULL
);

CREATE TABLE sessions (
    session_id       INT AUTO_INCREMENT PRIMARY KEY,
    customer_name    VARCHAR(100) NOT NULL,
    phone            VARCHAR(20)  NOT NULL,
    computer_id      INT NOT NULL,
    start_time       DATETIME NOT NULL,
    end_time         DATETIME NULL,
    duration_minutes INT NULL,
    total_amount     DECIMAL(10,2) NULL,
    status           VARCHAR(20) NOT NULL,                   -- 'Active' / 'Completed'
    FOREIGN KEY (computer_id) REFERENCES computers(computer_id)
);

CREATE TABLE feedback (
    feedback_id   INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone         VARCHAR(20)  NOT NULL,
    comments      TEXT NOT NULL
);
```

> Note: with this foreign key in place, MySQL won't let you delete a computer that has any session history. `delete_computer()` catches the resulting error and reports it.

---

## Setup and Running

1. **Install the dependency:**

   ```bash
   pip install mysql-connector-python
   ```

2. **Create the database** using the schema above.
3. **Set your MySQL credentials** (host, user, password) in `database.py`.
4. **Run the application:**

   ```bash
   python main.py
   ```

---

## Typical Workflow

1. The admin logs in and adds computers with their hourly rates.
2. A customer views the available computers and starts a session on one of them.
3. When the customer finishes, they stop the session and the bill is shown.
4. The admin checks all sessions and the revenue report.

---

## Security Notes

- The database password and the admin password are hard-coded in `database.py` and `admin.py`. For anything beyond local or learning use, move them into environment variables or a config file kept out of version control.
- All SQL queries use parameterized placeholders (`%s`), which protects against SQL injection.
