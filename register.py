from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFrame,
    QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox 
# Impord the backend code from the file
from backend.auth import register_new_user
import sys

class RegisterPage(QWidget):
    def open_login(self):
        from loginpage import LoginPage
        self.login_window = LoginPage()
        self.login_window.show()
        self.close()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Register")
        self.resize(500, 700)

        # ===== STYLESHEET =====
        self.setStyleSheet("""
        QWidget {
            background-color: #0B1120;
            color: #F8FAFC;
            font-family: Segoe UI;
        }

        QFrame#RegisterCard {
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

        QLabel#loginLabel {
            color: #94A3B8;
            font-size: 15px;
            background-color: transparent;
        }

        QLabel#loginLabel a {
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
        self.registerCard = QFrame()
        self.registerCard.setObjectName("RegisterCard")
        self.registerCard.setMinimumWidth(350)
        self.registerCard.setMaximumWidth(420)

        card_layout = QVBoxLayout(self.registerCard)
        card_layout.setSpacing(15)

        # TITLE 
        self.title = QLabel("Create Account")
        self.title.setObjectName("titleLabel")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        # SUBTITLE
        self.subtitle = QLabel("Register to get started")
        self.subtitle.setObjectName("subtitleLabel")
        self.subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.subtitle)

        card_layout.addSpacing(20)

        # Full Name
        self.inputFullName = QLineEdit()
        self.inputFullName.setPlaceholderText("Full Name")
        card_layout.addWidget(self.inputFullName)

        # Username
        self.inputUsername = QLineEdit()
        self.inputUsername.setPlaceholderText("Username")
        card_layout.addWidget(self.inputUsername)

        # Email
        self.inputEmail = QLineEdit()
        self.inputEmail.setPlaceholderText("Email")
        card_layout.addWidget(self.inputEmail)

        # Password
        self.inputPassword = QLineEdit()
        self.inputPassword.setPlaceholderText("Password")
        self.inputPassword.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.inputPassword)

        # Confirm Password
        self.inputConfirmPassword = QLineEdit()
        self.inputConfirmPassword.setPlaceholderText("Confirm Password")
        self.inputConfirmPassword.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.inputConfirmPassword)

        card_layout.addSpacing(10)

        # Register Button
        self.btnRegister = QPushButton("Register")
        self.btnRegister.clicked.connect(self.register)
        card_layout.addWidget(self.btnRegister)

        card_layout.addSpacing(15)

        # Login Link
        self.lblLogin = QLabel(
            'Already have an account? <a href="loginpage">Login</a>'
        )
        self.lblLogin.setObjectName("loginLabel")
        self.lblLogin.setAlignment(Qt.AlignCenter)
        self.lblLogin.linkActivated.connect(self.open_login)
        card_layout.addWidget(self.lblLogin)

        # Center Card
        main_layout.addWidget(
            self.registerCard,
            alignment=Qt.AlignCenter
        )

        main_layout.addStretch()

        # Press Enter in password field
        self.inputPassword.returnPressed.connect(
            self.btnRegister.click
        )
        
    # REGISTER FUNCTION
    def register(self):
        full_name = self.inputFullName.text()
        username = self.inputUsername.text()
        email = self.inputEmail.text()
        password = self.inputPassword.text()
        confirm_password = self.inputConfirmPassword.text()

        result = register_new_user(full_name, username, email, password, confirm_password)

        if "successfully registered" in result:
            QMessageBox.information(
                self,
                "Registration Successful",
                result
            )

        else:
            QMessageBox.warning(
                self,
                "Registration Failed",
                result
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = RegisterPage()
    window.show()

    sys.exit(app.exec_())