from qtpy.QtWidgets import QApplication, QLabel

app = QApplication([])
label = QLabel("ZEST is running 🚀")
label.resize(300, 100)
label.show()
app.exec()
