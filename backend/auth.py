import re               #Python RegEx
from Database.connection import connection

# Validate and verify format of the email
def valid_email(email):                                             # ^ = start with      $ = end with
    edu_email_pattern = r"^[\w\.-]+@[\w\.-]+\.edu\.my$"             # to compare and check as if is the email given is student email or not by check the edu and my part
    return re.match(edu_email_pattern, email)                       # \w is carackter from a to Z digit from 0-9 and _ caracker
                                                                    
# Register new user on app
def register_new_user(name, email, password, confirm_password):

    if not valid_email(email):
        return "Please use proper education email"

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
        return "Email is already exists"
    
    # put the value in if the name email password are acording to rule given
    cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    conn.commit()

    # close curser and conection
    cursor.close()
    conn.close()

    return "User have successfully registered"