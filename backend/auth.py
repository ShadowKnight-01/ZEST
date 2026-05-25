import re               #Python RegEx
from Database.connection import connection
from datetime import datetime

# Registration page

# Validate and verify format of the email
def valid_email(email):                                             # ^ = start with      $ = end with
    edu_email_pattern = r"^[\w\.-]+@[\w\.-]+\.edu\.my$"             # to compare and check as if is the email given is student email or not by check the edu and my part
    return re.match(edu_email_pattern, email) is not None                       # \w is carackter from a to Z digit from 0-9 and _ caracker


def valid_full_name(full_name):
    name_pattern = r"^[A-Za-z]+([ /@.'-][A-Za-z]+)*$"
    return re.match(name_pattern, full_name) is not None

def valid_username(username):
    username_pattern = r"^[A-Za-z0-9_]+$"
    return re.match(username_pattern, username) is not None


# Register new user on app
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
    if not re.findall("[\d]", password):
        return "Your password do not contain numbers"
    if len(password) < 8:
        return "Your password must contain at least 8 characters"
    
    conn = connection()
    cursor = conn.cursor()

    try:
        # check if email or usernameis a duplicate
        cursor.execute("SELECT email, username FROM user WHERE email=%s OR username=%s", (email, username))   # %s is like a empty slot/space to put things
        if cursor.fetchone():      # if email , username found in databse it will be true dont have then continue
            return "Email or Username already exists"
        
        # put the value in if the name email password are acording to rule given
        cursor.execute("INSERT INTO user (full_name, username, email, password) VALUES (%s, %s, %s, %s)", (full_name, username, email, password))

        # database for unique user id
        database_last_id = cursor.lastrowid

        # idnum = make unic id num calcalation like each person get one unic num when their sign in
        today = datetime.now().strftime("%y%m%d%H%M")
        unique_id = f"{today}{database_last_id:04d}"

        cursor.execute("UPDATE user SET user_id = %s WHERE id = %s", (unique_id, database_last_id))
        conn.commit()

    except Exception as e:
        conn.rollback()
        return f"Database Error: {e}"

    finally:
        # close curser and conection
        cursor.close()
        conn.close()
    return f"User have successfully registered. ID Num = {unique_id}."


# log in page
def log_in_user(identifier, password):

    conn = connection()
    cursor = conn.cursor()

    try:
        # check if there are email saved or not if yes check the passwordd to as if is it same or not
        cursor.execute("SELECT password FROM user WHERE email=%s OR username=%s", (identifier, identifier)) # make it so the user can put either username or email to log in

        result = cursor.fetchone()
        
        if not result: 
            return "Email or Username not found, You may need to register your account"
        
        password_in_db = result[0]

        if password_in_db != password:
            return "Wrong password, try again"
        
    except Exception as e:
        conn.rollback()
        return f"Database Error: {e}"
        
    finally:
        cursor.close()
        conn.close()

    return "User have successfully log in"

#   You should soon add:
#   hashes=d password    security