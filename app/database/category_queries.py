from app.database.connection import get_conn

def get_categories():
    conn = get_conn()
    if not conn:
        return []
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM categories")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return []
    finally:
        conn.close()
