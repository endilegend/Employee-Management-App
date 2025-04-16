import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt
from sqlConnector import connect

class LoginForm(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Login Form')
		self.resize(500, 120)

		# Set background image
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setBrush(QPalette.Window, QBrush(QPixmap("clwbeach.jpg")))
		self.setPalette(palette)

		# Create a container for the white box with modern styling
		container = QWidget(self)
		container.setStyleSheet("""
			background-color: white;
			border-radius: 15px;
			padding: 20px;
		""")

		# Add shadow effect to the container
		shadow = QGraphicsDropShadowEffect()
		shadow.setBlurRadius(15)
		shadow.setOffset(0, 0)
		container.setGraphicsEffect(shadow)

		container_layout = QGridLayout(container)

		label_name = QLabel('<font size="4"> Username </font>')
		self.lineEdit_username = QLineEdit()
		self.lineEdit_username.setPlaceholderText('Enter username')
		self.lineEdit_username.setStyleSheet("""
			border: 1px solid #ccc;
			border-radius: 10px;
			padding: 8px;
			font-size: 14px;
		""")
		container_layout.addWidget(label_name, 0, 0)
		container_layout.addWidget(self.lineEdit_username, 0, 1)

		label_password = QLabel('<font size="4"> Password </font>')
		self.lineEdit_password = QLineEdit()
		self.lineEdit_password.setPlaceholderText('Enter password')
		self.lineEdit_password.setEchoMode(QLineEdit.Password)  # Set password echo mode
		self.lineEdit_password.setStyleSheet("""
			border: 1px solid #ccc;
			border-radius: 10px;
			padding: 8px;
			font-size: 14px;
		""")
		container_layout.addWidget(label_password, 1, 0)
		container_layout.addWidget(self.lineEdit_password, 1, 1)

		button_login = QPushButton('Login')
		button_login.setStyleSheet("""
			background-color: #007BFF;
			color: white;
			border: none;
			border-radius: 10px;
			padding: 10px 20px;
			font-size: 14px;
		""")
		button_login.clicked.connect(self.check_password)
		container_layout.addWidget(button_login, 2, 0, 1, 2, alignment=Qt.AlignCenter)
		container_layout.setRowMinimumHeight(2, 75)

		# Center the white box on the main layout
		main_layout = QGridLayout(self)
		main_layout.addWidget(container, 0, 0, 1, 1, alignment=Qt.AlignCenter)
		self.setLayout(main_layout)

	def check_password(self):
		msg = QMessageBox()

		# Query to check username and password
		query = "SELECT * FROM employee WHERE userName = %s AND password = %s"
		data = (self.lineEdit_username.text(), self.lineEdit_password.text())

		# Execute the query using the connect function
		results = connect(query, data)

		if results and len(results) > 0:
			role = results[0][4]  # Assuming the role is in the 5th column (index 4)
			msg.setText('Login Successful')
			msg.exec_()

			# Redirect based on role
			if role == 'owner':
				subprocess.Popen(["python3", "owner.py"])
			elif role == 'manager':
				subprocess.Popen(["python3", "manager.py"])
			elif role == 'employee':
				subprocess.Popen(["python3", "employee.py"])

			QApplication.instance().quit()  # Properly quit the application
		else:
			msg.setText('Invalid Username or Password')
			msg.exec_()

if __name__ == '__main__':
	app = QApplication(sys.argv)

	form = LoginForm()
	form.show()

	sys.exit(app.exec_())