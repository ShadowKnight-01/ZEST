from Database.connection import connection
from datetime import datetime

# saving mesage that sended
def send_message(sender_id, receiver_id, message):

    conn = connection()
    cursor = conn.cursor()

    try:         
        date = datetime.now().strftime("%d-%m-%Y")
        time = datetime.now().strftime("%I:%M %p")
        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        cursor.execute("INSERT INTO messages (sender_id, receiver_id, message, date, time) VALUES (%s, %s, %s, %s, %s)", (sender_id, receiver_id, message, date, time))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"Database Error: {e}"
    finally:
        # close curser and conection
        cursor.close()
        conn.close()
    return "message sended succesfully"

# define of getting and sendding message
def get_message(userid1, userid2):

    conn = connection()
    cursor = conn.cursor()

    try:        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        cursor.execute("SELECT * FROM messages WHERE (sender_id=%s AND receiver_id=%s) OR (sender_id=%s AND receiver_id=%s)", (userid1, userid2, userid2, userid1))
        return cursor.fetchall()
    except Exception as e:
        return f"Database Error: {e}"
    finally:
        # close curser and conection
        cursor.close()
        conn.close()