Style_used_to_in_Login = """
    QWidget {
        background-color: #0B1120;
        color: #F8FAFC;
        font-family: Segoe UI;
        font-size: 14px;
    }

    QLineEdit, QTextEdit, QComboBox, QListWidget {
        background-color: #253247;
        border: 2px solid transparent;
        border-radius: 10px;
        padding: 12px;
        color: white;
        font-size: 11pt;
    }

    QLineEdit:focus, QTextEdit:focus {
        border: 2px solid #3B82F6;
    }

    QPushButton {
        background-color: #3B82F6;
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-size: 11pt;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #2563EB;
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