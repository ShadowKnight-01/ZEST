import sys
from PyQt5 import QtWidgets

# Import your generated UI classes
from zest_main import Ui_MainWindow
from chat_page import Ui_ChatForm
from pfpinterface import Ui_ProfileForm
#from ** import **    #for the explore page


# Step 1: Wrap your secondary forms into proper standalone custom Widgets
class ChatPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ChatForm()
        self.ui.setupUi(self)


class ProfilePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProfileForm()
        self.ui.setupUi(self)

class Explore(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
       # self.ui = Ui_searchForm()
        self.ui.setupUi(self)


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
        self.profile_page = ProfilePage()

        # 3. Take your existing static UI elements from the global feed layout
        # We wrap them into a temporary container to act as your "Explore" page
        self.main_page = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QHBoxLayout(self.main_page)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Pull out your existing layout elements from the primary interface
        self.ui.horizontalLayout.removeWidget(self.ui.feed_container)
        self.ui.horizontalLayout.removeWidget(self.ui.right_panel)
        
        # Drop them directly into our container widget layout
        self.main_layout.addWidget(self.ui.feed_container)
        self.main_layout.addWidget(self.ui.right_panel)

        # 4. Rig the pages onto the Stacked Widget deck
        # Index 0 = Explore, Index 1 = Message, Index 2 = Profile
        self.stacked_widget.addWidget(self.main_page)
        #self.stacked_widget.addWidget(self.explore_page)
        self.stacked_widget.addWidget(self.chat_page)
        self.stacked_widget.addWidget(self.profile_page)

        # 5. Insert the stacked widget container next to your sidebar
        self.ui.horizontalLayout.addWidget(self.stacked_widget)

        # 6. Wire up navigation logic to the sidebar push buttons
        self.ui.btn_mainpage.clicked.connect(lambda: self.switch_page(0))    
        self.ui.btn_explore.clicked.connect(lambda: self.switch_page(1))
        self.ui.btn_message.clicked.connect(lambda: self.switch_page(2))
        self.ui.btn_profile.clicked.connect(lambda: self.switch_page(3))

        # Start with the Explore Feed active
        self.switch_page(0)

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ZestApp()
    window.show()
    sys.exit(app.exec_())