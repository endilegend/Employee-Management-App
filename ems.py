from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
import sys
from login import LoginForm

class EMSApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EMS Application")
        self.setWindowIcon(QIcon("icon.jpg"))  # Set the application icon
        self.showFullScreen()  # Start in full-screen mode

        # Create a stacked widget to manage different screens
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Add the login screen as the default screen
        self.login_screen = LoginForm(self.central_widget)  # Pass QStackedWidget to LoginForm
        self.central_widget.addWidget(self.login_screen)
        print("Login screen added to QStackedWidget.")  # Debug print

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("EMS")  # Set the application name for the Dock
    app.setWindowIcon(QIcon("icon.icns"))  # Use the .icns file for Dock and window icon
    main_window = EMSApplication()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()