from app.database.connection import get_conn

def insert_comment(body, user_id, post_id):
    conn = get_conn()
    if not conn:
        return False

    try:
        
        with conn.cursor(dictionary=True) as cursor:
            query = """
                INSERT INTO comments (body, posted_at, user_id, post_id)
                VALUES (%s, CURDATE(), %s, %s)
            """
            cursor.execute(query, (body, user_id, post_id))
            conn.commit()
            return True
    except Exception as e:
        print("Error inserting comment:", e)
        return False
    finally:
        conn.close()


def get_all_comments():
    conn = get_conn()
    if not conn:
        return []
    try:
        
        with conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT c.*,
                       u.name AS author, p.title AS post_title
                FROM comments c
                JOIN users u ON c.user_id = u.id
                JOIN posts p ON c.post_id = p.id
        
            """
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print("Error fetching all comments:", e)
        return []
    finally:
        conn.close()


def get_comments_by_post(post_id):
    conn = get_conn()
    if not conn:
        return []
    try:
        
        with conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT c.*,
                       u.name AS author
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = %s
                
            """
            cursor.execute(query, (post_id,))
            return cursor.fetchall()
    except Exception as e:
        print("Error fetching comments for post:", e)
        return []
    finally:
        conn.close()


def get_comments_by_user(user_id):
    conn = get_conn()
    if not conn:
        return []
    try:
        
        with conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT c.*,
                       p.title AS post_title
                FROM comments c
                JOIN posts p ON c.post_id = p.id
                WHERE c.user_id = %s
              
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
    except Exception as e:
        print("Error fetching user comments:", e)
        return []
    finally:
        conn.close()


def get_comment_by_id(comment_id):
    conn = get_conn()
    if not conn:
        return []
    try:
        
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM comments WHERE id = %s", (comment_id,))
            return cursor.fetchone()
    except Exception as e:
        print("Error fetching comment by ID:", e)
        return None
    finally:
        conn.close()


def update_comment(comment_id, new_body):
    conn = get_conn()
    if not conn:
        return False
    try:
        
        with conn.cursor() as cursor:
            query = "UPDATE comments SET body = %s WHERE id = %s"
            cursor.execute(query, (new_body, comment_id))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print("Error updating comment:", e)
        return False
    finally:
        conn.close()


def delete_comment(comment_id):
    conn = get_conn()
    if not conn:
        return False
    try:
        
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print("Error deleting comment:", e)
        return False
    finally:
        conn.close()
