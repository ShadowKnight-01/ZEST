from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox, 
    QLabel, QLineEdit, QPushButton,
    QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Database.db_connect import supabase
from backend.session import SESSION
from datetime import datetime


class AdditionalInfoPage(QWidget):
    def __init__(self, stack_manager):
        super().__init__()
        self.stack = stack_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignCenter)
        scroll_layout.setSpacing(12)

        title = QLabel("Additional Information")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        layout.addWidget(title)

        self.cmb_gender = QComboBox()
        self.cmb_gender.addItems(["Male", "Female"])
        self.cmb_gender.setStyleSheet("border: 2px solid #3B82F6;")
        self.cmb_gender.setFixedWidth(320)

        self.txt_dob = QLineEdit()
        self.txt_dob.setPlaceholderText("Date of Birth (DD-MM-YYYY)")
        self.txt_dob.setStyleSheet("border: 2px solid #3B82F6;")
        self.txt_dob.setFixedWidth(320)

        self.txt_course = QLineEdit()
        self.txt_course.setPlaceholderText("Course (e.g., Computer Science)")
        self.txt_course.setStyleSheet("border: 2px solid #3B82F6;")
        self.txt_course.setFixedWidth(320)

        self.cmb_education = QComboBox()
        self.cmb_education.addItems(["Diploma", "Foundation/Matriculation", "Bachelor's Degree", "Master's Degree", "PhD"])
        self.cmb_education.setStyleSheet("border: 2px solid #3B82F6;")
        self.cmb_education.setFixedWidth(320)

        self.txt_state = QLineEdit()
        self.txt_state.setPlaceholderText("State (e.g., Selangor)")
        self.txt_state.setStyleSheet("border: 2px solid #3B82F6;")
        self.txt_state.setFixedWidth(320)

        self.txt_city = QLineEdit()
        self.txt_city.setPlaceholderText("City (e.g., Cyberjaya)")
        self.txt_city.setStyleSheet("border: 2px solid #3B82F6;")
        self.txt_city.setFixedWidth(320)

        btn_next = QPushButton("Continue")
        btn_next.setFixedWidth(320)
        btn_next.setStyleSheet("border: 2px solid #3B82F6;")
        btn_next.clicked.connect(self.save_data)

        scroll_layout.addWidget(QLabel("Select Gender:"))
        scroll_layout.addWidget(self.cmb_gender)
        scroll_layout.addWidget(QLabel("Date of Birth: (dd-mm-yyyy)"))
        scroll_layout.addWidget(self.txt_dob)
        scroll_layout.addWidget(QLabel("Academic Course:"))
        scroll_layout.addWidget(self.txt_course)
        scroll_layout.addWidget(QLabel("Current Education Level:"))
        scroll_layout.addWidget(self.cmb_education)
        scroll_layout.addWidget(QLabel("State :"))
        scroll_layout.addWidget(self.txt_state)
        scroll_layout.addWidget(QLabel("City :"))
        scroll_layout.addWidget(self.txt_city)

        scroll_layout.addWidget(btn_next)
        scroll.setWidget(scroll_content)
        main_box = QVBoxLayout(self)
        main_box.addWidget(scroll)
        self.setLayout(main_box)

    def save_data(self):
        dob_str = self.txt_dob.text().strip() # dob date of birth
        gender = self.cmb_gender.currentText()
        education = self.cmb_education.currentText()
        course = self.txt_course.text().strip()
        state = self.txt_state.text().strip()
        city = self.txt_city.text().strip()
        
        birth_date = None
        for format in ("%Y-%m-%d", "%d-%m-%Y"):
            try:
                birth_date = datetime.strptime(dob_str, format)
                break
            except ValueError:
                continue
        if not birth_date:
            QMessageBox.warning(self, "Error", "Please format date as DD-MM-YYYY or YYYY-MM-DD.")
            return

        clean_supabase_date = birth_date.strftime("%Y-%m-%d")
        today = datetime.now()
        age = today.year - birth_date.year

        try:
            supabase.table("users").update({
                "gender": gender,
                "birthday": clean_supabase_date,
                "age": age,
                "course": course,
                "education": education,
                "state": state,
                "city": city
            }).eq("user_id", SESSION["user_id"]).execute()

            SESSION["gender"] = gender
            self.stack.setCurrentIndex(2) # Advance to Interests
        except Exception as err:
            QMessageBox.critical(self, "Error", f"Failed updating traits: {str(err)}")
