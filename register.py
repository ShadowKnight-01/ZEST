from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, 
    QMessageBox, QListWidget, QFrame, QCheckBox, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Database.db_connect import supabase
from backend.session import SESSION
import re
import uuid
import hashlib
# Impord the backend code from the file

class RegisterPage(QWidget):
    def __init__(self, stack_manager):
        super().__init__()
        self.stack = stack_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("Create Account\nRegister to get started")
        title.setFont(QFont('Segoe UI', 25, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.txt_fullname = QLineEdit()
        self.txt_fullname.setPlaceholderText("Full Name")
        self.txt_fullname.setFixedWidth(320)
        
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Username")
        self.txt_username.setFixedWidth(320)

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("Email (e.g. name@student.edu.my)")
        self.txt_email.setFixedWidth(320)

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Password")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setFixedWidth(320)

        self.txt_confirm_pass = QLineEdit()
        self.txt_confirm_pass.setPlaceholderText("Confirm Password")
        self.txt_confirm_pass.setEchoMode(QLineEdit.Password)
        self.txt_confirm_pass.setFixedWidth(320)

        btn_register = QPushButton("Register")
        btn_register.setFixedWidth(320)
        btn_register.clicked.connect(self.handle_registration)

        btn_goto_login = QPushButton("Already have an account? Login")
        btn_goto_login.setFixedWidth(320)
        btn_goto_login.setStyleSheet("background: transparent; padding: 3px; border: 2px solid #3B82F6; color: white;")
        btn_goto_login.clicked.connect(lambda: self.stack.setCurrentIndex(3)) # Jump straight to Login

        layout.addWidget(self.txt_fullname)
        layout.addWidget(self.txt_username)
        layout.addWidget(self.txt_email)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.txt_confirm_pass)
        layout.addWidget(btn_register)
        layout.addWidget(btn_goto_login)
        self.setLayout(layout)

    def handle_registration(self):
        full_name = self.txt_fullname.text().strip()
        username = self.txt_username.text().strip()
        email = self.txt_email.text().strip()
        password = self.txt_password.text()
        confirm_password = self.txt_confirm_pass.text()

        if not full_name or not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.edu\.my$", email):
            QMessageBox.warning(self, "Error", "Please enter a valid student email address (e.g., name@student.edu.my)")
            return
        if not re.match(r"^[A-Za-z]+([ /@.'-][A-Za-z]+)*$", full_name):
            QMessageBox.warning(self, "Error", "Full Name can only contain these six symbols: /  space  -  @  '  .")
            return
        if not re.match(r"^[A-Za-z0-9_.-]+$", username):
            QMessageBox.warning(self, "Error", "Username can only contain letters, numbers and underscore")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        
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
            # Check for duplicate accounts gracefully
            dup_check = supabase.table("users").select("email, username").or_(f"email.eq.{email},username.eq.{username}").execute()
            if dup_check.data:
                QMessageBox.information(self, "Existing Profile", "This identity profile is already registered. \nYou may go to login Page by clicking the link below register button.")
                return

            # Set local runtime memory token
            SESSION["user_id"] = str(uuid.uuid4())
            SESSION["full_name"] = full_name
            SESSION["username"] = username

            # Push baseline profile to DB
            hashed_pw = hashlib.blake2b(password.encode()).hexdigest()
            supabase.table("users").insert({
                "user_id": SESSION["user_id"],
                "full_name": full_name,
                "username": username,
                "email": email,
                "password": hashed_pw
            }).execute()

            # Advance onwards to step 2
            self.stack.setCurrentIndex(1)

        except Exception as err:
            QMessageBox.critical(self, "Database System Fault", f"Transmission dropped: {str(err)}")