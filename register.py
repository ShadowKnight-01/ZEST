from PyQt5.QtWidgets import (    # import the Pyqt widget that needed
    QWidget, QVBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt    # Qt modul for allignment and font
from PyQt5.QtGui import QFont
from Database.db_connect import supabase   # import database 
from backend.session import SESSION        # import session data
import re                                # import the module for validate, unic id and password hashing
import uuid
import hashlib
# Impord the backend code from the file

class RegisterPage(QWidget):
    def __init__(self, stack_manager):
        super().__init__()
        self.stack = stack_manager                         # save the page maneger
        self.init_ui()                                     # create the user interface

    def init_ui(self):
        layout = QVBoxLayout()                              # create the main layout
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("Create Account\nRegister to get started")     # make the page title
        title.setFont(QFont('Segoe UI', 25, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.txt_fullname = QLineEdit()                              # make the imput box for fullname
        self.txt_fullname.setPlaceholderText("Full Name")
        self.txt_fullname.setFixedWidth(320)
        
        self.txt_username = QLineEdit()                              # make the imput box for username
        self.txt_username.setPlaceholderText("Username")
        self.txt_username.setFixedWidth(320)

        self.txt_email = QLineEdit()                              # make the imput box for email
        self.txt_email.setPlaceholderText("Email (e.g. name@student.edu.my)")
        self.txt_email.setFixedWidth(320)

        self.txt_password = QLineEdit()                              # make the imput box for password and make it hide
        self.txt_password.setPlaceholderText("Password")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setFixedWidth(320)

        self.txt_confirm_pass = QLineEdit()                              # make the imput box for confirm the password
        self.txt_confirm_pass.setPlaceholderText("Confirm Password")
        self.txt_confirm_pass.setEchoMode(QLineEdit.Password)
        self.txt_confirm_pass.setFixedWidth(320)

        btn_register = QPushButton("Register")                              # make the box of register button
        btn_register.setFixedWidth(320)
        btn_register.clicked.connect(self.handle_registration)

        btn_goto_login = QPushButton("Already have an account? Login")          # create a button if the person already have sign it
        btn_goto_login.setFixedWidth(320)
        btn_goto_login.setStyleSheet("background: transparent; padding: 3px; border: 2px solid #3B82F6; color: white;")
        btn_goto_login.clicked.connect(lambda: self.stack.setCurrentIndex(3)) # Jump straight to Login

        layout.addWidget(self.txt_fullname)                      # add all the widget to the layout
        layout.addWidget(self.txt_username)
        layout.addWidget(self.txt_email)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.txt_confirm_pass)
        layout.addWidget(btn_register)
        layout.addWidget(btn_goto_login)
        self.setLayout(layout)                   # set the layout for this page

    def handle_registration(self):
        full_name = self.txt_fullname.text().strip()             # get the user input
        username = self.txt_username.text().strip()
        email = self.txt_email.text().strip()
        password = self.txt_password.text()
        confirm_password = self.txt_confirm_pass.text()

        if not full_name or not username or not email or not password:  # check if anything empty
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.edu\.my$", email):       # check if the email is student one
            QMessageBox.warning(self, "Error", "Please enter a valid student email address (e.g., name@student.edu.my)")
            return
        if not re.match(r"^[A-Za-z]+([ /@.'-][A-Za-z]+)*$", full_name):      # fullname only contain six symbols: /  space  -  @  '  . and alphebet
            QMessageBox.warning(self, "Error", "Full Name can only contain these six symbols: /  space  -  @  '  .")
            return
        if not re.match(r"^[A-Za-z0-9_.-]+$", username):                     # fullname only contain allowed charackter
            QMessageBox.warning(self, "Error", "Username can only contain letters, numbers and underscore. No space")
            return
        if password != confirm_password:                                       # check if the password same
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        # password length uppercase lovercase and num check
        if not re.search(r"[a-z]", password):
            QMessageBox.warning(self, "Error", "Your password do not contain lower case alphabet")
            return
        if not re.search(r"[A-Z]", password):
            QMessageBox.warning(self, "Error", "Your password do not contain upper case alphabet")
            return
        if not re.search(r"[\d]", password):
            QMessageBox.warning(self, "Error", "Your password do not contain numbers")
            return
        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Your password must contain at least 8 characters")
            return
        

        try:
            # Check for duplicate accounts 
            dup_check = supabase.table("users").select("email, username").or_(f"email.eq.{email},username.eq.{username}").execute()
            if dup_check.data:
                QMessageBox.information(self, "Existing Profile", "This identity profile is already registered. \nYou may go to login Page by clicking the link below register button.")
                return

            # Save the current user infor in the session
            SESSION["user_id"] = str(uuid.uuid4())
            SESSION["full_name"] = full_name
            SESSION["username"] = username

            # encrypt the password before saving it
            hashed_pw = hashlib.blake2b(password.encode()).hexdigest()
            supabase.table("users").insert({       # save the user acc to the database
                "user_id": SESSION["user_id"],
                "full_name": full_name,
                "username": username,
                "email": email,
                "password": hashed_pw
            }).execute()

            # go to the additional information
            self.stack.setCurrentIndex(1)

        except Exception as err: # show error if something goes wrong
            QMessageBox.critical(self, "Database System Fault", f"Transmission dropped: {str(err)}")
