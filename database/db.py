import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "spendly.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            description TEXT,
            date        TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()

    users = [
        ("Nitish Kumar",  "nitish@example.com",  generate_password_hash("password123")),
        ("Priya Sharma",  "priya@example.com",   generate_password_hash("password123")),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        users,
    )
    conn.commit()

    nitish = conn.execute("SELECT id FROM users WHERE email = ?", ("nitish@example.com",)).fetchone()
    priya  = conn.execute("SELECT id FROM users WHERE email = ?", ("priya@example.com",)).fetchone()

    expenses = [
        (nitish["id"], 4500.00, "Bills",     "Electricity bill",       "2026-03-05"),
        (nitish["id"], 3200.00, "Food",      "Monthly groceries",      "2026-03-10"),
        (nitish["id"], 2050.00, "Health",    "Pharmacy",               "2026-03-15"),
        (nitish["id"], 1800.00, "Transport", "Uber rides",             "2026-03-18"),
        (nitish["id"],  850.00, "Shopping",  "New headphones",         "2026-03-20"),
        (priya["id"],  5200.00, "Bills",     "Rent contribution",      "2026-03-01"),
        (priya["id"],  1400.00, "Food",      "Restaurant dinners",     "2026-03-12"),
        (priya["id"],   600.00, "Transport", "Metro monthly pass",     "2026-03-02"),
        (priya["id"],  2200.00, "Shopping",  "Clothing",               "2026-03-22"),
        (priya["id"],   980.00, "Health",    "Gym membership",         "2026-03-03"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    conn.commit()
    conn.close()
    print("Database seeded with 2 users and 10 expenses.")


if __name__ == "__main__":
    init_db()
    seed_db()
    print("Done — spendly.db is ready.")
