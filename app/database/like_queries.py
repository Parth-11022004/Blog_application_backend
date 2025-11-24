from app.database.connection import get_conn
from mysql.connector.errors import IntegrityError

def add_like(user_id, post_id):
    conn = get_conn()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO likes (user_id, post_id)
                VALUES (%s, %s)
            """, (user_id, post_id))
            conn.commit()
        return True
    except IntegrityError:
        return False
    except Exception as e:
        print(f"Error adding like: {e}")
        return False
    finally:
        conn.close()


def remove_like(user_id, post_id):
    conn = get_conn()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM likes WHERE user_id = %s AND post_id = %s
            """, (user_id, post_id))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error removing like: {e}")
        return False
    finally:
        conn.close()


def get_like_count(post_id):
    conn = get_conn()
    if not conn:
        return 0
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT COUNT(*) AS count FROM likes WHERE post_id = %s
            """, (post_id,))
            result = cursor.fetchone()
            return result["count"]
    except Exception as e:
        print(f"Error getting like count: {e}")
        return 0
    finally:
        conn.close()


def check_user_liked(user_id, post_id):
    conn = get_conn()
    if not conn:
        return False
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT 1 FROM likes WHERE user_id = %s AND post_id = %s
            """, (user_id, post_id))
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error checking like: {e}")
        return False
    finally:
        conn.close()
