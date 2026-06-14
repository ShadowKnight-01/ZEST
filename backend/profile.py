from Database.connection import connection
# from datetime import datetime   might be in use later or not 

# getting the information of the users in profile to show
def get_profile(user_id):

    conn = connection()
    cursor = conn.cursor()

    try:        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        cursor.execute("SELECT user_id, full_name, username, email, gender, age, course, education, profile_pic, user_or_admin FROM users WHERE id=%s", (user_id,))
        return cursor.fetchone()
    except Exception as e:    # IF  SQL crashes wrong table, collumn of conn fail it return error message
        return f"Database Error: {e}"
    finally:
        # close curser and conection
        cursor.close()
        conn.close()

def update_profile(user_id, name):

    conn = connection()
    cursor = conn.cursor()

    try:        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        cursor.execute("UPDATE users SET name=%s WHERE id=%s", (name, user_id))
        conn.commit()
        return "Profile updated"
    except Exception as e:
        return f"Database Error: {e}"
    finally:
        # close curser and conection
        cursor.close()
        conn.close()
        