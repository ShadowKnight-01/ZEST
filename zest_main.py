from PyQt5.QtWidgets import (
    QWidget, QStackedWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QListWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Database.db_connect import supabase
from backend.session import SESSION

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

        brand = QLabel("ZEST")
        brand.setFont(QFont('Times New Roman', 16, QFont.Bold))
        brand.setStyleSheet("background: transparent; color: white; margin-bottom: 20px;")
        brand.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(brand)

        # The 4 navigational commands 
        self.btn_nav_profile = QPushButton("Profile")
        self.btn_nav_profile.setStyleSheet("background: transparent; border: transparent;")
        self.btn_nav_zest = QPushButton("ZEST Main")
        self.btn_nav_zest.setStyleSheet("background: transparent; border: transparent;")
        self.btn_nav_explore = QPushButton("Explore")
        self.btn_nav_explore.setStyleSheet("background: transparent; border: transparent;")
        self.btn_nav_messages = QPushButton("Messages")
        self.btn_nav_messages.setStyleSheet("background: transparent; border: transparent;")

        for btn in [self.btn_nav_profile, self.btn_nav_zest, self.btn_nav_explore, self.btn_nav_messages]:
            btn.setStyleSheet("text-align: left; padding: 12px; background: transparent; border-radius: 4px;")
            sidebar_layout.addWidget(btn)

        self.btn_nav_profile.clicked.connect(lambda: self.switch_tab(0))
        self.btn_nav_zest.clicked.connect(lambda: self.switch_tab(1))
        self.btn_nav_explore.clicked.connect(lambda: self.switch_tab(2))
        self.btn_nav_messages.clicked.connect(lambda: self.switch_tab(3))

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        
        self.tab_deck = QStackedWidget()
        
        
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


    # Profile page part

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
        self.txt_editable_username.setToolTip("Type here and click Save button to change your username")
        un_container.addWidget(self.txt_editable_username)
        
        self.lbl_prof_gender = QLabel("Gender: ")
        self.lbl_prof_interests = QLabel("Interests: ")

        btn_save_username = QPushButton("Save New Username")
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
        
        left_panel.addSpacing(100)
        left_panel.addStretch()


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
        self.lbl_prof_gender.setText(f"Gender: {SESSION['gender']}")
        self.lbl_prof_interests.setText(f"Interested Tags:\n{SESSION['interest']}")
        
        # Load local user's historical active contacts rolling frame
        try:
            self.lst_profile_friends.clear()
            result = supabase.table("messages").select("sender_id, receiver_id").or_(f"sender_id.eq.{SESSION['user_id']},receiver_id.eq.{SESSION['user_id']}").execute()
            
            interacted_uuids = set()
            for msg in result.data:
                if msg["sender_id"] != SESSION["user_id"]: interacted_uuids.add(msg["sender_id"])
                if msg["receiver_id"] != SESSION["user_id"]: interacted_uuids.add(msg["receiver_id"])

            if interacted_uuids:
                users_res = supabase.table("users").select("username").in_("user_id", list(interacted_uuids)).execute()
                for profile in users_res.data:
                    self.lst_profile_friends.addItem(profile["username"])
        except Exception as err:
            print(f"Database Error: {err}")

    def update_username_inline(self):
        new_un = self.txt_editable_username.text().strip()
        if not new_un or new_un == SESSION["username"]: return

        try:
            # check if username is a duplicate
            check = supabase.table("users").select("username").eq("username", new_un).execute()
            if check.data:
                QMessageBox.warning(self, "Constraint Error", "Username already exists.")
                return

            supabase.table("users").update({"username": new_un}).eq("user_id", SESSION["user_id"]).execute()
            SESSION["username"] = new_un
            QMessageBox.information(self, "System Notification", "Username have been updated successfully.")
        except Exception as err:
            QMessageBox.critical(self, "Fault Drop", str(err))

    def route_to_external_interests_editor(self):
       
        from interest_page import InterestPage
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


    # ZEST Main Page

    def build_zest_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        header = QLabel("ZEST Global Activity Feed")
        header.setFont(QFont('Segoe UI', 14, QFont.Bold))
        layout.addWidget(header)

        
        post_box = QHBoxLayout()
        self.txt_zest_feed_input = QLineEdit()
        self.txt_zest_feed_input.setPlaceholderText("Broadcast something onto the ZEST timeline...")
        btn_submit_post = QPushButton("Create Post")
        btn_submit_post.clicked.connect(self.submit_zest_global_feed_post)
        
        post_box.addWidget(self.txt_zest_feed_input)
        post_box.addWidget(btn_submit_post)
        layout.addLayout(post_box)

  
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
            result = supabase.table("posts").select("*").order("created_at", desc=True).execute()
            for post in result.data:
                display_item = f"{post['username']}\n↳ {post['content']}\n"
                self.lst_zest_feed_scroller.addItem(display_item)
        except Exception as err:
            print(f"Feed rendering failure drop: {err}")


    # Search section

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
            result = supabase.table("users").select("username, interest").neq("user_id", SESSION["user_id"]).execute()
            for u in result.data:
                self.lst_explore_directory.addItem(f"User: {u['username']}  | Focus Traits: {u.get('interest', 'None')}")
        except Exception as err:
            QMessageBox.critical(self, "Network scan crash", str(err))


    # Message Page

    def build_messages_tab(self):
        page = QWidget()
        layout = QHBoxLayout(page)

       
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

     
        right_pane = QVBoxLayout()
        self.lbl_chat_header_active_target = QLabel("Select a user to start chatting")
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

        # Add this inside build_messages_tab()
        btn_delete_msg = QPushButton("Delete Selected")
        btn_delete_msg.clicked.connect(self.delete_selected_message)
        message_input_box.addWidget(btn_delete_msg)

        right_pane.addLayout(message_input_box)

        layout.addLayout(left_pane, 4)
        layout.addLayout(right_pane, 6)
        self.tab_deck.addWidget(page)

    def load_conversations_list(self):
        try:
            self.lst_msg_historical_chats.clear()
            result = supabase.table("messages").select("sender_id, receiver_id").or_(f"sender_id.eq.{SESSION['user_id']},receiver_id.eq.{SESSION['user_id']}").execute()
            
            interacted_uuids = set()
            for msg in result.data:
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
            result = supabase.table("users").select("username, user_id").ilike("username", f"%{term}%").neq("user_id", SESSION["user_id"]).execute()
            self.lst_msg_historical_chats.clear()
            for u in result.data:
                self.lst_msg_historical_chats.addItem(f"{u['username']} ({u['user_id']})")
        except Exception as err:
            QMessageBox.critical(self, "Search Fault", str(err))

    def handle_historical_chat_selection_click(self, item):
        text = item.text()
       
        username = text.split(" (")[0]
        receiver_uuid = text.split(" (")[1].replace(")", "")
        
        self.active_chat_receiver_id = receiver_uuid
        self.lbl_chat_header_active_target.setText(f"Chat Session Running -> @{username}")
        self.stream_live_chat_history()

    def stream_live_chat_history(self):
        if not self.active_chat_receiver_id: return
        try:
            self.lst_chat_message_history_stream.clear()
            
          
            result = supabase.table("messages").select("sender_id, message").or_(
                f"and(sender_id.eq.{SESSION['user_id']},receiver_id.eq.{self.active_chat_receiver_id}),"
                f"and(sender_id.eq.{self.active_chat_receiver_id},receiver_id.eq.{SESSION['user_id']})"
            ).order("created_at", desc=False).execute()

            for m in result.data:
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

    def delete_selected_message(self):
        # 1. Grab the currently clicked message from the chat list
        selected_items = self.lst_chat_message_history_stream.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Notice", "Please select a message to delete first.")
            return

        selected_item = selected_items[0]
        full_text = selected_item.text()

        # 2. Security check: Only allow deleting messages sent by the user
        if not full_text.startswith("You: "):
            QMessageBox.warning(self, "Denied", "You can only delete your own messages.")
            return

        # 3. Strip the "You: " prefix to get the exact raw message text
        raw_message = full_text.replace("You: ", "", 1)

        try:
            # 4. Tell Supabase to delete the matching message row
            supabase.table("messages").delete().match({
                "sender_id": SESSION["user_id"],
                "receiver_id": self.active_chat_receiver_id,
                "message": raw_message
            }).execute()

            # 5. Remove it instantly from the UI list so it disappears visually
            row = self.lst_chat_message_history_stream.row(selected_item)
            self.lst_chat_message_history_stream.takeItem(row)

        except Exception as err:
            QMessageBox.critical(self, "Error", f"Failed to delete: {str(err)}")        