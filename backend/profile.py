from Database.db_connect import supabase
from datetime import datetime

# getting the information of the users in profile to show
def get_profile(user_id):
    try:        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        response = supabase.table("users").select("user_id, full_name, username, email, gender, age, course, education, user_or_admin").eq("user_id", user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:    # IF  SQL crashes wrong table, collumn of conn fail it return error message
        return f"Database Error: {e}"

def update_profile(user_id, name):

    try:        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        responce = supabase.table("users").update({"full_name": name}).eq("user_id", user_id).execute()
        return "Profile updated"
    except Exception as e:
        return f"Database Error: {e}"

        
def save_additional_info(user_id, gender, birthday_str, course, education, state, city):

    try:        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        if not all([user_id, gender, birthday_str, course, education, state, city]):
            return "All fields must be filled"
        
        if gender not in ["Male", "Female"]:
            return "Please select a valid gender"     
        
        try:
            birth_date = datetime.strptime(birthday_str, "%Y-%m-%d")
            current_year = datetime.now().year
            calculated_age = current_year - birth_date.year      #  this year minus with birth year is the age
        except Exception:
            calculated_age = None

        # Update Database
        response = supabase.table("users").update({
            "gender"    : gender,
            "age"       : calculated_age,
            "birthday"  : birthday_str,
            "course"    : course,
            "education" : education,
            "state"     : state,
            "city"      : city
        }).eq("user_id", user_id).execute()

        # optional safety check
        if not response.data:
            return {
                "status": "error",
                "message": "Failed to update user information"
            }

        return {
            "status": "success",
            "user_id": user_id
        }
        

    except Exception as e:    # IF  SQL crashes wrong table, collumn of conn fail it return error message
        return f"Database Error: {e}"
    
def save_interest(user_id, interest):
    try:        
        # put the value in if the sender_id receiver_id and message are acording to rule given
        if not all([user_id, interest]):
            return "All fields must be filled"
        
        # Update Database
        response = supabase.table("users").update({
            "interests"  : interest,
        }).eq("user_id", user_id).execute()

        # optional safety check
        if not response.data:
            return "Failed to update interest"

        return "interest saved successfully"

    except Exception as e:    # IF  SQL crashes wrong table, collumn of conn fail it return error message
        return f"Database Error: {e}"
