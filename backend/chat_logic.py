from Database.db_connect import supabase
from datetime import datetime

# saving mesage that sended
def send_message(sender_id, receiver_id, message):

    try:         
        date = datetime.now().strftime("%d-%m-%Y")  # dd-mm-yyyy
        time = datetime.now().strftime("%I:%M %p")  # %p is AM or PM -> Hour : Minute AM/PM
        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        message_memory = supabase.table("messages").insert({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "date": date,
            "time": time
            }).execute()
        
        if message_memory.data:
            return "Message sent successfully"
        else:
            return "Failed to send message"

    except Exception as e:
        return f"Database Error: {e}"

# define of getting and sendding message
def get_message(userid1, userid2):

    try:        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        message_check = supabase.table("messages").select("*").or_(f"and(sender_id.eq.{userid1},receiver_id.eq.{userid2}),and(sender_id.eq.{userid2},receiver_id.eq.{userid1})").execute()
        return message_check.data
 
    except Exception as e:
        return f"Database Error: {e}"
