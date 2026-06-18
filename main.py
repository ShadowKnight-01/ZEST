import sys
from PyQt5 import QtWidgets

# Import your generated UI classes
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
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 1. Create a QStackedWidget instance
        self.stacked_widget = QtWidgets.QStackedWidget(self.ui.centralwidget)
        self.stacked_widget.setObjectName("stacked_widget")

        # 2. Instantiate your custom pages
        self.chat_page = ChatPage()
        self.profile_page = ProfilePage(user_id=1)

        # 3. Take your existing static UI elements from the global feed layout
        # We wrap them into a temporary container to act as your "Explore" page
        self.explore_page = QtWidgets.QWidget()
        self.explore_layout = QtWidgets.QHBoxLayout(self.explore_page)
        self.explore_layout.setContentsMargins(0, 0, 0, 0)
        
        # Pull out your existing layout elements from the primary interface
        self.ui.horizontalLayout.removeWidget(self.ui.feed_container)
        self.ui.horizontalLayout.removeWidget(self.ui.right_panel)
        
        # Drop them directly into our container widget layout
        self.explore_layout.addWidget(self.ui.feed_container)
        self.explore_layout.addWidget(self.ui.right_panel)

        # 4. Rig the pages onto the Stacked Widget deck
        # Index 0 = Explore, Index 1 = Message, Index 2 = Profile
        self.stacked_widget.addWidget(self.explore_page)
        self.stacked_widget.addWidget(self.chat_page)
        self.stacked_widget.addWidget(self.profile_page)

        # 5. Insert the stacked widget container next to your sidebar
        self.ui.horizontalLayout.addWidget(self.stacked_widget)

        # 6. Wire up navigation logic to the sidebar push buttons
        self.ui.btn_explore.clicked.connect(lambda: self.switch_page(0))
        self.ui.btn_message.clicked.connect(lambda: self.switch_page(1))
        self.ui.btn_profile.clicked.connect(lambda: self.switch_page(2))

        # Start with the Explore Feed active
        self.switch_page(0)

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ZestApp()
    window.show()
    sys.exit(app.exec_())