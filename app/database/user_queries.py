from app.database.connection import get_conn
from mysql.connector.errors import IntegrityError

def insert_registration_data(name, username, email, password_hash):
    conn = get_conn()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (name, username, email, password)
                VALUES (%s, %s, %s, %s)
            """, (name, username, email, password_hash))
            conn.commit()
        return True
    except IntegrityError:
        return False
    except Exception as e:
        print(f"Error inserting user: {e}")
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_conn()
    if not conn:
        return None
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        conn.close()
