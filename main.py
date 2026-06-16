import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

# Import your beautiful custom standalone UI views
from loginpage import LoginPage
from register import RegisterPage
from additional_information import AdditionalInfoPage
from interest_page import InterestPage

# Import system layout shells
from zest_main import Ui_MainWindow
from chat_page import Ui_ChatForm
from pfpinterface import Ui_ProfileForm

class ZestAppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZEST Application Suite")
        self.resize(1200, 800)

        # Master navigation deck
        self.deck = QStackedWidget()
        self.setCentralWidget(self.deck)

        # 1. Instantiate the explicit page components
        self.login_page = LoginPage()
        self.register_page = RegisterPage()
        self.additional_page = AdditionalInfoPage()
        self.interest_page = InterestPage()
        
        # 2. Build Dashboard Container Frame (Workspace Index 4)
        self.dashboard_window = QtWidgets.QWidget()
        self.ui_dashboard = Ui_MainWindow()
        self.ui_dashboard.setupUi(self.dashboard_window)

        # 3. Mount pages strictly into sequential deck indexes matching test.py
        # Index 0 -> Login Screen Layout
        # Index 1 -> Register Screen Layout
        # Index 2 -> Additional Profile Info Collection Frame
        # Index 3 -> Interests Selector Checklist View
        # Index 4 -> Core Dashboard Operations Space
        self.deck.addWidget(self.login_page)       # Index 0
        self.deck.addWidget(self.register_page)    # Index 1
        self.deck.addWidget(self.additional_page)  # Index 2
        self.deck.addWidget(self.interest_page)    # Index 3
        self.deck.addWidget(self.dashboard_window)  # Index 4

        # Wire internal workspace controls for chat/profile tabs
        self.setup_internal_dashboard_tabs()

        # Monitor layout alterations to sync backend states automatically
        self.deck.currentChanged.connect(self.sync_active_view_state)

        # Launch the application at the Login frame entry node
        self.deck.setCurrentIndex(0)

    def setup_internal_dashboard_tabs(self):
        """Constructs and pins functional view tabs within Dashboard Workspace Workspace Index 4"""
        self.inner_stack = QtWidgets.QStackedWidget()

        # Initialize Chat UI
        self.chat_view = QtWidgets.QWidget()
        self.ui_chat = Ui_ChatForm()
        self.ui_chat.setupUi(self.chat_view)

        # Initialize Profile UI
        self.profile_view = QtWidgets.QWidget()
        self.ui_profile = Ui_ProfileForm()
        self.ui_profile.setupUi(self.profile_view)

        # Add tabs to interior dashboard switcher
        self.inner_stack.addWidget(self.chat_view)     # Sub-Index 0
        self.inner_stack.addWidget(self.profile_view)  # Sub-Index 1

        # Replace UI workspace layout placeholder with live views safely
        if self.ui_dashboard.horizontalLayout.indexOf(self.ui_dashboard.feed_container) != -1:
            self.ui_dashboard.horizontalLayout.removeWidget(self.ui_dashboard.feed_container)
        
        self.ui_dashboard.horizontalLayout.addWidget(self.inner_stack)

        # Map sidebar layout pushbuttons to adjust internal workspace indexes
        self.ui_dashboard.btn_message.clicked.connect(lambda: self.inner_stack.setCurrentIndex(0))
        self.ui_dashboard.btn_profile.clicked.connect(lambda: self.inner_stack.setCurrentIndex(1))

    def sync_active_view_state(self, index):
        """Pre-loads user content parameters whenever view changes take place"""
        from backend.session import SESSION
        current_uid = SESSION.get("user_id")

        if index == 4 and current_uid:
            # Safely refresh active contacts panel when arriving at dashboard
            if hasattr(self.ui_chat, "list_friends"):
                from backend.chat_logic import load_chat_users
                load_chat_users(self.ui_chat, current_uid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ZestAppMainWindow()
    main_window.show()
    sys.exit(app.exec_())