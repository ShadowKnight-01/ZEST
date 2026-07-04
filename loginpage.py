from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox
# Impord the backend code from the file

from Database.db_connect import supabase
from backend.session import SESSION
import hashlib



class LoginPage(QWidget):
    def __init__(self, stack_manager):
        super().__init__()
        self.stack = stack_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("LogIn")
        title.setFont(QFont('Segoe UI', 25, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.txt_login = QLineEdit()
        self.txt_login.setPlaceholderText("Username or Email")
        self.txt_login.setFixedWidth(320)

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Password")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setFixedWidth(320)

        btn_login = QPushButton("Log In")
        btn_login.setFixedWidth(320)
        btn_login.clicked.connect(self.auth_user)

        btn_goto_register = QPushButton("Don\'t have an account? Create Account")
        btn_goto_register.setFixedWidth(320)
        btn_goto_register.setStyleSheet("background: transparent; padding: 3px; border: 2px solid #3B82F6; color: white;")
        btn_goto_register.clicked.connect(lambda: self.stack.setCurrentIndex(0)) # Jump straight to Register

        layout.addWidget(self.txt_login)
        layout.addWidget(self.txt_password)
        layout.addWidget(btn_login)
        layout.addWidget(btn_goto_register)
        self.setLayout(layout)

    def auth_user(self):
        ident = self.txt_login.text().strip()
        password = self.txt_password.text()

        try:
            result = supabase.table("users").select("*").or_(f"email.eq.{ident},username.eq.{ident}").execute()
            if not result.data:
                QMessageBox.warning(self, "Auth Error", "Email or Username not found, you may need to register.")
                return

            db_user = result.data[0]
            hashed_input = hashlib.blake2b(password.encode()).hexdigest()

            if db_user["password"] != hashed_input:
                QMessageBox.warning(self, "Auth Error", "Wrong password, you may try again.")
                return

            # Commit globally mapped Session memory pointers
            SESSION["user_id"] = db_user["user_id"]
            SESSION["username"] = db_user["username"]
            SESSION["full_name"] = db_user["full_name"]
            SESSION["gender"] = db_user.get("gender", "Unspecified")
            SESSION["interest"] = db_user.get("interest", "None Selected")

            # Route execution out directly to Workspace Suite Container
            self.stack.widget(4).load_profile_data()
            self.stack.widget(4).load_feed()
            self.stack.widget(4).load_chat_list()
            self.stack.setCurrentIndex(4)

        except Exception as err:
            QMessageBox.critical(self, "Runtime Stack Drop", str(err))
