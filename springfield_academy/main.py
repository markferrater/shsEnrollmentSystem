import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from views.login_window import LoginWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Springfield Academy")
    app.setStyle("Fusion")
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
