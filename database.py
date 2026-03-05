import sqlite3

DB_NAME = "she_shield.db"

# ---------------- CONNECTION ---------------- #

def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------------- CREATE TABLES ---------------- #

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dob TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        mobile TEXT,
        role TEXT DEFAULT 'User'
    )
    """)

    # CONTACTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        name TEXT NOT NULL,
        number TEXT NOT NULL
    )
    """)

    # COMPLAINTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        category TEXT NOT NULL,
        subject TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    conn.commit()
    conn.close()


# ---------------- USER FUNCTIONS ---------------- #

def add_user(name, dob, email, password, mobile):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users (name, dob, email, password, mobile)
        VALUES (?, ?, ?, ?, ?)
        """, (name, dob, email, password, mobile))

        conn.commit()
        conn.close()
        return True

    except sqlite3.IntegrityError:
        return False


def validate_login(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()
    return user


def get_user(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()
    return user


def update_profile(email, name, mobile):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET name=?, mobile=?
    WHERE email=?
    """, (name, mobile, email))

    conn.commit()
    conn.close()


# ---------------- CONTACT FUNCTIONS ---------------- #

def add_contact(email, name, number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO contacts (email, name, number)
    VALUES (?, ?, ?)
    """, (email, name, number))

    conn.commit()
    conn.close()


def get_contacts(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, number FROM contacts WHERE email=?",
        (email,)
    )

    contacts = cursor.fetchall()
    conn.close()
    return contacts


# ---------------- COMPLAINT FUNCTIONS ---------------- #

def add_complaint(email, category, subject, description, location):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO complaints (email, category, subject, description, location)
    VALUES (?, ?, ?, ?, ?)
    """, (email, category, subject, description, location))

    conn.commit()
    conn.close()


def get_user_complaints(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, category, subject, status
    FROM complaints
    WHERE email=?
    ORDER BY id DESC
    """, (email,))

    data = cursor.fetchall()
    conn.close()
    return data


def get_complaint_counts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, COUNT(*)
    FROM complaints
    GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()
    return data