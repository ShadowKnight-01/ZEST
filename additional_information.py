from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFrame,
    QLabel, QLineEdit, QPushButton, 
    QComboBox, QDateEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
# Impord the backend code from the file
from backend.profile import save_additional_info
import sys

class AdditionalInfoPage(QWidget):

    # Login switching place
    def open_login(self):
        from loginpage import LoginPage
        self.login_window = LoginPage()
        self.login_window.show()
        self.close()

    def __init__(self, user_id, username, full_name=""):
        super().__init__()

        self.user_id = user_id
        self.username = username
        self.full_name = full_name

        self.setWindowTitle("Additional Infomation")
        self.resize(500, 700)

        # ===== STYLESHEET =====
        self.setStyleSheet("""
        QWidget {
            background-color: #0B1120;
            color: #F8FAFC;
            font-family: Segoe UI;
        }

        QFrame#AdditionalInfoCard {
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
                           
        QLabel#lblUserLabel{
            color: #94A3B8;
            font-size: 13px;
            font-weight: 500;
            background-color: transparent;
        }
                           
        QLabel#lblIDLabel{
            color: #64748B;
            font-size: 11px;
            font-weight: 500;
            background-color: transparent;
        }

        QLineEdit, QComboBox, QDateEdit {
            background-color: #253247;
            border: 2px solid transparent;
            border-radius: 10px;
            padding: 12px;
            color: white;
            font-size: 11pt;
        }

        QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
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
        self.AdditionalInfoCard = QFrame()
        self.AdditionalInfoCard.setObjectName("AdditionalInfoCard")
        self.AdditionalInfoCard.setMinimumWidth(350)
        self.AdditionalInfoCard.setMaximumWidth(420)

        card_layout = QVBoxLayout(self.AdditionalInfoCard)
        card_layout.setSpacing(15)

        # TITLE 
        self.title = QLabel("Additional Infomation")
        self.title.setObjectName("titleLabel")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        # SUBTITLE
        self.subtitle = QLabel("Please complete your profile details")
        self.subtitle.setObjectName("subtitleLabel")
        self.subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.subtitle)

        card_layout.addSpacing(20)

        self.lblUser = QLabel(f"Username: {self.username}")
        self.lblUser.setObjectName("lblUserLabel")
        card_layout.addWidget(self.lblUser)

        self.lblID = QLabel(f"User ID: {self.user_id}")
        self.lblID.setObjectName("lblIDLabel")
        card_layout.addWidget(self.lblID)

        # Gender
        self.inputgender = QComboBox()
        self.inputgender.addItems(["Select Gender", "Male", "Female"])
        card_layout.addWidget(self.inputgender)

        # Birth date
        self.inputBirthday = QDateEdit()
        self.inputBirthday.setCalendarPopup(True)  # enables calendar UI
        self.inputBirthday.setDate(QDate.currentDate())  # default value
        self.inputBirthday.setMinimumDate(QDate(1, 1, 1900))
        self.inputBirthday.setMaximumDate(QDate.currentDate())
        card_layout.addWidget(self.inputBirthday)

        # Course
        self.inputCourse = QLineEdit()
        self.inputCourse.setPlaceholderText("Course (e.g. Computer Science)")
        card_layout.addWidget(self.inputCourse)

        # educated Place
        self.inputEducation = QLineEdit()
        self.inputEducation.setPlaceholderText("Education Institution (e.g. University Name)")
        card_layout.addWidget(self.inputEducation)

        # State
        self.inputState = QLineEdit()
        self.inputState.setPlaceholderText("State")
        card_layout.addWidget(self.inputState)

        # City
        self.inputCity = QLineEdit()
        self.inputCity.setPlaceholderText("City")
        card_layout.addWidget(self.inputCity)

        card_layout.addSpacing(15)

        # Button
        self.btnSubmit = QPushButton("Save Information")
        self.btnSubmit.clicked.connect(self.save_info)
        card_layout.addWidget(self.btnSubmit)

        # Center Card
        main_layout.addWidget(
            self.AdditionalInfoCard,
            alignment=Qt.AlignCenter
        )
        main_layout.addStretch()

        
    # Save Function
    def save_info(self):
        gender = self.inputgender.currentText()
        birthday = self.inputBirthday.date().toString("yyyy-MM-dd")
        course = self.inputCourse.text()
        education = self.inputEducation.text()
        state = self.inputState.text()
        city = self.inputCity.text()

        if gender == "Select Gender" or not course or not education or not state or not city:
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields.")
            return

        result = save_additional_info(self.user_id, gender, birthday, course, education, state, city)

        if "successfully" in str(result).lower():
            QMessageBox.information(
                self,
                "Success",
                "Your information has been saved successfully!"
            )

            self.open_login()

        else:
            QMessageBox.warning(
                self,
                "Please fill in all required fields.",
                str(result)
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AdditionalInfoPage()
    window.show()

    sys.exit(app.exec_())