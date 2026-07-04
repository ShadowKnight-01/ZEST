from PyQt5.QtWidgets import (
    QWidget, QStackedWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QListWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Database.db_connect import supabase
from backend.session import SESSION

class SideNavigate(QWidget):
    def __init__(self, stack_manager):
        super().__init__()
        self.parent_stack = stack_manager        # save the main page manager
        self.active_chat_receiver_id = None      # store the currently selected chat user
        self.init_ui()                           # make the side interface

    def init_ui(self):
        main_layout = QHBoxLayout(self)          # create the main horizontel layout
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # make the left sidebar
        sidebar = QFrame()                    
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)    # create the sidebar layout
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)

        brand = QLabel("ZEST")       # create the app logo
        brand.setFont(QFont('Times New Roman', 16, QFont.Bold))
        brand.setStyleSheet("background: transparent; color: white; margin-bottom: 20px;")
        brand.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(brand)

        # make the buttons for navigate
        self.btn_nav_profile = QPushButton("Profile")
        self.btn_nav_profile.setStyleSheet("background: transparent; border: transparent;")
        self.btn_nav_zest = QPushButton("ZEST Main")
        self.btn_nav_zest.setStyleSheet("background: transparent; border: transparent;")
        self.btn_nav_explore = QPushButton("Explore")
        self.btn_nav_explore.setStyleSheet("background: transparent; border: transparent;")
        self.btn_nav_messages = QPushButton("Messages")
        self.btn_nav_messages.setStyleSheet("background: transparent; border: transparent;")

        buttons = [             # store all the navigation buttons in a list
            self.btn_nav_profile, 
            self.btn_nav_zest, 
            self.btn_nav_explore, 
            self.btn_nav_messages
        ]

        for btn in buttons:       # add the button to the side bar
            btn.setStyleSheet("text-align: left; padding: 12px; background: transparent; border-radius: 4px;")
            sidebar_layout.addWidget(btn)

        self.btn_nav_profile.clicked.connect(lambda: self.switch_tab(0))        # connect the each button to the side bar
        self.btn_nav_zest.clicked.connect(lambda: self.switch_tab(1))
        self.btn_nav_explore.clicked.connect(lambda: self.switch_tab(2))
        self.btn_nav_messages.clicked.connect(lambda: self.switch_tab(3))

        sidebar_layout.addStretch()                      # push the button to the top
        main_layout.addWidget(sidebar)                   # Add the sidebar to the main layout

        self.tab_deck = QStackedWidget()                 # create the stacked widget for the pages
        
        self.profile_page()                              # create all the pages
        self.main_page()
        self.explore_page()
        self.messages_page()

        main_layout.addWidget(self.tab_deck)                 # add the page container to tha main layout
        self.setLayout(main_layout)                          # set the layout for this widgets

    def switch_tab(self, index):                             # switch to the selected page 
        self.tab_deck.setCurrentIndex(index)
        if index == 0: self.load_profile_data()              # load the latest data for the selected page
        if index == 1: self.load_feed()
        if index == 3: self.load_chat_list()

        buttons = [                                          # store all the navigate btn
            self.btn_nav_profile, 
            self.btn_nav_zest, 
            self.btn_nav_explore, 
            self.btn_nav_messages
        ]

        for btn in buttons:                               # reset all btn style
            btn.setStyleSheet("background: transparent; border: transparent; text-align: left;")

        buttons[index].setStyleSheet("background: transparent; border: transparent; color: #3B82F6; text-align: left; padding: 12px; border-radius: 4px;")    # Highlight the selected btn

        

# Profile page part
    def profile_page(self): # Defines the layout and UI for the user profile tab
        page = QWidget() # Creates a blank widget to act as the profile page container
        layout = QHBoxLayout(page) # Sets up a horizontal layout (left and right sides)

        # Left Sub-Column Layout Panel
        left_panel = QVBoxLayout() # Creates a vertical layout for the left side of the profile
        left_panel.setSpacing(10) # Adds 10 pixels of vertical space between items

        self.lbl_prof_fullname = QLabel("Full Name") # Label to display the user's full name
        self.lbl_prof_fullname.setFont(QFont('Segoe UI', 16, QFont.Bold)) # Makes the name text large and bold
        
        # Inline Username Field Layer
        un_container = QHBoxLayout() # Creates a small horizontal box for the '@' and username input
        un_container.addWidget(QLabel("@")) # Adds the '@' symbol text next to the input
        self.txt_editable_username = QLineEdit() # Creates a text box so the user can type a new username
        self.txt_editable_username.setToolTip("Type here and click Save button to change your username") # Hover text hint
        un_container.addWidget(self.txt_editable_username) # Puts the text box into the small horizontal box
        
        self.lbl_prof_gender = QLabel("Gender: ") # Label to show the user's gender
        self.lbl_prof_interests = QLabel("Interests: ") # Label to show selected interests

        btn_save_username = QPushButton("Save New Username") # Button to trigger the username save action
        btn_save_username.clicked.connect(self.update_username) # Links the button click to the update_username function

        btn_edit_interests = QPushButton("Edit Interests Tags") # Button to navigate to the interests editing page
        btn_edit_interests.clicked.connect(self.edit_interests) # Links the button click to the edit_interests function

        # Personal Forum Feed Sub-List
        left_panel.addWidget(self.lbl_prof_fullname) # Adds the full name label to the left panel
        left_panel.addLayout(un_container) # Adds the username input area to the left panel
        left_panel.addWidget(btn_save_username) # Adds the save button below the username input
        left_panel.addWidget(self.lbl_prof_gender) # Adds the gender label to the panel
        left_panel.addWidget(self.lbl_prof_interests) # Adds the interests label to the panel
        left_panel.addWidget(btn_edit_interests) # Adds the edit interests button to the panel
        
        left_panel.addSpacing(100) # Adds a 100-pixel blank gap to push things down
        left_panel.addStretch() # Fills remaining vertical space so items stay pushed to the top

        right_panel = QVBoxLayout() # Creates a vertical layout for the right side
        right_panel.addWidget(QLabel("Recent Conversational Interactions:")) # Title for the contacts list
        self.lst_profile_friends = QListWidget() # Creates a scrollable list box for recent contacts
        right_panel.addWidget(self.lst_profile_friends) # Adds the scrollable list to the right panel

        layout.addLayout(left_panel, 6) # Adds left panel to main layout, giving it 60% of the screen width
        layout.addLayout(right_panel, 4) # Adds right panel to main layout, giving it 40% of the screen width
        self.tab_deck.addWidget(page) # Adds this whole profile page into your app's main tab system

    def load_profile_data(self): # Function to fetch and display the logged-in user's data
        self.lbl_prof_fullname.setText(SESSION["full_name"]) # Updates label with name from current session dictionary
        self.txt_editable_username.setText(SESSION["username"]) # Pre-fills the text box with the current username
        self.lbl_prof_gender.setText(f"Gender: {SESSION['gender']}") # Updates gender label with session data
        self.lbl_prof_interests.setText(f"Interested Tags:\n{SESSION['interest']}") # Updates interests label with session data
        
        # Load local user's historical active contacts rolling frame
        try:
            self.lst_profile_friends.clear() # Empties the friends list before loading new ones
            result = supabase.table("messages").select("sender_id, receiver_id").or_(f"sender_id.eq.{SESSION['user_id']},receiver_id.eq.{SESSION['user_id']}").execute() # Fetches all messages where user is sender OR receiver
            
            interacted_uuids = set() # Creates an empty set (avoids duplicate IDs) to store contact IDs
            for msg in result.data: # Loops through all the messages we just fetched
                if msg["sender_id"] != SESSION["user_id"]: interacted_uuids.add(msg["sender_id"]) # If user didn't send it, add the sender's ID
                if msg["receiver_id"] != SESSION["user_id"]: interacted_uuids.add(msg["receiver_id"]) # If user didn't receive it, add the receiver's ID

            if interacted_uuids: # If we found people the user interacted with
                users_res = supabase.table("users").select("username").in_("user_id", list(interacted_uuids)).execute() # Fetch the usernames for all those gathered IDs
                for profile in users_res.data: # Loop through the fetched profiles
                    self.lst_profile_friends.addItem(profile["username"]) # Add each username to the visual list widget
        except Exception as err: # Catches any errors during the database process
            print(f"Database Error: {err}") # Prints the error to the console for debugging

    def update_username(self): # Function that runs when the Save Username button is clicked
        new_un = self.txt_editable_username.text().strip() # Grabs the typed text and removes extra spaces
        if not new_un or new_un == SESSION["username"]: return # Stops the function if box is empty or username hasn't changed

        try:
            # check if username is a duplicate
            check = supabase.table("users").select("username").eq("username", new_un).execute() # Asks database if anyone has this username
            if check.data: # If data comes back, it means the name is taken
                QMessageBox.warning(self, "Constraint Error", "Username already exists.") # Shows a warning popup
                return # Stops the function so it doesn't save

            supabase.table("users").update({"username": new_un}).eq("user_id", SESSION["user_id"]).execute() # Tells database to update the name for this specific user ID
            SESSION["username"] = new_un # Updates the local session dictionary with the new name
            QMessageBox.information(self, "System Notification", "Username have been updated successfully.") # Shows a success popup
        except Exception as err:
            QMessageBox.critical(self, "Fault Drop", str(err)) # Shows a critical error popup if the database update fails

    def edit_interests(self): # Function to handle swapping to the interests editing screen
        from interest_page import InterestPage # Imports the separate page layout
        self.parent_stack.removeWidget(self.parent_stack.widget(2)) # Removes whatever was previously in slot 2 of the navigation stack
        profile_interest_context_bridge = InterestPage(self.parent_stack, return_to_profile=True) # Initializes the new interest page
        self.parent_stack.insertWidget(2, profile_interest_context_bridge) # Inserts it into slot 2 of the navigation stack
        self.parent_stack.setCurrentIndex(2) # Switches the screen view to show slot 2

    # ZEST Main Page
    def main_page(self): # Defines the layout and UI for the global feed page
        page = QWidget() # Creates a blank widget container for the main page
        layout = QVBoxLayout(page) # Sets up a top-to-bottom vertical layout

        header = QLabel("ZEST Global Activity Feed") # Title label for the top of the feed
        header.setFont(QFont('Segoe UI', 14, QFont.Bold)) # Sets the font size and boldness for the header
        layout.addWidget(header) # Adds the header to the main layout
        
        post_box = QHBoxLayout() # Creates a horizontal row for the input box and button
        self.txt_zest_feed_input = QLineEdit() # Creates the text box for typing a new post
        self.txt_zest_feed_input.setPlaceholderText("Broadcast something onto the ZEST timeline...") # Grey placeholder text inside the empty box
        btn_submit_post = QPushButton("Create Post") # Button to submit the post
        btn_submit_post.clicked.connect(self.global_feed_post) # Links button click to the global_feed_post function
        
        post_box.addWidget(self.txt_zest_feed_input) # Puts the text box into the horizontal row
        post_box.addWidget(btn_submit_post) # Puts the submit button next to the text box
        layout.addLayout(post_box) # Adds the horizontal row into the main vertical layout

        self.lst_zest_feed_scroller = QListWidget() # Creates the big scrollable list area where all posts will appear
        layout.addWidget(self.lst_zest_feed_scroller) # Adds the scrollable list to the bottom of the main layout
        self.tab_deck.addWidget(page) # Adds this whole main page into your app's main tab system

    def global_feed_post(self): # Function that runs when submitting a new post to the feed
        txt = self.txt_zest_feed_input.text().strip() # Grabs the typed post text and removes extra spacing
        if not txt: return # Stops the function if the user didn't type anything
        try:
            supabase.table("posts").insert({ # Tells database to insert a new row into the 'posts' table
                "user_id": SESSION["user_id"], # Logs who made the post by their ID
                "username": SESSION["username"], # Logs the name of the person posting
                "content": txt # Logs the actual text they typed
            }).execute()
            self.txt_zest_feed_input.clear() # Empties the text box so it's ready for a new post
            self.load_feed() # Refreshes the feed to show the newly created post
        except Exception as err:
            QMessageBox.critical(self, "Error", str(err)) # Shows an error popup if the database insertion fails

    def load_feed(self): # Function to fetch and display all posts in the global feed
        try:
            self.lst_zest_feed_scroller.clear() # Empties the current feed view before loading new data
            result = supabase.table("posts").select("*").order("created_at", desc=True).execute() # Fetches all posts and sorts them by newest first
            for post in result.data: # Loops through every post fetched from the database
                display_item = f"{post['username']}\n↳ {post['content']}\n" # Formats the text string so the username is on top and content is below with an arrow
                self.lst_zest_feed_scroller.addItem(display_item) # Adds the formatted text block into the visual scroll list
        except Exception as err:
            print(f"Feed rendering failure drop: {err}") # Prints the error to the console if feed fails to load

# Search section
    def explore_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Section Title Header
        title = QLabel("Explore Active Platform Network Users")
        title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        layout.addWidget(title)

        btn_pull_directory = QPushButton("Find people with shared interests")
        btn_pull_directory.clicked.connect(self.find_people)
        layout.addWidget(btn_pull_directory)

# List Widget container to display matched results
        self.lst_explore_directory = QListWidget()
        layout.addWidget(self.lst_explore_directory)
        # Register the page view into the main tab layout stack deck
        self.tab_deck.addWidget(page)

    def find_people(self):
        try:
            self.lst_explore_directory.clear()

            # 1. Fetch the logged-in owner's own interests from Supabase
            owner_query = supabase.table("users").select("interest").eq("user_id", SESSION["user_id"]).single().execute()
            owner_interest_str = owner_query.data.get("interest") if owner_query.data else ""
            
            # Clean and convert owner interests to a standardized lowercase set for precise matching
            if owner_interest_str and owner_interest_str.strip().lower() != "none":
                owner_interests = {trait.strip().lower() for trait in owner_interest_str.split(",") if trait.strip()}
            else:
                owner_interests = set()

            # 2. Pull all other network users from Supabase
            result = supabase.table("users").select("username, interest").neq("user_id", SESSION["user_id"]).execute()
            
            matched_users = []

            for u in result.data:
                user_interest_str = u.get("interest")
                if not user_interest_str or user_interest_str.strip().lower() == "none":
                    continue  # Skip users with no traits right away
                
                # Split, clean, and map user's traits while keeping their original casing for UI display
                user_traits_mapped = {trait.strip().lower(): trait.strip() for trait in user_interest_str.split(",") if trait.strip()}
                user_interests_set = set(user_traits_mapped.keys())

                # Find the intersection between the owner and this user
                intersecting_keys = owner_interests.intersection(user_interests_set)

                # 3. Only include the user if they share at least one mutual trait
                if intersecting_keys:
                    # Restore original capitalization for the UI presentation
                    matched_traits = [user_traits_mapped[k] for k in intersecting_keys]
                    
                    matched_users.append({
                        "username": u["username"],
                        "all_traits": user_interest_str,
                        "intersecting": matched_traits,
                        "match_count": len(intersecting_keys)
                    })

            # 4. Sort users from highest match count to lowest
            matched_users.sort(key=lambda x: x["match_count"], reverse=True)

            # 5. Populate sorted results into the QListWidget
            for mu in matched_users:
                intersect_str = ", ".join(mu["intersecting"])
                display_text = f"User: {mu['username']} | Intersecting: {intersect_str} | Focus Traits: {mu['all_traits']}"
                self.lst_explore_directory.addItem(display_text)

            if not matched_users:
                self.lst_explore_directory.addItem("No active users found sharing your interests.")

        except Exception as err:
            QMessageBox.critical(self, "Network scan crash", str(err))
            
# Message Page
    def messages_page(self): # Defines the layout and UI for the private messaging tab
        page = QWidget() # Creates a blank widget container for the messages page
        layout = QHBoxLayout(page) # Sets up a horizontal layout (left list, right chat area)

        left_pane = QVBoxLayout() # Creates a vertical layout for the left side (search and contacts)
        
        search_box = QHBoxLayout() # Creates a horizontal row for the search input and button
        self.txt_msg_user_search = QLineEdit() # Creates a text box to type a user's name to search
        self.txt_msg_user_search.setPlaceholderText("Search profiles...") # Placeholder text inside the empty search box
        btn_trigger_msg_search = QPushButton("Search") # Creates a button to trigger the search
        btn_trigger_msg_search.clicked.connect(self.search_chat_users) # Links the search button to the search_chat_users function
        search_box.addWidget(self.txt_msg_user_search) # Adds the search text box into the horizontal row
        search_box.addWidget(btn_trigger_msg_search) # Adds the search button next to the text box
        left_pane.addLayout(search_box) # Adds the search row to the top of the left vertical panel

        self.lst_msg_historical_chats = QListWidget() # Creates a scrollable list to show recent or searched contacts
        self.lst_msg_historical_chats.itemClicked.connect(self.open_chat) # Links clicking a contact to the open_chat function
        left_pane.addWidget(self.lst_msg_historical_chats) # Adds the contact list below the search bar in the left panel

        right_pane = QVBoxLayout() # Creates a vertical layout for the right side (active chat area)
        self.lbl_chat_header_active_target = QLabel("Select a user to start chatting") # Default header when no chat is open
        self.lbl_chat_header_active_target.setFont(QFont('Segoe UI', 12, QFont.Bold)) # Sets the font style and size for the header
        right_pane.addWidget(self.lbl_chat_header_active_target) # Adds the header to the top of the right panel

        self.lst_chat_message_history_stream = QListWidget() # Creates a large scrollable area to view the actual messages
        right_pane.addWidget(self.lst_chat_message_history_stream) # Adds the message viewing area to the right panel

        message_input_box = QHBoxLayout() # Creates a horizontal row for typing and sending a new message
        self.txt_chat_payload_input = QLineEdit() # Creates the text box where the user types their message
        self.txt_chat_payload_input.setPlaceholderText("Type your message here...") # Grey placeholder text inside the input box
        self.txt_chat_payload_input.returnPressed.connect(self.send_message) # Allows pressing 'Enter' on the keyboard to send the message
        
        btn_send_msg = QPushButton("Send") # Creates a button to manually click to send a message
        btn_send_msg.clicked.connect(self.send_message) # Links the send button to the send_message function
        message_input_box.addWidget(self.txt_chat_payload_input) # Adds the typing box to the horizontal row
        message_input_box.addWidget(btn_send_msg) # Adds the send button next to the typing box

        # Add this inside build_messages_tab()
        btn_delete_msg = QPushButton("Delete Selected") # Creates a button to delete a highlighted message
        btn_delete_msg.clicked.connect(self.delete_selected_message) # Links the delete button to the (assumed) delete function
        message_input_box.addWidget(btn_delete_msg) # Adds the delete button to the bottom row

        right_pane.addLayout(message_input_box) # Adds the entire input row to the bottom of the right panel

        layout.addLayout(left_pane, 4) # Adds left panel to main layout, giving it 40% of the width
        layout.addLayout(right_pane, 6) # Adds right panel to main layout, giving it 60% of the width
        self.tab_deck.addWidget(page) # Adds this entire messaging interface into the app's main tab system

    def load_chat_list(self): # Function to fetch users you have chatted with before
        try:
            self.lst_msg_historical_chats.clear() # Empties the contact list before loading fresh data
            result = supabase.table("messages").select("sender_id, receiver_id").or_(f"sender_id.eq.{SESSION['user_id']},receiver_id.eq.{SESSION['user_id']}").execute() # Asks database for all messages involving the logged-in user
            
            interacted_uuids = set() # Creates a set to store unique user IDs without duplicates
            for msg in result.data: # Loops through the fetched messages
                if msg["sender_id"] != SESSION["user_id"]: interacted_uuids.add(msg["sender_id"]) # Adds the ID of the person who sent a message to the user
                if msg["receiver_id"] != SESSION["user_id"]: interacted_uuids.add(msg["receiver_id"]) # Adds the ID of the person the user sent a message to

            if interacted_uuids: # If we found people the user has talked to
                profiles = supabase.table("users").select("username, user_id").in_("user_id", list(interacted_uuids)).execute() # Fetches the usernames for those specific IDs
                for p in profiles.data: # Loops through the fetched user profiles
                    self.lst_msg_historical_chats.addItem(f"{p['username']} ({p['user_id']})") # Displays the username and ID in the contact list
        except Exception as err:
            print(f"History fetch error: {err}") # Prints any database errors to the console

    def search_chat_users(self): # Function to look up a specific user to message
        term = self.txt_msg_user_search.text().strip() # Grabs the typed search text and removes extra spaces
        if not term: return # Stops the function if the search box is empty
        try:
            result = supabase.table("users").select("username, user_id").ilike("username", f"%{term}%").neq("user_id", SESSION["user_id"]).execute() # Searches database for usernames matching the typed text, excluding the user's own profile
            self.lst_msg_historical_chats.clear() # Clears the current contact list to show search results
            for u in result.data: # Loops through the search results
                self.lst_msg_historical_chats.addItem(f"{u['username']} ({u['user_id']})") # Adds matching users to the list
        except Exception as err:
            QMessageBox.critical(self, "Search Fault", str(err)) # Shows an error popup if the database search fails

    def open_chat(self, item): # Function triggered when you click a person's name in the list
        text = item.text() # Grabs the full text of the clicked item (Username + ID)
       
        username = text.split(" (")[0] # Splits the text at the space and bracket to isolate the username
        receiver_uuid = text.split(" (")[1].replace(")", "") # Isolates the ID and removes the closing bracket
        
        self.active_chat_receiver_id = receiver_uuid # Stores the ID of the person you are now chatting with
        self.lbl_chat_header_active_target.setText(f"Chat Session Running -> @{username}") # Updates the top header to show who you are talking to
        self.load_chat_history() # Calls the function to load the past messages with this specific person

    def load_chat_history(self): # Function to fetch and display the actual conversation
        if not self.active_chat_receiver_id: return # Stops if no chat partner is currently selected
        try:
            self.lst_chat_message_history_stream.clear() # Empties the message viewing area before loading
            
          
            result = supabase.table("messages").select("sender_id, message").or_( # Asks database for specific messages between these two people
                f"and(sender_id.eq.{SESSION['user_id']},receiver_id.eq.{self.active_chat_receiver_id})," # Checks for messages sent BY the user TO the partner
                f"and(sender_id.eq.{self.active_chat_receiver_id},receiver_id.eq.{SESSION['user_id']})" # Checks for messages sent BY the partner TO the user
            ).order("created_at", desc=False).execute() # Sorts them chronologically (oldest at top, newest at bottom)

            for m in result.data: # Loops through the fetched conversation
                prefix = "You: " if m["sender_id"] == SESSION["user_id"] else "Them: " # Determines if the prefix should say 'You' or 'Them' based on the sender ID
                self.lst_chat_message_history_stream.addItem(f"{prefix}{m['message']}") # Adds the formatted message to the viewing screen
                
        except Exception as err:
            print(f"Critical stream drop error: {err}") # Prints to console if fetching the conversation fails

    def send_message(self): # Function triggered to send a new message
        msg_payload = self.txt_chat_payload_input.text().strip() # Grabs typed text and removes extra spacing
        if not msg_payload or not self.active_chat_receiver_id:  # Stops if the box is empty or no partner is selected
            return
        try:
            supabase.table("messages").insert({ # Tells the database to add a new row to the messages table
                "sender_id": SESSION["user_id"], # Logs the sender as the currently logged-in user
                "receiver_id": self.active_chat_receiver_id, # Logs the receiver as the currently selected partner
                "message": msg_payload # Logs the actual text message
            }).execute() # Executes the insert command
            
            self.txt_chat_payload_input.clear()
            self.load_chat_history()
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