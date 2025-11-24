from app.database.connection import get_conn

def get_all_posts(limit=10, offset=0, sort_order="DESC", category_id=None):
    conn = get_conn()
    if not conn:
        return []
    try:
        with conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT p.*, u.name AS author, c.name AS category
                FROM posts p
                LEFT JOIN users u ON p.user_id = u.id
                LEFT JOIN categories c ON p.category_id = c.id
            """
            params = []

            # Filtering
            if category_id:
                query += " WHERE p.category_id = %s"
                params.append(category_id)

            # Sorting
            if sort_order.upper() not in ["ASC", "DESC"]:
                sort_order = "DESC"
            query += f" ORDER BY p.posted_at {sort_order}"

            # Pagination
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, tuple(params))
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []
    finally:
        conn.close()

def get_post_by_id(post_id):
    conn = get_conn()
    if not conn:
        return None
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT p.*,
                       u.name AS author, c.name AS category
                FROM posts p
                LEFT JOIN users u ON p.user_id = u.id
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.id = %s
            """, (post_id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching post: {e}")
        return None
    finally:
        conn.close()

def insert_new_post(title, subtitle, body, category_id, user_id):
    conn = get_conn()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO posts (title, subtitle, body, category_id, user_id, posted_at)
                VALUES (%s, %s, %s, %s, %s, CURDATE())
            """, (title, subtitle, body, category_id, user_id))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting post: {e}")
        return False
    finally:
        conn.close()

def delete_users_post(post_id, user_id):
    conn = get_conn()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM posts WHERE id = %s AND user_id = %s", (post_id,user_id))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting post: {e}")
        return False
    finally:
        conn.close()

def get_users_posts(user_id):
    conn = get_conn()
    if not conn:
        return []
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT p.*,
                       u.name AS author, c.name AS category
                FROM posts p
                LEFT JOIN users u ON p.user_id = u.id
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE u.id = %s
            """, (user_id,))
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching user's posts: {e}")
        return []
    finally:
        conn.close()

def update_users_post(post_id, title, subtitle, body, category_id, user_id):
    conn = get_conn()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("""UPDATE posts 
                           SET title=%s, subtitle=%s, body=%s, category_id=%s
                           WHERE id = %s AND user_id = %s""", 
                           (title, subtitle, body, category_id, post_id, user_id))
            conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating post: {e}")
        return False
    finally:
        conn.close()

def get_all_posts_ids():
    conn = get_conn()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT id FROM posts""")
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()