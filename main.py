import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget
)

from StyleSheet import Style_used_to_in_Login   # import the stylesheet
# Import all the app pages
from register import RegisterPage
from additional_information import AdditionalInfoPage
from interest_page import InterestPage
from loginpage import LoginPage
from zest_main import SideNavigate

class Zest_Engine(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZEST Application") # set the window title, size and style
        self.resize(1100,700)
        self.setStyleSheet(Style_used_to_in_Login)

        self.deck = QStackedWidget() # make a stacked widget to hold all page
        self.setCentralWidget(self.deck)

        # add all the pages according to this stacked widget:
        # Index 0 -> Register page
        # Index 1 -> Additional Info page
        # Index 2 -> Interests page
        # Index 3 -> Login page
        # Index 4 -> Main page

        self.deck.addWidget(RegisterPage(self.deck))
        self.deck.addWidget(AdditionalInfoPage(self.deck))
        self.deck.addWidget(InterestPage(self.deck))
        self.deck.addWidget(LoginPage(self.deck))
        self.deck.addWidget(SideNavigate(self.deck))

        self.deck.setCurrentIndex(3)  # Show the login page first when the app get started

if __name__ == "__main__":  #start the application
    app = QApplication(sys.argv)
    engine = Zest_Engine()
    engine.show()
    sys.exit(app.exec_())