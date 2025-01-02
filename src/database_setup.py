import sqlite3
import os

def setup_database(db_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL queries for table creation
    create_books_table = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT NOT NULL UNIQUE,
        isbn TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        publisher TEXT,
        publication_year INTEGER,
        category TEXT,
        total_copies INTEGER DEFAULT 1,
        available_copies INTEGER DEFAULT 1,
        language TEXT,
        description TEXT,
        location TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active'
    );
    """
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        national_id VARCHAR(11) NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        address TEXT,
        membership_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        membership_expiry TIMESTAMP,
        membership_type TEXT NOT NULL,
        penalty_points INTEGER DEFAULT 0,
        total_borrowed INTEGER DEFAULT 0,
        account_status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    create_loans_table = """
    CREATE TABLE IF NOT EXISTS loans (
        loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        book_id INTEGER NOT NULL,
        loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        due_date TIMESTAMP,
        return_date TIMESTAMP,
        status TEXT DEFAULT 'borrowed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    );
    """
    
    # Execute table creation queries
    try:
        cursor.execute(create_books_table)
        print("Books table created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating books table: {e}")

    try:
        cursor.execute(create_users_table)
        print("Users table created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating users table: {e}")

    try:
        cursor.execute(create_loans_table)
        print("Loans table created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating loans table: {e}")

    # Commit changes and close the connection
    conn.commit()
    conn.close()
