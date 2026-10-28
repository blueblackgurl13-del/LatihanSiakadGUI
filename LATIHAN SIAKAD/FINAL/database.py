
import mysql.connector
import hashlib
import hmac
import os

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",  # Isi jika MySQL kamu memakai password
    "database": "siakad"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def hash_password(password):
    salt = os.urandom(16)
    result = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        180000
    )
    return salt.hex() + "$" + result.hex()


def verify_password(password, saved_hash):
    try:
        salt_hex, hash_hex = saved_hash.split("$", 1)
        result = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            180000
        )
        return hmac.compare_digest(result.hex(), hash_hex)
    except (ValueError, TypeError):
        return False


def setup_login():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            nama VARCHAR(100) NOT NULL,
            password_hash VARCHAR(300) NOT NULL
        )
    """)

    cursor.execute(
        "SELECT id FROM users WHERE username = %s",
        ("admin",)
    )

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (username, nama, password_hash)
            VALUES (%s, %s, %s)
        """, (
            "admin",
            "Administrator SIAKAD",
            hash_password("admin123")
        ))

    conn.commit()
    cursor.close()
    conn.close()


def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM users WHERE username = %s
    """, (username,))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and verify_password(password, user["password_hash"]):
        return user

    return None