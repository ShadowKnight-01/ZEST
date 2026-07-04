from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QCheckBox, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Database.db_connect import supabase
from backend.session import SESSION

class InterestPage(QWidget):
    """
        Initializes the interests selection view.
        :param stack_manager: QStackedWidget manager controlling app navigation layers.
        :param return_to_profile: Boolean flag indicating if this page was accessed 
                                  via the profile editor rather than original onboarding.
        """
    def __init__(self, stack_manager, return_to_profile=False):
        super().__init__()
        self.stack = stack_manager
        self.return_to_profile = return_to_profile
        self.init_ui()

    def init_ui(self):
        """
        Sets up the layout, dynamic grid of interest checkboxes, and submission action triggers.
        """
        # Primary master vertical box layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

# Page Headline Label
        title = QLabel("Select Hobbies / Interests")
        title.setFont(QFont('Segoe UI', 25, QFont.Bold))
        layout.addWidget(title)

# Create a sub-widget container to isolate grid arrangement logic safely
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        
        # Predefined hobby tags for selection mapping
        self.tags = ["Games", "Music", "Tech", "Cooking", "Art", "Books", "Sports", "Traveling", "Movies", "Photography"]
        self.boxes = []

# Dynamically loop and build checkbox matrices across a 2-column layout
        for index, tag in enumerate(self.tags):
            box = QCheckBox(tag)
            # Row calculation uses floor division (index // 2), Column uses modulo remainder calculation (index % 2)
            grid.addWidget(box, index // 2, index % 2)
            self.boxes.append(box)# Track UI object references to read states later

        layout.addWidget(grid_widget)

# Confirm and Submit action registration trigger
        btn_save = QPushButton("Save && Finish Profile Form")
        btn_save.setFixedWidth(320)
        btn_save.clicked.connect(self.commit_interests)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def commit_interests(self):
        """
        Aggregates checked tags, validates that at least one trait is selected,
        commits records upstream onto Supabase tables, and handles interface redirection.
        """
        # Filter list comprehension extracting titles from actively clicked checkbox instances
        selected = [b.text() for b in self.boxes if b.isChecked()]
        # Validation Check: Enforce picking a minimum of one item parameter
        if not selected:
            QMessageBox.warning(self, "Validation Error", "Select at least 1 interest tag.")
            return

# Flatten string arrays into single comma-delimited strings (e.g., "Games, Tech, Art")
        interests_csv = ", ".join(selected)
        try:
            supabase.table("users").update({"interest": interests_csv}).eq("user_id", SESSION["user_id"]).execute()
            # Update the global local runtime memory session context cache string reference directly
            SESSION["interest"] = interests_csv
            
            QMessageBox.information(self, "Success", "Profile data completed successfully.")
            
            # Check context source flag routing path workflows
            if self.return_to_profile:
                # Routed via the Profile Edit View sub-layer
                self.stack.setCurrentIndex(4) # Bounce to Core Window Stack Frame
                self.stack.widget(4).switch_tab(0) # Route inside main stack directly to view 0 (Profile Tab)
            else:
                # Flow: Standard Onboarding route, proceed to natural Log In authentication page index template sequence
                self.stack.setCurrentIndex(3) # Route to natural Authentication Log In sequence
        except Exception as err:
            # Display any server exceptions or backend interaction errors directly to the user interface
            QMessageBox.critical(self, "Error", str(err))
