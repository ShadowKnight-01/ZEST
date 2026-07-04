import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget
)

from StyleSheet import Style_used_to_in_Login
# Import your generated UI classes
from register import RegisterPage
from additional_information import AdditionalInfoPage
from interest_page import InterestPage
from loginpage import LoginPage
from zest_main import SideNavigate

class Zest_Engine(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZEST Application")
        self.resize(1100,700)
        self.setStyleSheet(Style_used_to_in_Login)

        self.deck = QStackedWidget()
        self.setCentralWidget(self.deck)

        # Primary Router Layer Map Position:
        # Index 0 -> Register Layout View
        # Index 1 -> Additional Info Layout View
        # Index 2 -> Interests Checklist View
        # Index 3 -> Login View Frame
        # Index 4 -> Operational Workplace Dashboard Switcher (ZEST Deck Suite)

        self.deck.addWidget(RegisterPage(self.deck))
        self.deck.addWidget(AdditionalInfoPage(self.deck))
        self.deck.addWidget(InterestPage(self.deck))
        self.deck.addWidget(LoginPage(self.deck))
        self.deck.addWidget(SideNavigate(self.deck))

        self.deck.setCurrentIndex(3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = Zest_Engine()
    engine.show()
    sys.exit(app.exec_())
    