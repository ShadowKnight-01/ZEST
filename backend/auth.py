from Database.db_connect import supabase
import re               # Python RegEx
import hashlib          # extra security for password
import uuid

# Registration page
# Validate and verify format of the email
def valid_email(email):                                             # ^ = start with      $ = end with
    edu_email_pattern = r"^[\w\.-]+@[\w\.-]+\.edu\.my$"             # to compare and check as if is the email given is student email or not by check the edu and my part
    return re.match(edu_email_pattern, email) is not None                       # \w is carackter from a to Z digit from 0-9 and _ caracker

def valid_full_name(full_name):
    name_pattern = r"^[A-Za-z]+([ /@.'-][A-Za-z]+)*$"
    return re.match(name_pattern, full_name) is not None

def valid_username(username):
    username_pattern = r"^[A-Za-z0-9_.-]+$"
    return re.match(username_pattern, username) is not None

def hash_password(password):
    return hashlib.blake2b(password.encode()).hexdigest()

# Register new users on app
def register_new_user(full_name, username, email, password, confirm_password):
    
    if not valid_email(email):
        return "Please use proper education email"
    
    if not valid_full_name(full_name):
        return "Full Name can only contain these six symbols: /  space  -  @  '  ."
    
    if not valid_username(username):
        return "Username can only contain letters, numbers and underscore"

    if password != confirm_password:
        return "Password do not match"
    
    if not re.findall("[a-z]", password):
        return "Your password do not contain lower case alphabet"
    if not re.findall("[A-Z]", password):
        return "Your password do not contain upper case alphabet"
    if not re.findall(r"[\d]", password):
        return "Your password do not contain numbers"
    if len(password) < 8:
        return "Your password must contain at least 8 characters"
    
    try:
        # check if email is a duplicate
        email_check = supabase.table("users").select("id").eq("email", email).execute()
        if email_check.data:      # if email found in databse it will be true dont have then continue
            return "Email already exists"

        # check if username is a duplicate
        username_check = supabase.table("users").select("id").eq("username", username).execute()
        if username_check.data:   # if username found in databse it will be true dont have then continue
            return "Username already exists"
        
        hashed_password = hash_password(password)
        user_id = str(uuid.uuid4())    # database for unique users id
        
        # put the value in if the name email password are acording to rule given
        supabase.table("users").insert({
            "user_id"  : user_id,    # database for unique users id
            "full_name": full_name,
            "username" : username,
            "email"    : email,
            "password" : hashed_password
        }).execute()

        return {
            "status": "success",
            "user_id": user_id,
            "username": username
        }

    except Exception as e:
        return {
        "status": "error",
        "message": str(e)
    }



# log in page
def log_in_user(identifier, password):
    try:
        # check if there are email saved or not if yes check the passwordd to as if is it same or not
        result = supabase.table("users") \
            .select("password") \
            .or_(f"email.eq.{identifier},username.eq.{identifier}") \
            .execute()
        
        if not result.data:      # if email found in databse it will be true dont have then continue
            return "Email or Username not found, you may need to register" # make it so the users can put either username or email to log in
                     
        password_in_db = result.data[0]["password"]

        hashed_password = hash_password(password)

        if password_in_db != hashed_password:
            return "Wrong password, try again"
        return "User have successfully log in"
        
    except Exception as e:
        return f"Database Error: {e}"
