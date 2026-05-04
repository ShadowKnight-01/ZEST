import re               #Python RegEx
from Database.connection import connection

# Registration page

# Validate and verify format of the email
def valid_email(email):                                             # ^ = start with      $ = end with
    edu_email_pattern = r"^[\w\.-]+@[\w\.-]+\.edu\.my$"             # to compare and check as if is the email given is student email or not by check the edu and my part
    return re.match(edu_email_pattern, email) is not None                       # \w is carackter from a to Z digit from 0-9 and _ caracker

def valid_full_name(full_name):
    name_patern = r"^[A-Za-z]+([ /@-][A-Za-z]+)*$"
    return re.match(name_patern, full_name) is not None

def valid_preferred_name(preferred_name):
    name_patern = r"^[A-Za-z]+$"
    return re.match(name_patern, preferred_name) is not None
                                                                    
# Register new user on app
def register_new_user(full_name, preferred_name, email, password, confirm_password):

    if not valid_email(email):
        return "Please use proper education email"
    
    if not valid_full_name(full_name):
        return "Full Name can only contain these four symbol ( "/", " ", "-", "@")"
    
    if not valid_preferred_name(preferred_name):
        return "Name must contain only alphabets no numbers or any special character"

    if password != confirm_password:
        return "Password do not match"
    
    if not re.findall("[a-z]", password):
        return "Your password do not contain lower case alphabet"
    if not re.findall("[A-Z]", password):
        return "Your password do not contain upper case alphabet"
    if not re.findall("[\d]", password):
        return "Your password do not contain numbers"
    
    # idnum = make unic id num calcalation like each person get one unic num when their sign in
    
    conn = connection()
    cursor = conn.cursor()

    # check if it is a duplicate
    cursor.execute("SELECT * FROM user WHERE email=%s", (email,))   # , after email to make it tuple without , it will be just string. %s is like a empty slot/space to put things
    if cursor.fetchone():      # if email found in databse it will be true dont have then continue
        cursor.close()
        conn.close()
        return "Email already exists"
    
    # put the value in if the name email password are acording to rule given
    cursor.execute("INSERT INTO user (full_name, preferred_name, email, password) VALUES (%s, %s, %s, %s)", (full_name, preferred_name, email, password))
    conn.commit()

    # close curser and conection
    cursor.close()
    conn.close()

    return "User have successfully registered"

# log in page

def log_in_user(identifier, password):

    conn = connection()
    cursor = conn.cursor()

    # check if there are email saved or not if yes check the passwordd to as if is it same or not
    cursor.execute("SELECT password FROM user WHERE email=%s OR preferred_name=%s", (identifier, identifier)) # make it so the user can put either name or email to log in

    result = cursor.fetchone()
    
    if not result: 
        cursor.close()
        conn.close()
        return "Email not found, You may need to register your email"
    
    password_in_db = result[0]

    if password_in_db != password:
        cursor.close()
        conn.close()
        return "Wrong password, try again"
    
    cursor.close()
    conn.close()

    return "User have successfully log in"

#   You should soon add:
#   hashes=d password    security
#   minimum password length