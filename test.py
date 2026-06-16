import sys
import re
import uuid
import hashlib
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, 
    QMessageBox, QListWidget, QFrame, QCheckBox, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from supabase import create_client, Client

# ==========================================
# 0. DATABASE CONNECTION INITIALIZATION
# ==========================================
SUPABASE_URL = "https://obvhcmbnkfhvvkntiaqu.supabase.co"
SUPABASE_KEY = "sb_publishable_3jh4v5IBT2qJyKiQZhsxIA_8Z9iJNza"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Global Auth State Tracker
SESSION = {
    "user_id": None,
    "username": None,
    "full_name": None,
    "gender": None,
    "interest": None
}

# Dark Theme Stylesheet Palette matching your UI screenshots
DARK_STYLE = """
    QWidget {
        background-color: #121214;
        color: #E1E1E6;
        font-family: 'Segoe UI', Arial;
        font-size: 13px;
    }
    QLineEdit, QTextEdit, QComboBox, QListWidget {
        background-color: #202024;
        border: 1px solid #323238;
        border-radius: 6px;
        padding: 8px;
        color: #FFFFFF;
    }
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #00B37E;
    }
    QPushButton {
        background-color: #00B37E;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 10px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #00875F;
    }
    QPushButton:disabled {
        background-color: #29292E;
        color: #7C7C8A;
    }
    QFrame#Sidebar {
        background-color: #202024;
        border-right: 1px solid #323238;
    }
    QCheckBox {
        spacing: 8px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        background-color: #202024;
        border: 1px solid #323238;
        border-radius: 4px;
    }
    QCheckBox::indicator:checked {
        background-color: #00B37E;
        border: 1px solid #00B37E;
    }
"""

# ==========================================
# 1. AUTHENTICATION PAGES & PROFILE WIZARDS
# ==========================================
class RegisterPage(QWidget):
    def __init__(self, stack_manager):
        super().__init__()
        self.stack = stack_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("Create Account\nRegister to get started")
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.txt_fullname = QLineEdit()
        self.txt_fullname.setPlaceholderText("Full Name")
        self.txt_fullname.setFixedWidth(320)
        
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Username")
        self.txt_username.setFixedWidth(320)

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("Email (e.g. name@student.edu.my)")
        self.txt_email.setFixedWidth(320)

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Password")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setFixedWidth(320)

        self.txt_confirm_pass = QLineEdit()
        self.txt_confirm_pass.setPlaceholderText("Confirm Password")
        self.txt_confirm_pass.setEchoMode(QLineEdit.Password)
        self.txt_confirm_pass.setFixedWidth(320)

        btn_register = QPushButton("Register")
        btn_register.setFixedWidth(320)
        btn_register.clicked.connect(self.handle_registration)

        btn_goto_login = QPushButton("Already have an account? Login")
        btn_goto_login.setFixedWidth(320)
        btn_goto_login.setStyleSheet("background: transparent; color: #00B37E;")
        btn_goto_login.clicked.connect(lambda: self.stack.setCurrentIndex(3)) # Jump straight to Login

        layout.addWidget(self.txt_fullname)
        layout.addWidget(self.txt_username)
        layout.addWidget(self.txt_email)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.txt_confirm_pass)
        layout.addWidget(btn_register)
        layout.addWidget(btn_goto_login)
        self.setLayout(layout)

    def handle_registration(self):
        fn = self.txt_fullname.text().strip()
        un = self.txt_username.text().strip()
        em = self.txt_email.text().strip()
        pw = self.txt_password.text()
        cp = self.txt_confirm_pass.text()

        if not fn or not un or not em or not pw:
            QMessageBox.warning(self, "Error", "All entry fields are required.")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.edu\.my$", em):
            QMessageBox.warning(self, "Error", "Invalid education domain configuration. Redirecting registration check.")
            return
        if pw != cp:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        try:
            # Check for duplicate accounts gracefully
            dup_check = supabase.table("users").select("email, username").or_(f"email.eq.{em},username.eq.{un}").execute()
            if dup_check.data:
                QMessageBox.information(self, "Existing Profile", "This identity profile is already registered. Moving to Sign In screen.")
                self.stack.setCurrentIndex(3)
                return

            # Set local runtime memory token
            SESSION["user_id"] = str(uuid.uuid4())
            SESSION["full_name"] = fn
            SESSION["username"] = un

            # Push baseline profile to DB
            hashed_pw = hashlib.blake2b(pw.encode()).hexdigest()
            supabase.table("users").insert({
                "user_id": SESSION["user_id"],
                "full_name": fn,
                "username": un,
                "email": em,
                "password": hashed_pw
            }).execute()

            # Advance onwards to step 2
            self.stack.setCurrentIndex(1)

        except Exception as err:
            QMessageBox.critical(self, "Database System Fault", f"Transmission dropped: {str(err)}")


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
        self.cmb_gender.setFixedWidth(320)

        self.txt_dob = QLineEdit()
        self.txt_dob.setPlaceholderText("Date of Birth (YYYY-MM-DD)")
        self.txt_dob.setFixedWidth(320)

        self.txt_course = QLineEdit()
        self.txt_course.setPlaceholderText("Course (e.g., Computer Science)")
        self.txt_course.setFixedWidth(320)

        self.cmb_education = QComboBox()
        self.cmb_education.addItems(["Diploma", "Foundation/Matriculation", "Bachelor's Degree", "Master's Degree", "PhD"])
        self.cmb_education.setFixedWidth(320)

        self.txt_state = QLineEdit()
        self.txt_state.setPlaceholderText("State (e.g., Selangor)")
        self.txt_state.setFixedWidth(320)

        self.txt_city = QLineEdit()
        self.txt_city.setPlaceholderText("City (e.g., Cyberjaya)")
        self.txt_city.setFixedWidth(320)

        btn_next = QPushButton("Continue")
        btn_next.setFixedWidth(320)
        btn_next.clicked.connect(self.save_data)

        scroll_layout.addWidget(QLabel("Select Gender:"))
        scroll_layout.addWidget(self.cmb_gender)
        scroll_layout.addWidget(QLabel("Date of Birth:"))
        scroll_layout.addWidget(self.txt_dob)
        scroll_layout.addWidget(QLabel("Academic Course Portfolio:"))
        scroll_layout.addWidget(self.txt_course)
        scroll_layout.addWidget(QLabel("Current Education Level:"))
        scroll_layout.addWidget(self.cmb_education)
        scroll_layout.addWidget(QLabel("State Location Hub:"))
        scroll_layout.addWidget(self.txt_state)
        scroll_layout.addWidget(QLabel("City Region Assignment:"))
        scroll_layout.addWidget(self.txt_city)

        scroll_layout.addWidget(btn_next)
        scroll.setWidget(scroll_content)
        main_box = QVBoxLayout(self)
        main_box.addWidget(scroll)
        self.setLayout(main_box)

    def save_data(self):
        dob_str = self.txt_dob.text().strip()
        gender = self.cmb_gender.currentText()
        
        try:
            birth_date = datetime.strptime(dob_str, "%Y-%m-%d")
            age = datetime.now().year - birth_date.year
        except ValueError:
            QMessageBox.warning(self, "Error", "Please format date strictly as YYYY-MM-DD.")
            return

        try:
            supabase.table("users").update({
                "gender": gender,
                "birthday": dob_str,
                "age": age
            }).eq("user_id", SESSION["user_id"]).execute()

            SESSION["gender"] = gender
            self.stack.setCurrentIndex(2) # Advance to Interests
        except Exception as err:
            QMessageBox.critical(self, "Error", f"Failed updating traits: {str(err)}")


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
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
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

        btn_save = QPushButton("Save & Finish Profile Configuration")
        btn_save.setFixedWidth(320)
        btn_save.clicked.connect(self.commit_interests)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def commit_interests(self):
        selected = [b.text() for b in self.boxes if b.isChecked()]
        if not selected:
            QMessageBox.warning(self, "Validation Error", "Select at least 1 focus tag.")
            return

        interests_csv = ", ".join(selected)
        try:
            supabase.table("users").update({"interest": interests_csv}).eq("user_id", SESSION["user_id"]).execute()
            SESSION["interest"] = interests_csv
            
            QMessageBox.information(self, "Success", "Profile data configured successfully.")
            
            if self.return_to_profile:
                # Routed via the Profile Edit View sub-layer
                self.stack.setCurrentIndex(4) # Bounce to Core Window Stack Frame
                self.stack.widget(4).switch_tab(0) # Route inside main stack directly to view 0 (Profile Tab)
            else:
                self.stack.setCurrentIndex(3) # Route to natural Authentication Log In sequence
        except Exception as err:
            QMessageBox.critical(self, "Error", str(err))


class LoginPage(QWidget):
    def __init__(self, stack_manager):
        super().__init__()
        self.stack = stack_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("Sign In")
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        layout.addWidget(title)

        self.txt_login = QLineEdit()
        self.txt_login.setPlaceholderText("Username or Email")
        self.txt_login.setFixedWidth(320)

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Password")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setFixedWidth(320)

        btn_login = QPushButton("Log In")
        btn_login.setFixedWidth(320)
        btn_login.clicked.connect(self.auth_user)

        layout.addWidget(self.txt_login)
        layout.addWidget(self.txt_password)
        layout.addWidget(btn_login)
        self.setLayout(layout)

    def auth_user(self):
        ident = self.txt_login.text().strip()
        pw = self.txt_password.text()

        try:
            res = supabase.table("users").select("*").or_(f"email.eq.{ident},username.eq.{ident}").execute()
            if not res.data:
                QMessageBox.warning(self, "Auth Error", "No identity registry profile mapped to those configurations.")
                return

            db_user = res.data[0]
            hashed_input = hashlib.blake2b(pw.encode()).hexdigest()

            if db_user["password"] != hashed_input:
                QMessageBox.warning(self, "Auth Error", "Invalid passcode security sequence verification.")
                return

            # Commit globally mapped Session memory pointers
            SESSION["user_id"] = db_user["user_id"]
            SESSION["username"] = db_user["username"]
            SESSION["full_name"] = db_user["full_name"]
            SESSION["gender"] = db_user.get("gender", "Unspecified")
            SESSION["interest"] = db_user.get("interest", "None Selected")

            # Route execution out directly to Workspace Suite Container
            self.stack.widget(4).sync_dynamic_profile_view()
            self.stack.widget(4).refresh_forum_feed()
            self.stack.widget(4).load_conversations_list()
            self.stack.setCurrentIndex(4)

        except Exception as err:
            QMessageBox.critical(self, "Runtime Stack Drop", str(err))

# ==========================================
# 2. RUNTIME WORKSPACE STACK DECK LAYOUT (ZEST)
# ==========================================
class WorkspaceSuite(QWidget):
    def __init__(self, stack_manager):
        super().__init__()
        self.parent_stack = stack_manager
        self.active_chat_receiver_id = None
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Column: System Navigation Sidebar (Sidebar Layout Layer)
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)

        brand = QLabel("ZEST SUITE")
        brand.setFont(QFont('Segoe UI', 16, QFont.Bold))
        brand.setStyleSheet("color: #00B37E; margin-bottom: 20px;")
        brand.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(brand)

        # The 4 explicit navigational commands matching your visual layout blueprints
        self.btn_nav_profile = QPushButton("Profile")
        self.btn_nav_zest = QPushButton("ZEST Main")
        self.btn_nav_explore = QPushButton("Explore")
        self.btn_nav_messages = QPushButton("Messages")

        for b in [self.btn_nav_profile, self.btn_nav_zest, self.btn_nav_explore, self.btn_nav_messages]:
            b.setStyleSheet("text-align: left; padding: 12px; background: transparent; border-radius: 4px;")
            sidebar_layout.addWidget(b)

        self.btn_nav_profile.clicked.connect(lambda: self.switch_tab(0))
        self.btn_nav_zest.clicked.connect(lambda: self.switch_tab(1))
        self.btn_nav_explore.clicked.connect(lambda: self.switch_tab(2))
        self.btn_nav_messages.clicked.connect(lambda: self.switch_tab(3))

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # Right Column: Main View Deck Switcher
        self.tab_deck = QStackedWidget()
        
        # Build views onto the main view deck
        self.build_profile_tab()
        self.build_zest_tab()
        self.build_explore_tab()
        self.build_messages_tab()

        main_layout.addWidget(self.tab_deck)
        self.setLayout(main_layout)

    def switch_tab(self, index):
        self.tab_deck.setCurrentIndex(index)
        if index == 0: self.sync_dynamic_profile_view()
        if index == 1: self.refresh_forum_feed()
        if index == 3: self.load_conversations_list()

    # ------------------------------------------
    # VIEW CARD 0: Personal Profile Dashboard Workspace
    # ------------------------------------------
    def build_profile_tab(self):
        page = QWidget()
        layout = QHBoxLayout(page)

        # Left Sub-Column Layout Panel
        left_panel = QVBoxLayout()
        left_panel.setSpacing(10)

        self.lbl_prof_fullname = QLabel("Full Name")
        self.lbl_prof_fullname.setFont(QFont('Segoe UI', 16, QFont.Bold))
        
        # Inline Username Field Layer
        un_container = QHBoxLayout()
        un_container.addWidget(QLabel("@"))
        self.txt_editable_username = QLineEdit()
        self.txt_editable_username.setToolTip("Type here and click Save to change your username")
        un_container.addWidget(self.txt_editable_username)
        
        self.lbl_prof_gender = QLabel("Gender: ")
        self.lbl_prof_interests = QLabel("Interests: ")

        btn_save_username = QPushButton("Save Username Change")
        btn_save_username.clicked.connect(self.update_username_inline)

        btn_edit_interests = QPushButton("Edit Interests Tags")
        btn_edit_interests.clicked.connect(self.route_to_external_interests_editor)

        # Personal Forum Feed Sub-List
        left_panel.addWidget(self.lbl_prof_fullname)
        left_panel.addLayout(un_container)
        left_panel.addWidget(btn_save_username)
        left_panel.addWidget(self.lbl_prof_gender)
        left_panel.addWidget(self.lbl_prof_interests)
        left_panel.addWidget(btn_edit_interests)
        
        # Inline Personal Forum Box Placement Configuration
        left_panel.addWidget(QLabel("\nCreate Micro-Forum Post:"))
        self.txt_profile_forum_input = QTextEdit()
        self.txt_profile_forum_input.setPlaceholderText("Write updates here...")
        self.txt_profile_forum_input.setFixedHeight(80)
        btn_post_profile = QPushButton("Post to Forum")
        btn_post_profile.clicked.connect(self.submit_profile_forum_post)
        
        left_panel.addWidget(self.txt_profile_forum_input)
        left_panel.addWidget(btn_post_profile)
        left_panel.addStretch()

        # Right Sub-Column Layout Panel: Active Contacts Chat Roll History Widget
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Recent Conversational Interactions:"))
        self.lst_profile_friends = QListWidget()
        right_panel.addWidget(self.lst_profile_friends)

        layout.addLayout(left_panel, 6)
        layout.addLayout(right_panel, 4)
        self.tab_deck.addWidget(page)

    def sync_dynamic_profile_view(self):
        self.lbl_prof_fullname.setText(SESSION["full_name"])
        self.txt_editable_username.setText(SESSION["username"])
        self.lbl_prof_gender.setText(f"Gender Parameters: {SESSION['gender']}")
        self.lbl_prof_interests.setText(f"Subscribed Focus Tags:\n{SESSION['interest']}")
        
        # Load local user's historical active contacts rolling frame
        try:
            self.lst_profile_friends.clear()
            res = supabase.table("messages").select("sender_id, receiver_id").or_(f"sender_id.eq.{SESSION['user_id']},receiver_id.eq.{SESSION['user_id']}").execute()
            
            interacted_uuids = set()
            for msg in res.data:
                if msg["sender_id"] != SESSION["user_id"]: interacted_uuids.add(msg["sender_id"])
                if msg["receiver_id"] != SESSION["user_id"]: interacted_uuids.add(msg["receiver_id"])

            if interacted_uuids:
                users_res = supabase.table("users").select("username").in_("user_id", list(interacted_uuids)).execute()
                for profile in users_res.data:
                    self.lst_profile_friends.addItem(profile["username"])
        except Exception as err:
            print(f"Silenced background contact parsing drop: {err}")

    def update_username_inline(self):
        new_un = self.txt_editable_username.text().strip()
        if not new_un or new_un == SESSION["username"]: return

        try:
            # Check duplicate username availability constraints
            check = supabase.table("users").select("username").eq("username", new_un).execute()
            if check.data:
                QMessageBox.warning(self, "Constraint Error", "Username token already claimed across network profiles.")
                return

            supabase.table("users").update({"username": new_un}).eq("user_id", SESSION["user_id"]).execute()
            SESSION["username"] = new_un
            QMessageBox.information(self, "System Notification", "Username trace updated cleanly across core layers.")
        except Exception as err:
            QMessageBox.critical(self, "Fault Drop", str(err))

    def route_to_external_interests_editor(self):
        # Hot-swap view index 2 to return execution cleanly back onto Profile layout targets
        self.parent_stack.removeWidget(self.parent_stack.widget(2))
        profile_interest_context_bridge = InterestPage(self.parent_stack, return_to_profile=True)
        self.parent_stack.insertWidget(2, profile_interest_context_bridge)
        self.parent_stack.setCurrentIndex(2)

    def submit_profile_forum_post(self):
        txt = self.txt_profile_forum_input.toPlainText().strip()
        if not txt: return
        try:
            supabase.table("posts").insert({
                "user_id": SESSION["user_id"],
                "username": SESSION["username"],
                "content": txt
            }).execute()
            self.txt_profile_forum_input.clear()
            QMessageBox.information(self, "Success", "Forum post published.")
        except Exception as err:
            QMessageBox.critical(self, "Error", str(err))

    # ------------------------------------------
    # VIEW CARD 1: ZEST Main Feed Core Component Frame
    # ------------------------------------------
    def build_zest_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        header = QLabel("ZEST Global Activity Feed")
        header.setFont(QFont('Segoe UI', 14, QFont.Bold))
        layout.addWidget(header)

        # Micro-Form Entry Component Container
        post_box = QHBoxLayout()
        self.txt_zest_feed_input = QLineEdit()
        self.txt_zest_feed_input.setPlaceholderText("Broadcast something onto the ZEST timeline...")
        btn_submit_post = QPushButton("Create Post")
        btn_submit_post.clicked.connect(self.submit_zest_global_feed_post)
        
        post_box.addWidget(self.txt_zest_feed_input)
        post_box.addWidget(btn_submit_post)
        layout.addLayout(post_box)

        # Public Global Live Feed Container Widget Layer
        self.lst_zest_feed_scroller = QListWidget()
        layout.addWidget(self.lst_zest_feed_scroller)
        self.tab_deck.addWidget(page)

    def submit_zest_global_feed_post(self):
        txt = self.txt_zest_feed_input.text().strip()
        if not txt: return
        try:
            supabase.table("posts").insert({
                "user_id": SESSION["user_id"],
                "username": SESSION["username"],
                "content": txt
            }).execute()
            self.txt_zest_feed_input.clear()
            self.refresh_forum_feed()
        except Exception as err:
            QMessageBox.critical(self, "Error", str(err))

    def refresh_forum_feed(self):
        try:
            self.lst_zest_feed_scroller.clear()
            res = supabase.table("posts").select("*").order("created_at", desc=True).execute()
            for post in res.data:
                display_item = f"{post['username']}\n↳ {post['content']}\n"
                self.lst_zest_feed_scroller.addItem(display_item)
        except Exception as err:
            print(f"Feed rendering failure drop: {err}")

    # ------------------------------------------
    # VIEW CARD 2: Explore Discovery Module Layer
    # ------------------------------------------
    def build_explore_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Explore Active Platform Network Users")
        title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        layout.addWidget(title)

        btn_pull_directory = QPushButton("Scan Network Active Nodes")
        btn_pull_directory.clicked.connect(self.scan_network_directory)
        layout.addWidget(btn_pull_directory)

        self.lst_explore_directory = QListWidget()
        layout.addWidget(self.lst_explore_directory)
        self.tab_deck.addWidget(page)

    def scan_network_directory(self):
        try:
            self.lst_explore_directory.clear()
            res = supabase.table("users").select("username, interest").neq("user_id", SESSION["user_id"]).execute()
            for u in res.data:
                self.lst_explore_directory.addItem(f"User: {u['username']}  | Focus Traits: {u.get('interest', 'None')}")
        except Exception as err:
            QMessageBox.critical(self, "Network scan crash", str(err))

    # ------------------------------------------
    # VIEW CARD 3: Direct Messages Messenger Engine Terminal
    # ------------------------------------------
    def build_messages_tab(self):
        page = QWidget()
        layout = QHBoxLayout(page)

        # Left Pane Configuration Panel: Lookups and Search Controllers
        left_pane = QVBoxLayout()
        
        search_box = QHBoxLayout()
        self.txt_msg_user_search = QLineEdit()
        self.txt_msg_user_search.setPlaceholderText("Search profiles...")
        btn_trigger_msg_search = QPushButton("Search")
        btn_trigger_msg_search.clicked.connect(self.execute_chat_user_lookup)
        search_box.addWidget(self.txt_msg_user_search)
        search_box.addWidget(btn_trigger_msg_search)
        left_pane.addLayout(search_box)

        self.lst_msg_historical_chats = QListWidget()
        self.lst_msg_historical_chats.itemClicked.connect(self.handle_historical_chat_selection_click)
        left_pane.addWidget(self.lst_msg_historical_chats)

        # Right Pane Layout Panel: Live Workspace Conversational Box Text Stream
        right_pane = QVBoxLayout()
        self.lbl_chat_header_active_target = QLabel("Target Node: Select a user to start chatting")
        self.lbl_chat_header_active_target.setFont(QFont('Segoe UI', 12, QFont.Bold))
        right_pane.addWidget(self.lbl_chat_header_active_target)

        self.lst_chat_message_history_stream = QListWidget()
        right_pane.addWidget(self.lst_chat_message_history_stream)

        message_input_box = QHBoxLayout()
        self.txt_chat_payload_input = QLineEdit()
        self.txt_chat_payload_input.setPlaceholderText("Type your message here...")
        self.txt_chat_payload_input.returnPressed.connect(self.transmit_direct_message)
        
        btn_send_msg = QPushButton("Send")
        btn_send_msg.clicked.connect(self.transmit_direct_message)
        message_input_box.addWidget(self.txt_chat_payload_input)
        message_input_box.addWidget(btn_send_msg)
        right_pane.addLayout(message_input_box)

        layout.addLayout(left_pane, 4)
        layout.addLayout(right_pane, 6)
        self.tab_deck.addWidget(page)

    def load_conversations_list(self):
        try:
            self.lst_msg_historical_chats.clear()
            res = supabase.table("messages").select("sender_id, receiver_id").or_(f"sender_id.eq.{SESSION['user_id']},receiver_id.eq.{SESSION['user_id']}").execute()
            
            interacted_uuids = set()
            for msg in res.data:
                if msg["sender_id"] != SESSION["user_id"]: interacted_uuids.add(msg["sender_id"])
                if msg["receiver_id"] != SESSION["user_id"]: interacted_uuids.add(msg["receiver_id"])

            if interacted_uuids:
                profiles = supabase.table("users").select("username, user_id").in_("user_id", list(interacted_uuids)).execute()
                for p in profiles.data:
                    self.lst_msg_historical_chats.addItem(f"{p['username']} ({p['user_id']})")
        except Exception as err:
            print(f"History fetch error: {err}")

    def execute_chat_user_lookup(self):
        term = self.txt_msg_user_search.text().strip()
        if not term: return
        try:
            res = supabase.table("users").select("username, user_id").ilike("username", f"%{term}%").neq("user_id", SESSION["user_id"]).execute()
            self.lst_msg_historical_chats.clear()
            for u in res.data:
                self.lst_msg_historical_chats.addItem(f"{u['username']} ({u['user_id']})")
        except Exception as err:
            QMessageBox.critical(self, "Search Fault", str(err))

    def handle_historical_chat_selection_click(self, item):
        text = item.text()
        # Parse tracking token elements out safely via raw string slice
        username = text.split(" (")[0]
        receiver_uuid = text.split(" (")[1].replace(")", "")
        
        self.active_chat_receiver_id = receiver_uuid
        self.lbl_chat_header_active_target.setText(f"Chat Session Running $\rightarrow$ @{username}")
        self.stream_live_chat_history()

    def stream_live_chat_history(self):
        if not self.active_chat_receiver_id: return
        try:
            self.lst_chat_message_history_stream.clear()
            
            # Fetch message history between current user and target user
            res = supabase.table("messages").select("sender_id, message").or_(
                f"and(sender_id.eq.{SESSION['user_id']},receiver_id.eq.{self.active_chat_receiver_id}),"
                f"and(sender_id.eq.{self.active_chat_receiver_id},receiver_id.eq.{SESSION['user_id']})"
            ).order("created_at", desc=False).execute()

            for m in res.data:
                prefix = "You: " if m["sender_id"] == SESSION["user_id"] else "Them: "
                self.lst_chat_message_history_stream.addItem(f"{prefix}{m['message']}")
                
        except Exception as err:
            print(f"Critical stream drop error: {err}")

    def transmit_direct_message(self):
        msg_payload = self.txt_chat_payload_input.text().strip()
        if not msg_payload or not self.active_chat_receiver_id: 
            return
        try:
            supabase.table("messages").insert({
                "sender_id": SESSION["user_id"],
                "receiver_id": self.active_chat_receiver_id,
                "message": msg_payload
            }).execute()
            
            self.txt_chat_payload_input.clear()
            self.stream_live_chat_history()
            self.lst_chat_message_history_stream.scrollToBottom()
        except Exception as err:
            QMessageBox.critical(self, "Transmission Failure",f"Could not send message: {str(err)}")

# ==========================================
# 3. CORE ROUTING DECK ENGINE EXECUTOR
# ==========================================
class ApplicationExecutionEngine(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZEST Application Suite Workspace")
        self.resize(1100, 700)
        self.setStyleSheet(DARK_STYLE)

        self.deck = QStackedWidget()
        self.setCentralWidget(self.deck)

        # Primary Router Layer Map Positions:
        # Index 0 -> Register Layout View
        # Index 1 -> Additional Info Layout View
        # Index 2 -> Interests Checklist View
        # Index 3 -> Login View Frame
        # Index 4 -> Operational Workspace Dashboard Switcher (ZEST Deck Suite)
        self.deck.addWidget(RegisterPage(self.deck))
        self.deck.addWidget(AdditionalInfoPage(self.deck))
        self.deck.addWidget(InterestPage(self.deck, return_to_profile=False))
        self.deck.addWidget(LoginPage(self.deck))
        self.deck.addWidget(WorkspaceSuite(self.deck))

        # Launch default application entry layout node
        self.deck.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = ApplicationExecutionEngine()
    engine.show()
    sys.exit(app.exec_())