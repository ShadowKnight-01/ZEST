import re     #Python RegEx
from Database.connection import get_connection

# Validate and verify format of the email
def valid_email(email):
    edu_email_pattern = r"^[\w\.-]+@[\w\.-]+\.edu\.my$" # to compare and check as if is the email given is student email or not by check the edu and my part
    return re.match(edu_email_pattern, email)     # \w is carackter from a to Z digit from 0-9 and _ caracker
                                                  # ^ = start with      $ = end with
# Register new user on app
def register_new_user(name, email, password, comfirm_password):

    if not valid_email(email):
        return "Please use proper education email"
    
    conn = get_connection()
    cursor = conn.cursor()
