from Database.db_connect import supabase
from datetime import datetime

# saving mesage that sended
def send_message(sender_id, receiver_id, message):

    try:         
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")  # dd-mm-yyyy
        time = now.strftime("%I:%M %p")  # %p is AM or PM -> Hour : Minute AM/PM
        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        message_memory = supabase.table("messages").insert({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "date": date,
            "time": time
        }).execute()
        
        return bool(message_memory.data)

    except Exception as e:
        return f"Database Error: {e}"

# define of getting and sendding message
def get_message(userid1, userid2):

    try:        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        message_check = supabase.table("messages").select("*").or_(
            f"and(sender_id.eq.{userid1},receiver_id.eq.{userid2}),"
            f"and(sender_id.eq.{userid2},receiver_id.eq.{userid1})"
        ).execute()

        return message_check.data or []
 
    except Exception as e:
        return f"Database Error: {e}"
    
def load_chat_users(self, user_id):
    data = supabase.table("messages").select("*").or_(
        f"sender_id.eq.{user_id},receiver_id.eq.{user_id}"
    ).execute().data

    user = set()

    for messages in data:
        if messages["sender_id"] != user_id:
            user.add(messages["sender_id"])
        if messages["receiver_id"] != user_id:
            user.add(messages["receiver_id"])

    self.list_friends.clear()

    for u in user:
        self.list_friends.addItem(str(u))
