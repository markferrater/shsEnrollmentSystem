"""
seed_credentials.py
───────────────────
Run this ONCE to:
  1. Create the announcements table if it doesn't exist.
  2. Insert bcrypt-hashed credentials for staff ('staff123')
     and admin ('admin123') — only if they don't already exist.

Usage:
    python seed_credentials.py
"""

import bcrypt
import pymysql

DB_CONFIG = dict(
    host='localhost',
    user='root',
    password='',
    database='enrollment_database'
)


def get_conn():
    return pymysql.connect(**DB_CONFIG)


def hash_pw(plain: str) -> str:
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def run():
    conn = get_conn()
    cur  = conn.cursor()

    # ── 1. Create announcements table ──────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            title       VARCHAR(255) NOT NULL,
            content     TEXT         NOT NULL,
            target      VARCHAR(20)  NOT NULL DEFAULT 'All',
            posted_by   VARCHAR(100),
            posted_date DATETIME     DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── 2. Seed staff_credentials ──────────────────────────────────
    cur.execute("SELECT COUNT(*) FROM staff_credentials WHERE username = 'staff'")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO staff_credentials (username, password) VALUES (%s, %s)",
            ('staff', hash_pw('staff123'))
        )
        print("✅  staff credential inserted  (username=staff  password=staff123)")
    else:
        print("ℹ️   staff credential already exists — skipped")

    # ── 3. Seed admin_credentials ──────────────────────────────────
    cur.execute("SELECT COUNT(*) FROM admin_credentials WHERE username = 'admin'")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO admin_credentials (username, password) VALUES (%s, %s)",
            ('admin', hash_pw('admin123'))
        )
        print("✅  admin credential inserted   (username=admin  password=admin123)")
    else:
        print("ℹ️   admin credential already exists — skipped")

    conn.commit()
    cur.close()
    conn.close()
    print("\nDone.")


if __name__ == '__main__':
    run()