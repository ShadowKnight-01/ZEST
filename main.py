import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget
)

from StyleSheet import Style_used_to_in_Login
# Import your generated UI classes
<<<<<<< HEAD
from zest_main import Ui_MainWindow
from chat_page import Ui_Form as Ui_ChatForm
from pfpinterface import Ui_Form as Ui_ProfileForm
from backend.profile import (get_profile, update_profile)

# Step 1: Wrap your secondary forms into proper standalone custom Widgets
class ChatPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ChatForm()
        self.ui.setupUi(self)


class ProfilePage(QtWidgets.QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProfileForm()
        self.ui.setupUi(self)
        self.user_id = user_id 
        self.load_user_data()
        self.ui.pushButton.clicked.connect(self.edit_profile_action)
        self.ui.pushButton_2.clicked.connect(self.post_action) 
    def load_user_data(self):
        user_data = get_profile(self.user_id)
        if isinstance(user_data, tuple):
            full_name = user_data[1]
            username = user_data[2]
            self.ui.label_2.setText(full_name)
            self.ui.label_4.setText(f"@{username}")
        else:
            print(f"Could not load database profile data: {user_data}")
    def edit_profile_action(self):
        print("Edit Profile button clicked!")
    def post_action(self):
        post_content = self.ui.textEdit.toPlainText()
        if post_content.strip():
            print(f"User {self.user_id} posted: {post_content}")
            self.ui.textEdit.clear()
        else:
            print("Cannot submit an empty post box.")

                



# Step 2: Create the controller that orchestrates the switching
class ZestApp(QtWidgets.QMainWindow):
=======
from register import RegisterPage
from additional_information import AdditionalInfoPage
from interest_page import InterestPage
from loginpage import LoginPage
from zest_main import WorkspaceSuite

class ApplicationExecutionEngine(QMainWindow):
>>>>>>> 308f165e689f533fa857ae1d3bb1e4781387a917
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZEST Application")
        self.resize(1100,700)
        self.setStyleSheet(Style_used_to_in_Login)

        self.deck = QStackedWidget()
        self.setCentralWidget(self.deck)

<<<<<<< HEAD
        # 2. Instantiate your custom pages
        self.chat_page = ChatPage()
        self.profile_page = ProfilePage(user_id=1)
=======
        # Primary Router Layer Map Position:
        # Index 0 -> Register Layout View
        # Index 1 -> Additional Info Layout View
        # Index 2 -> Interests Checklist View
        # Index 3 -> Login View Frame
        # Index 4 -> Operational Workplace Dashboard Switcher (ZEST Deck Suite)
>>>>>>> 308f165e689f533fa857ae1d3bb1e4781387a917

        self.deck.addWidget(RegisterPage(self.deck))
        self.deck.addWidget(AdditionalInfoPage(self.deck))
        self.deck.addWidget(InterestPage(self.deck))
        self.deck.addWidget(LoginPage(self.deck))
        self.deck.addWidget(WorkspaceSuite(self.deck))

        self.deck.setCurrentIndex(3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = ApplicationExecutionEngine()
    engine.show()
    sys.exit(app.exec_())