import sqlite3

def create_database():
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()

    # Create the users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
    
    # Create the buy table
    c.execute('''CREATE TABLE IF NOT EXISTS buy (
                    Email TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    coin_amount INTEGER,
                    total_price FLOAT
                )''')

    # Create the sell table
    c.execute('''CREATE TABLE IF NOT EXISTS sell (
                    Email TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    coin_amount INTEGER,
                    total_price FLOAT
                )''')

    conn.commit()
    conn.close()
