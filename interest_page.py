from PyQt5.QtWidgets import QMainWindow
from ui_interests import Ui_MainWindow
from backend.session import SESSION


class InterestPage(QMainWindow):

    def __init__(self, user_id=None):
        super().__init__()

        self.user_id = user_id

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_submit.clicked.connect(
            self.save_interest
        )


    def save_interest(self):

        interests = []

        boxes = [
            self.ui.chk_games,
            self.ui.chk_music,
            self.ui.chk_tech,
            self.ui.chk_cooking,
            self.ui.chk_art,
            self.ui.chk_books,
            self.ui.chk_sports,
            self.ui.chk_traveling,
            self.ui.chk_movies,
            self.ui.chk_photography
        ]


        for box in boxes:
            if box.isChecked():
                interests.append(box.text())


        if not interests:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "No Interest",
                "Select at least one interest"
            )
            return


        interest_text = ", ".join(interests)

        from backend.profile import save_interest

        result = save_interest(
            self.user_id,
            interest_text
        )

        if "successfully" in result.lower():
            QMessageBox.information(
                self,
                "Success",
                "Interest saved!"
            )

            # --- FIX: Route back to Login view (Index 0) to verify account cycle ---
            main_window = self.window()
            if hasattr(main_window, "deck"):
                main_window.deck.setCurrentIndex(0)
            elif self.parent():
                self.parent().setCurrentIndex(0)
        else:
            QMessageBox.warning(
                self,
                "Database Issue",
                str(result)
            )