from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog, stacked_widget=None):
        self.stacked_widget = stacked_widget  # Reference to QStackedWidget for navigation
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 600)  # Increased default window size
        
        # Initialize input widgets
        self.closeCreditInput = QtWidgets.QLineEdit()
        self.closeCashInEnvInput = QtWidgets.QLineEdit()
        self.closeExpenseInput = QtWidgets.QLineEdit()
        self.CloseCommentsInput = QtWidgets.QLineEdit()
        
        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create top bar with gradient background
        self.top_bar = QtWidgets.QWidget()
        self.top_bar.setFixedHeight(60)
        self.top_bar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2c3e50, stop:1 #3498db);
            border-bottom: 1px solid #1a252f;
        """)
        
        # Create top bar layout
        self.top_bar_layout = QtWidgets.QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(20, 0, 20, 0)
        self.top_bar_layout.setSpacing(20)
        
        # Add logo/icon
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setFixedSize(40, 40)
        self.logo_label.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
            color: #2c3e50;
            font-size: 20px;
            font-weight: bold;
        """)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setText("EM")
        self.top_bar_layout.addWidget(self.logo_label)
        
        # Add employee name label with modern style
        self.employee_name_label = QtWidgets.QLabel("Employee Name")
        self.employee_name_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        self.employee_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.top_bar_layout.addWidget(self.employee_name_label)
        
        # Add store name label
        self.store_name_label = QtWidgets.QLabel("Store Name")
        self.store_name_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        self.store_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.top_bar_layout.addWidget(self.store_name_label)
        
        # Add store combo box with modern style
        self.store_combo = QtWidgets.QComboBox()
        self.store_combo.setFixedWidth(200)
        self.store_combo.addItem("Select Store")
        self.store_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                color: #2c3e50;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox:hover {
                background-color: #f5f5f5;
            }
        """)
        self.top_bar_layout.addWidget(self.store_combo)
        
        # Add top bar to main layout
        self.main_layout.addWidget(self.top_bar)
        
        # Create content area
        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setStyleSheet("background-color: #f5f7fa;")
        self.content_layout = QtWidgets.QHBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Create sidebar with modern style
        self.sidebar = QtWidgets.QWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            background-color: white;
            border-right: 1px solid #e0e0e0;
        """)
        
        # Create vertical layout for sidebar buttons
        self.verticalLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.verticalLayout.setContentsMargins(10, 20, 10, 20)
        self.verticalLayout.setSpacing(10)
        
        # Define sidebar buttons explicitly
        self.clockInViewBtn = QtWidgets.QPushButton("Clock-In")
        self.clockOutViewBtn = QtWidgets.QPushButton("Clock-Out")
        self.closeViewBtn = QtWidgets.QPushButton("Close")
        self.historyViewBtn = QtWidgets.QPushButton("History")
        self.signOutBtn = QtWidgets.QPushButton("Sign-Out")

        # Add buttons to sidebar with modern style
        buttons = [
            (self.clockInViewBtn, "#2ecc71"),
            (self.clockOutViewBtn, "#e74c3c"),
            (self.closeViewBtn, "#f39c12"),
            (self.historyViewBtn, "#3498db"),
            (self.signOutBtn, "#95a5a6")
        ]
        
        for btn, color in buttons:
            btn.setFixedHeight(45)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0 10px;
                }}
                QPushButton:hover {{
                    background-color: {color}dd;
                }}
                QPushButton:pressed {{
                    background-color: {color}bb;
                }}
            """)
            self.verticalLayout.addWidget(btn)
        
        # Add spacer at the bottom
        self.verticalLayout.addStretch()
        
        # Add sidebar to content layout
        self.content_layout.addWidget(self.sidebar)
        
        # Create main content area
        self.main_content = QtWidgets.QWidget()
        self.main_content.setStyleSheet("background-color: #f5f7fa;")
        
        # Create stacked widget for frames
        self.stackedWidget = QtWidgets.QStackedWidget(self.main_content)
        self.stackedWidget.setStyleSheet("""
            QStackedWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        # Create frames with modern style
        self.create_clock_in_frame()
        self.create_clock_out_frame()
        self.create_close_frame()
        self.create_history_frame()
        
        # Add stacked widget to main content
        main_content_layout = QtWidgets.QVBoxLayout(self.main_content)
        main_content_layout.setContentsMargins(20, 20, 20, 20)
        main_content_layout.addWidget(self.stackedWidget)
        
        # Add main content to content layout
        self.content_layout.addWidget(self.main_content)
        
        # Add content widget to main layout
        self.main_layout.addWidget(self.content_widget)
        
        # Connect buttons to switch frames
        self.clockInViewBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.btnClockIn))
        self.clockOutViewBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.btnClockOut))
        self.closeViewBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.btnClose))
        self.historyViewBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.btnHistory))
        
        # Connect the "Sign-Out" button to the sign-out functionality
        self.signOutBtn.clicked.connect(self.sign_out)

        # Set the default frame to the Clock-In frame
        self.stackedWidget.setCurrentWidget(self.btnClockIn)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def sign_out(self):
        print("Signing out...")  # Debug print
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(0)  # Redirect to the login screen

    def create_clock_in_frame(self):
        self.btnClockIn = QtWidgets.QWidget()
        self.btnClockIn.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(self.btnClockIn)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QtWidgets.QLabel("Clock In")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Balance input
        self.RegInBalanceInput = QtWidgets.QLineEdit()
        self.RegInBalanceInput.setPlaceholderText("Enter Register Balance")
        self.RegInBalanceInput.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 16px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
        """)
        layout.addWidget(self.RegInBalanceInput)
        
        # Clock In button
        self.clockInBtn = QtWidgets.QPushButton("Clock In")
        self.clockInBtn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
        """)
        layout.addWidget(self.clockInBtn)
        
        layout.addStretch()
        self.stackedWidget.addWidget(self.btnClockIn)

    def create_clock_out_frame(self):
        self.btnClockOut = QtWidgets.QWidget()
        self.btnClockOut.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(self.btnClockOut)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QtWidgets.QLabel("Clock Out")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Balance input
        self.RegOutBalanceInput = QtWidgets.QLineEdit()
        self.RegOutBalanceInput.setPlaceholderText("Enter Register Balance")
        self.RegOutBalanceInput.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 16px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
        """)
        layout.addWidget(self.RegOutBalanceInput)
        
        # Clock Out button
        self.ClockOutBtn = QtWidgets.QPushButton("Clock Out")
        self.ClockOutBtn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        layout.addWidget(self.ClockOutBtn)
        
        layout.addStretch()
        self.stackedWidget.addWidget(self.btnClockOut)

    def create_close_frame(self):
        self.btnClose = QtWidgets.QWidget()
        self.btnClose.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(self.btnClose)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QtWidgets.QLabel("Close Register")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)
        
        # Input fields
        fields = [
            ("Credit Amount", self.closeCreditInput),
            ("Cash in Envelope", self.closeCashInEnvInput),
            ("Expenses", self.closeExpenseInput),
            ("Comments", self.CloseCommentsInput)
        ]
        
        for label_text, input_widget in fields:
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
            """)
            
            input_widget.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 2px solid #e0e0e0;
                    border-radius: 6px;
                    font-size: 14px;
                    background-color: #f8f9fa;
                }
                QLineEdit:focus {
                    border-color: #3498db;
                    background-color: white;
                }
            """)
            
            form_layout.addRow(label, input_widget)
        
        layout.addLayout(form_layout)
        
        # Submit button
        self.closeSubmitBtn = QtWidgets.QPushButton("Submit")
        self.closeSubmitBtn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
        """)
        layout.addWidget(self.closeSubmitBtn)
        
        layout.addStretch()
        self.stackedWidget.addWidget(self.btnClose)

    def create_history_frame(self):
        self.btnHistory = QtWidgets.QWidget()
        self.btnHistory.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(self.btnHistory)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QtWidgets.QLabel("History")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Table
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(8)
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(self.tableWidget)
        
        self.stackedWidget.addWidget(self.btnHistory)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Employee Management"))
        self.clockInBtn.setText(_translate("Dialog", "Clock-In"))
        self.RegInBalanceInput.setPlaceholderText(_translate("Dialog", "Enter Register Balance"))
        self.ClockOutBtn.setText(_translate("Dialog", "Clock-Out"))
        self.RegOutBalanceInput.setPlaceholderText(_translate("Dialog", "Enter Register Balance"))
        self.closeCreditInput.setPlaceholderText(_translate("Dialog", "Enter Credit Amount"))
        self.closeCashInEnvInput.setPlaceholderText(_translate("Dialog", "Enter Cash in Envelope"))
        self.closeExpenseInput.setPlaceholderText(_translate("Dialog", "Enter Expenses"))
        self.CloseCommentsInput.setPlaceholderText(_translate("Dialog", "Enter Comments"))
        self.closeSubmitBtn.setText(_translate("Dialog", "Submit"))
        self.clockInViewBtn.setText(_translate("Dialog", "Clock-In"))
        self.clockOutViewBtn.setText(_translate("Dialog", "Clock-Out"))
        self.closeViewBtn.setText(_translate("Dialog", "Close"))
        self.historyViewBtn.setText(_translate("Dialog", "History"))
        self.signOutBtn.setText(_translate("Dialog", "Sign-Out"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

