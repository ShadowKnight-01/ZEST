import sys
import os
# This tells Python to look one folder up so it can see the 'Database' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.db_connect import supabase
from datetime import datetime


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
            return "Failed to update user information"

        return "Additional information saved successfully"

    except Exception as e:    # IF  SQL crashes wrong table, collumn of conn fail it return error message
        return f"Database Error: {e}"

# getting the information of the users in profile to show
def get_profile(user_id):
    try:        
        # FIX 1: Group all columns into a single comma-separated string
        response = supabase.table("users").select(
            "user_id, full_name, username, email, gender, age, course, education, profile_pic, user_or_admin"
        ).eq("user_id", user_id).execute()
        
        # If a matching user was found, the list won't be empty
        if response.data:
            user_dict = response.data[0] # Get the first user record dictionary
            
            # FIX 2: Convert the dictionary into a tuple to match your main.py requirements
            return (
                user_dict.get("user_id"),
                user_dict.get("full_name"),
                user_dict.get("username"),
                user_dict.get("email"),
                user_dict.get("gender"),
                user_dict.get("age"),
                user_dict.get("course"),
                user_dict.get("education"),
                user_dict.get("profile_pic"),
                user_dict.get("user_or_admin")
            )
        else:
            return "User not found"
            
    except Exception as e:    
        return f"Database Error: {e}"


def update_profile(user_id, name):
    """FIXED: Converted from raw SQL to Supabase client API."""
    try:        
        # 1. Uses the 'supabase' client instead of conn/cursor
        # 2. Changed column target to 'full_name' and 'user_id' to match your DB
        response = supabase.table("users").update({
            "full_name": name 
        }).eq("user_id", user_id).execute()
        
        # 3. Safety check to ensure the update actually happened
        if not response.data:
            return "Failed to update profile data"
            
        return "Profile updated"
        
    except Exception as e:
        return f"Database Error: {e}"