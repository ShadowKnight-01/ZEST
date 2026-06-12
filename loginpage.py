from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFrame,
    QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
# Impord the backend code from the file
from backend.auth import log_in_user
from register import RegisterPage
import sys

class LoginPage(QWidget):
    def open_register(self):
        self.register_window = RegisterPage()
        self.register_window.show()
        self.close()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Page")
        self.resize(500, 700)

        # STYLESHEET 
        self.setStyleSheet("""
        QWidget {
            background-color: #0B1120;
            color: #F8FAFC;
            font-family: Segoe UI;
        }

        QFrame#LoginCard {
            background-color: #162033;
            border-radius: 20px;
            padding: 30px;
        }

        QLabel {
            color: #F8FAFC;
        }

        QLabel#titleLabel {
            font-size: 24px;
            font-weight: 700;
            background-color: transparent;
        }

        QLabel#subtitleLabel {
            color: #94A3B8;
            font-size: 15px;
            font-weight: 500;
            background-color: transparent;
        }

        QLineEdit {
            background-color: #253247;
            border: 2px solid transparent;
            border-radius: 10px;
            padding: 12px;
            color: white;
            font-size: 11pt;
        }

        QLineEdit:focus {
            border: 2px solid #3B82F6;
        }

        QPushButton {
            background-color: #3B82F6;
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-size: 11pt;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #2563EB;
        }

        QPushButton:pressed {
            background-color: #1D4ED8;
        }

        QLabel#registerLabel {
            color: #94A3B8;
            font-size: 15px;
            background-color: transparent;
        }

        QLabel#registerLabel a {
            color: #60A5FA;
            font-size: 14px;
            font-weight: bold;
            text-decoration: none;
        }
        """)

        # MAIN LAYOUT 
        main_layout = QVBoxLayout(self)

        main_layout.addStretch()

        # LOGIN CARD 
        self.loginCard = QFrame()
        self.loginCard.setObjectName("LoginCard")
        self.loginCard.setMinimumWidth(350)
        self.loginCard.setMaximumWidth(420)

        card_layout = QVBoxLayout(self.loginCard)
        card_layout.setSpacing(15)

        # TITLE 
        self.titlelogin = QLabel("Welcome Back")
        self.titlelogin.setObjectName("titleLabel")
        self.titlelogin.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(self.titlelogin)

        # SUBTITLE 
        self.subtitle = QLabel("Sign in to continue")
        self.subtitle.setObjectName("subtitleLabel")
        self.subtitle.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(self.subtitle)
        card_layout.addSpacing(20)

        # EMAIL / USERNAME 
        self.inputUsername = QLineEdit()
        self.inputUsername.setPlaceholderText("Email or Username")
        card_layout.addWidget(self.inputUsername)

        # PASSWORD 
        self.inputPass = QLineEdit()
        self.inputPass.setPlaceholderText("Password")
        self.inputPass.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.inputPass)

        card_layout.addSpacing(10)

        # LOGIN BUTTON 
        self.btnLogin = QPushButton("Login")
        self.btnLogin.clicked.connect(self.login)
        card_layout.addWidget(self.btnLogin)

        card_layout.addSpacing(15)

        # REGISTER LINK 
        self.lblRegister = QLabel(
            'Don\'t have an account? <a href="register">Create Account</a>'
        )
        self.lblRegister.setObjectName("registerLabel")
        self.lblRegister.setAlignment(Qt.AlignCenter)
        self.lblRegister.linkActivated.connect(self.open_register)
        card_layout.addWidget(self.lblRegister)

        # Center Card
        main_layout.addWidget(
            self.loginCard,
            alignment=Qt.AlignCenter
        )

        main_layout.addStretch()

        # Press Enter in password field
        self.inputPass.returnPressed.connect(
            self.btnLogin.click
        )

    # LOGIN FUNCTION 
    def login(self):
        identifier = self.inputUsername.text().strip()    # change input inputUsername to input identifier
        password   = self.inputPass.text() 

        result = log_in_user(identifier, password)

        print(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginPage()
    window.show()

    sys.exit(app.exec_())