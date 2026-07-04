from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QCheckBox, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Database.db_connect import supabase
from backend.session import SESSION

class InterestPage(QWidget):
    def __init__(self, stack_manager, return_to_profile=False):
        super().__init__()
        self.stack = stack_manager
        self.return_to_profile = return_to_profile
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        title = QLabel("Select Hobbies / Interests")
        title.setFont(QFont('Segoe UI', 25, QFont.Bold))
        layout.addWidget(title)

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        
        self.tags = ["Games", "Music", "Tech", "Cooking", "Art", "Books", "Sports", "Traveling", "Movies", "Photography"]
        self.boxes = []

        for index, tag in enumerate(self.tags):
            box = QCheckBox(tag)
            grid.addWidget(box, index // 2, index % 2)
            self.boxes.append(box)

        layout.addWidget(grid_widget)

        btn_save = QPushButton("Save && Finish Profile Form")
        btn_save.setFixedWidth(320)
        btn_save.clicked.connect(self.commit_interests)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def commit_interests(self):
        selected = [b.text() for b in self.boxes if b.isChecked()]
        if not selected:
            QMessageBox.warning(self, "Validation Error", "Select at least 1 interest tag.")
            return

        interests_csv = ", ".join(selected)
        try:
            supabase.table("users").update({"interest": interests_csv}).eq("user_id", SESSION["user_id"]).execute()
            SESSION["interest"] = interests_csv
            
            QMessageBox.information(self, "Success", "Profile data completed successfully.")
            
            if self.return_to_profile:
                # Routed via the Profile Edit View sub-layer
                self.stack.setCurrentIndex(4) # Bounce to Core Window Stack Frame
                self.stack.widget(4).switch_tab(0) # Route inside main stack directly to view 0 (Profile Tab)
            else:
                self.stack.setCurrentIndex(3) # Route to natural Authentication Log In sequence
        except Exception as err:
            QMessageBox.critical(self, "Error", str(err))
