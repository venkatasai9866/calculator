import sqlite3
import hashlib

def create_database():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password!")
        return False

create_database()
def create_transaction_table():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def add_transaction(user_id, type, category, amount, date):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO transactions (user_id, type, category, amount, date)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, type, category, amount, date))
    conn.commit()
    conn.close()
    print("Transaction added successfully!")

create_transaction_table()
def generate_report(user_id, period="monthly"):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    if period == "monthly":
        cursor.execute("""
        SELECT category, type, SUM(amount) FROM transactions
        WHERE user_id = ? AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        GROUP BY category, type
        """, (user_id,))
    else:
        cursor.execute("""
        SELECT category, type, SUM(amount) FROM transactions
        WHERE user_id = ? AND strftime('%Y', date) = strftime('%Y', 'now')
        GROUP BY category, type
        """, (user_id,))
    report = cursor.fetchall()
    conn.close()
    for row in report:
        print(f"Category: {row[0]}, Type: {row[1]}, Total: {row[2]}")
def create_budget_table():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        budget REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def set_budget(user_id, category, budget):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO budgets (user_id, category, budget)
    VALUES (?, ?, ?)
    """, (user_id, category, budget))
    conn.commit()
    conn.close()
    print("Budget set successfully!")

create_budget_table()
