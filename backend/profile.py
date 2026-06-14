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
            calculated_age = current_year - birth_date.year
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

        print(response.data)

        # optional safety check
        if not response.data:
            return "Failed to update user information"

        return "Additional information saved successfully"

    except Exception as e:    # IF  SQL crashes wrong table, collumn of conn fail it return error message
        return f"Database Error: {e}"

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
        