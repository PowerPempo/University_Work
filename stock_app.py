
import sqlite3

DATABASE_NAME = 'stock_exchange.db'

def get_db_connection():
    """Створює з'єднання з БД та налаштовує доступ до колонок за іменем."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Доступ до колонок за іменем
    conn.execute("PRAGMA foreign_keys = ON;") # Увімкнення підтримки зовнішніх ключів
    return conn

def init_db():
    """Ініціалізує таблиці в БД згідно зі схемою, якщо вони ще не створені."""
    schema = """
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        registration_date TEXT DEFAULT CURRENT_TIMESTAMP,
        details TEXT
    );

    CREATE TABLE IF NOT EXISTS shares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL,
        ticker_symbol TEXT UNIQUE NOT NULL,
        total_shares INTEGER NOT NULL,
        outstanding_shares INTEGER NOT NULL,
        issue_date TEXT DEFAULT CURRENT_TIMESTAMP,
        current_price REAL DEFAULT 0.00,
        FOREIGN KEY (company_id) REFERENCES companies (id)
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        balance REAL DEFAULT 100000.00
    );

    CREATE TABLE IF NOT EXISTS portfolios (
        user_id INTEGER NOT NULL,
        share_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        PRIMARY KEY (user_id, share_id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (share_id) REFERENCES shares (id)
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        share_id INTEGER NOT NULL,
        order_type TEXT NOT NULL CHECK (order_type IN ('BUY', 'SELL')),
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'PENDING',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (share_id) REFERENCES shares (id)
    );

    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        share_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        buyer_id INTEGER NOT NULL,
        seller_id INTEGER NOT NULL,
        buy_order_id INTEGER,
        sell_order_id INTEGER,
        trade_time TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (share_id) REFERENCES shares (id),
        FOREIGN KEY (buyer_id) REFERENCES users (id),
        FOREIGN KEY (seller_id) REFERENCES users (id),
        FOREIGN KEY (buy_order_id) REFERENCES orders (id),
        FOREIGN KEY (sell_order_id) REFERENCES orders (id)
    );
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()

def execute_query(query, params=(), fetch_one=False, fetch_all=False, commit=False):
    """Універсальна функція для виконання SQL-запитів."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount

        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()
        return None
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")
        if commit:
             conn.rollback()
        return None
    finally:
        conn.close()

if __name__ == '__main__':
    print("Ініціалізація бази даних...")
    init_db()
    print("База даних ініціалізована.")