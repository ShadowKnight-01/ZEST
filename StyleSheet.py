Style_used_to_in_Login = """
    QWidget { /* Main window and base text styling */
        background-color: #0B1120; /* Deep dark blue background */
        color: #F8FAFC; /* Off-white text */
        font-family: Segoe UI; /* Default font */
        font-size: 14px; /* Default text size */
    }

    QLineEdit, QTextEdit, QComboBox, QListWidget { /* Input fields and lists */
        background-color: #253247; /* Lighter dark background */
        border: 2px solid transparent; /* Invisible border */
        border-radius: 10px; /* Rounded corners */
        padding: 12px; /* Inner spacing */
        color: white; /* Text color */
        font-size: 11pt; /* Text size */
    }

    QLineEdit:focus, QTextEdit:focus { /* When typing in a text box */
        border: 2px solid #3B82F6; /* Bright blue outline */
    }

    QPushButton { /* Primary buttons */
        background-color: #3B82F6; /* Bright blue background */
        border: none; /* No border */
        border-radius: 10px; /* Rounded corners */
        padding: 12px; /* Button thickness */
        font-size: 11pt;
        font-weight: bold; /* Bold text */
    }

    QPushButton:hover { /* When mouse is over the button */
        background-color: #2563EB; /* Darker blue */
    }

    QPushButton:disabled { /* Inactive or locked buttons */
        background-color: #29292E; /* Muted dark gray */
        color: #7C7C8A; /* Faded text */
    }

    QFrame#Sidebar { /* Specific styling for the Sidebar */
        background-color: #202024; /* Dark gray background */
        border-right: 1px solid #323238; /* Right dividing line */
    }

    QCheckBox { /* Checkbox widget spacing */
        spacing: 8px; /* Gap between box and text */
    }

    QCheckBox::indicator { /* The clickable square */
        width: 18px;
        height: 18px;
        background-color: #202024; /* Dark gray box */
        border: 1px solid #323238; /* Gray outline */
        border-radius: 4px; /* Rounded corners */
    }
    
    QCheckBox::indicator:checked { /* When successfully ticked */
        background-color: #00B37E; /* Green fill */
        border: 1px solid #00B37E; /* Green outline */
    }
"""