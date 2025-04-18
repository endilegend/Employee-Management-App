from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox  # Import QMessageBox
from sqlConnector import connect  # Import the database connection function
from datetime import datetime, timedelta  # Import datetime and timedelta
import pytz  # For handling time zones


class Ui_Dialog(object):
    def setupUi(self, Dialog, stacked_widget=None, employee_id=None):
        self.stacked_widget = stacked_widget  # Reference to QStackedWidget for navigation
        self.employee_id = employee_id  # Set the employee ID from the login page
        self.store_id = None  # Placeholder for store ID
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
        
        # Fetch employee name from database
        if self.employee_id:
            try:
                query = "SELECT firstName, lastName FROM employee WHERE employee_id = %s"
                data = (self.employee_id,)
                results = connect(query, data)
                
                if results and len(results) > 0:
                    employee = results[0]
                    self.employee_name = f"{employee[0]} {employee[1]}"
                else:
                    self.employee_name = "Employee Name"
            except Exception as e:
                print(f"Error fetching employee name: {e}")
                self.employee_name = "Employee Name"
        else:
            self.employee_name = "Employee Name"
        
        # Add employee name label with modern style
        self.employee_name_label = QtWidgets.QLabel(self.employee_name)
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
        
        # Fetch stores from the database and populate the combo box
        self.populate_stores()
        
        # Connect the combo box to update the store name label and store ID
        self.store_combo.currentIndexChanged.connect(self.update_store_id)
        
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
        
        # Connect the Clock-In and Clock-Out buttons to their respective methods
        self.clockInBtn.clicked.connect(self.clock_in)
        self.ClockOutBtn.clicked.connect(self.clock_out)

        # Set the default frame to the Clock-In frame
        self.stackedWidget.setCurrentWidget(self.btnClockIn)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def sign_out(self):
        print("Signing out...")  # Debug print
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(0)  # Redirect to the login screen

    def populate_stores(self):
        """Fetch stores from the database and populate the combo box."""
        query = "SELECT store_id, store_name FROM Store"
        results = connect(query, None)

        if results:
            # Set the first store as the default
            first_store = results[0]
            self.store_id = first_store[0]  # Store the store ID
            self.store_name_label.setText(first_store[1])
            self.store_combo.addItem(first_store[1])

            # Add the rest of the stores to the combo box
            for store in results[1:]:
                self.store_combo.addItem(store[1])

    def update_store_id(self):
        """Update the store ID when a new store is selected."""
        selected_index = self.store_combo.currentIndex()
        query = "SELECT store_id FROM Store LIMIT %s, 1"
        data = (selected_index,)
        results = connect(query, data)

        if results:
            self.store_id = results[0][0]
            print(f"Store ID updated to: {self.store_id}")  # Debug print

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

    def clock_in(self):
        """Handle the clock-in operation."""
        print(f"Attempting to clock in employee ID: {self.employee_id}")
        
        if not self.employee_id:
            QMessageBox.critical(None, "Error", "Employee ID is missing. Please log in again.")
            print("Error: Employee ID is missing")
            return

        if not self.store_id:
            QMessageBox.critical(None, "Error", "Store ID is missing. Please select a store.")
            print("Error: Store ID is missing")
            return

        # Get the current time in Miami timezone
        try:
            miami_tz = pytz.timezone("America/New_York")
            current_time = datetime.now(miami_tz)
            print(f"Current time in Miami: {current_time}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to get current time: {e}")
            print(f"Error getting current time: {e}")
            return

        # Get the cash-in value from the input
        try:
            reg_in = float(self.RegInBalanceInput.text())
            print(f"Register in amount: ${reg_in:.2f}")
        except ValueError:
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid cash-in amount.")
            print("Error: Invalid cash-in amount")
            return

        # Check if the employee is already clocked in
        try:
            query = "SELECT * FROM clockTable WHERE employee_id = %s AND store_id = %s AND clock_out IS NULL"
            data = (self.employee_id, self.store_id)
            print(f"Checking if employee is already clocked in. Query: {query}, Data: {data}")
            results = connect(query, data)
            print(f"Clock-in check results: {results}")

            if results:
                QMessageBox.warning(None, "Already Clocked In", "You are already clocked in. Please clock out first.")
                print("Error: Employee already clocked in")
                return
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to check clock-in status: {e}")
            print(f"Error checking clock-in status: {e}")
            return

        # Insert a new clock-in entry
        try:
            query = """
                INSERT INTO clockTable (employee_id, store_id, clock_in, reg_in)
                VALUES (%s, %s, %s, %s)
            """
            data = (self.employee_id, self.store_id, current_time, reg_in)
            print(f"Inserting clock-in record. Query: {query}, Data: {data}")
            success = connect(query, data)
            print(f"Clock-in insert result: {success}")

            if success:
                QMessageBox.information(None, "Clock-In Successful", "You have successfully clocked in.")
                self.RegInBalanceInput.clear()  # Clear the input field
                print("Clock-in successful")
            else:
                QMessageBox.critical(None, "Clock-In Failed", "An error occurred while clocking in.")
                print("Error: Clock-in insert failed")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to clock in: {e}")
            print(f"Error during clock-in: {e}")

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

    def clock_out(self):
        """Handle the clock-out operation."""
        print(f"Attempting to clock out employee ID: {self.employee_id}")
        
        if not self.employee_id:
            QMessageBox.critical(None, "Error", "Employee ID is missing. Please log in again.")
            print("Error: Employee ID is missing")
            return

        if not self.store_id:
            QMessageBox.critical(None, "Error", "Store ID is missing. Please select a store.")
            print("Error: Store ID is missing")
            return

        # Get the current time in Miami timezone
        try:
            miami_tz = pytz.timezone("America/New_York")
            current_time = datetime.now(miami_tz)
            print(f"Current time in Miami: {current_time}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to get current time: {e}")
            print(f"Error getting current time: {e}")
            return

        # Get the cash-out value from the input
        try:
            reg_out = float(self.RegOutBalanceInput.text())
            print(f"Register out amount: ${reg_out:.2f}")
        except ValueError:
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid cash-out amount.")
            print("Error: Invalid cash-out amount")
            return

        # Check if the employee is clocked in
        try:
            query = "SELECT * FROM clockTable WHERE employee_id = %s AND store_id = %s AND clock_out IS NULL"
            data = (self.employee_id, self.store_id)
            print(f"Checking if employee is clocked in. Query: {query}, Data: {data}")
            results = connect(query, data)
            print(f"Clock-out check results: {results}")

            if not results:
                QMessageBox.warning(None, "Not Clocked In", "You are not clocked in. Please clock in first.")
                print("Error: Employee not clocked in")
                return
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to check clock-out status: {e}")
            print(f"Error checking clock-out status: {e}")
            return

        # Update the clock-out entry
        try:
            query = """
                UPDATE clockTable
                SET clock_out = %s, reg_out = %s
                WHERE employee_id = %s AND store_id = %s AND clock_out IS NULL
            """
            data = (current_time, reg_out, self.employee_id, self.store_id)
            print(f"Updating clock-out record. Query: {query}, Data: {data}")
            success = connect(query, data)
            print(f"Clock-out update result: {success}")

            if success:
                QMessageBox.information(None, "Clock-Out Successful", "You have successfully clocked out.")
                self.RegOutBalanceInput.clear()  # Clear the input field
                print("Clock-out successful")
            else:
                QMessageBox.critical(None, "Clock-Out Failed", "An error occurred while clocking out.")
                print("Error: Clock-out update failed")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to clock out: {e}")
            print(f"Error during clock-out: {e}")

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
        
        # Connect the submit button to the close_submit method
        self.closeSubmitBtn.clicked.connect(self.close_submit)
        
        layout.addStretch()
        self.stackedWidget.addWidget(self.btnClose)

    def close_submit(self):
        """Handle the close register submission."""
        print(f"Attempting to submit close register for employee ID: {self.employee_id}")
        
        if not self.employee_id:
            QMessageBox.critical(None, "Error", "Employee ID is missing. Please log in again.")
            print("Error: Employee ID is missing")
            return

        if not self.store_id:
            QMessageBox.critical(None, "Error", "Store ID is missing. Please select a store.")
            print("Error: Store ID is missing")
            return

        # Get store name
        try:
            query = "SELECT store_name FROM Store WHERE store_id = %s"
            data = (self.store_id,)
            print(f"Fetching store name. Query: {query}, Data: {data}")
            results = connect(query, data)
            print(f"Store name results: {results}")
            
            if not results:
                QMessageBox.critical(None, "Error", "Could not find store information.")
                print("Error: Store not found")
                return
                
            store_name = results[0][0]
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to get store information: {e}")
            print(f"Error getting store information: {e}")
            return

        # Get employee name
        try:
            query = "SELECT firstName, lastName FROM employee WHERE employee_id = %s"
            data = (self.employee_id,)
            print(f"Fetching employee name. Query: {query}, Data: {data}")
            results = connect(query, data)
            print(f"Employee name results: {results}")
            
            if not results:
                QMessageBox.critical(None, "Error", "Could not find employee information.")
                print("Error: Employee not found")
                return
                
            first_name = results[0][0]
            last_name = results[0][1]
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to get employee information: {e}")
            print(f"Error getting employee information: {e}")
            return

        # Validate and get input values
        try:
            credit = float(self.closeCreditInput.text()) if self.closeCreditInput.text() else 0.0
            cash_in_envelope = float(self.closeCashInEnvInput.text()) if self.closeCashInEnvInput.text() else 0.0
            expense = float(self.closeExpenseInput.text()) if self.closeExpenseInput.text() else 0.0
            comments = self.CloseCommentsInput.text() if self.CloseCommentsInput.text() else ""
            
            print(f"Input values - Credit: ${credit:.2f}, Cash: ${cash_in_envelope:.2f}, Expense: ${expense:.2f}")
        except ValueError:
            QMessageBox.warning(None, "Invalid Input", "Please enter valid numbers for credit, cash, and expense amounts.")
            print("Error: Invalid input values")
            return

        try:
            # First, delete any existing record for this store on the current date
            delete_query = """
                DELETE FROM employee_close 
                WHERE store_name = %s 
                AND DATE(timestamp) = CURDATE()
            """
            delete_data = (store_name,)
            print(f"Deleting existing close record. Query: {delete_query}, Data: {delete_data}")
            connect(delete_query, delete_data)
            
            # Then insert the new record
            insert_query = """
                INSERT INTO employee_close 
                (firstName, lastName, store_name, credit, cash_in_envelope, expense, comments, employee_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            insert_data = (first_name, last_name, store_name, credit, cash_in_envelope, expense, comments, self.employee_id)
            print(f"Inserting new close record. Query: {insert_query}, Data: {insert_data}")
            success = connect(insert_query, insert_data)
            print(f"Close register insert result: {success}")

            if success:
                QMessageBox.information(None, "Success", "Close register submitted successfully.")
                # Clear input fields
                self.closeCreditInput.clear()
                self.closeCashInEnvInput.clear()
                self.closeExpenseInput.clear()
                self.CloseCommentsInput.clear()
                print("Close register submission successful")
            else:
                QMessageBox.critical(None, "Error", "Failed to submit close register.")
                print("Error: Close register insert failed")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to submit close register: {e}")
            print(f"Error during close register submission: {e}")

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
        layout.setSpacing(20)
        
        # Title
        title = QtWidgets.QLabel("Clock History")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Create table widget
        self.historyTable = QtWidgets.QTableWidget()
        self.historyTable.setColumnCount(6)
        self.historyTable.setHorizontalHeaderLabels([
            "Date", "Clock In", "Clock Out", "Register In", "Register Out", "Shift Duration"
        ])
        
        # Style the table
        self.historyTable.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 8px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        
        # Set table properties
        self.historyTable.setAlternatingRowColors(True)
        self.historyTable.setShowGrid(False)
        
        # Add refresh button
        refresh_btn = QtWidgets.QPushButton("Refresh History")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2475a8;
            }
        """)
        refresh_btn.clicked.connect(self.load_history)
        
        # Add widgets to layout
        layout.addWidget(self.historyTable)
        layout.addWidget(refresh_btn, alignment=QtCore.Qt.AlignRight)
        
        self.stackedWidget.addWidget(self.btnHistory)
        
        # Load initial history
        self.load_history()

    def load_history(self):
        """Load the employee's clock history for the past 7 days."""
        if not self.employee_id:
            QMessageBox.warning(None, "Error", "Employee ID is missing.")
            return

        try:
            print(f"Loading history for employee ID: {self.employee_id}")
            
            # Query to get clock history for the past 7 days
            query = """
                SELECT 
                    DATE(clock_in) as date,
                    TIME(clock_in) as clock_in_time,
                    TIME(clock_out) as clock_out_time,
                    reg_in,
                    reg_out,
                    TIMESTAMPDIFF(MINUTE, clock_in, clock_out) as duration_minutes
                FROM clockTable
                WHERE employee_id = %s 
                AND clock_in >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                ORDER BY clock_in DESC
            """
            data = (self.employee_id,)
            print(f"Executing query: {query}")
            print(f"With parameters: {data}")
            
            results = connect(query, data)
            print(f"Query results: {results}")

            # Clear existing table data
            self.historyTable.setRowCount(0)

            if isinstance(results, bool):
                print("Database connection returned boolean instead of results")
                QMessageBox.critical(None, "Error", "Failed to connect to database.")
                return

            # Create a list to store all history records
            history_records = []
            if results and len(results) > 0:
                print(f"Found {len(results)} clock records")
                for row_data in results:
                    try:
                        date = row_data[0].strftime("%Y-%m-%d")
                        print(f"Processing record for date: {date}")
                        
                        # Handle clock in time (convert timedelta to time string)
                        clock_in_td = row_data[1]
                        if isinstance(clock_in_td, timedelta):
                            total_seconds = int(clock_in_td.total_seconds())
                            hours = total_seconds // 3600
                            minutes = (total_seconds % 3600) // 60
                            seconds = total_seconds % 60
                            clock_in = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                        else:
                            clock_in = "-"
                        print(f"Clock in time: {clock_in}")
                        
                        # Handle clock out time (convert timedelta to time string)
                        clock_out_td = row_data[2]
                        if isinstance(clock_out_td, timedelta):
                            total_seconds = int(clock_out_td.total_seconds())
                            hours = total_seconds // 3600
                            minutes = (total_seconds % 3600) // 60
                            seconds = total_seconds % 60
                            clock_out = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                        else:
                            clock_out = "-"
                        print(f"Clock out time: {clock_out}")
                        
                        # Handle register amounts
                        reg_in = f"${float(row_data[3]):.2f}" if row_data[3] is not None else "-"
                        reg_out = f"${float(row_data[4]):.2f}" if row_data[4] is not None else "-"
                        print(f"Register in: {reg_in}, Register out: {reg_out}")
                        
                        # Handle duration
                        duration_minutes = row_data[5]
                        duration = self.format_duration(duration_minutes) if duration_minutes is not None else "-"
                        print(f"Duration: {duration}")
                        
                        # Add record to list
                        history_records.append({
                            'date': date,
                            'clock_in': clock_in,
                            'clock_out': clock_out,
                            'reg_in': reg_in,
                            'reg_out': reg_out,
                            'duration': duration
                        })
                    except Exception as e:
                        print(f"Error processing row data: {e}")
                        print(f"Row data: {row_data}")
                        continue

            # Get the last 7 days
            today = datetime.now().date()
            last_7_days = [(today - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(7)]
            print(f"Last 7 days: {last_7_days}")

            # Add rows for each record
            for record in history_records:
                row = self.historyTable.rowCount()
                self.historyTable.insertRow(row)
                
                # Add items to table
                self.historyTable.setItem(row, 0, QtWidgets.QTableWidgetItem(record['date']))
                self.historyTable.setItem(row, 1, QtWidgets.QTableWidgetItem(record['clock_in']))
                self.historyTable.setItem(row, 2, QtWidgets.QTableWidgetItem(record['clock_out']))
                self.historyTable.setItem(row, 3, QtWidgets.QTableWidgetItem(record['reg_in']))
                self.historyTable.setItem(row, 4, QtWidgets.QTableWidgetItem(record['reg_out']))
                self.historyTable.setItem(row, 5, QtWidgets.QTableWidgetItem(record['duration']))
                
                # Center align all items
                for col in range(6):
                    self.historyTable.item(row, col).setTextAlignment(QtCore.Qt.AlignCenter)
            
            # Resize columns to fit content
            self.historyTable.resizeColumnsToContents()
            self.historyTable.horizontalHeader().setStretchLastSection(True)
            
            if not history_records:
                print("No clock history found for the past 7 days")
                QMessageBox.information(None, "No History", "No clock history found for the past 7 days.")
                
        except Exception as e:
            print(f"Error in load_history: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            QMessageBox.critical(None, "Error", f"Failed to load history: {str(e)}")

    def format_duration(self, minutes):
        """Format duration in minutes to hours and minutes."""
        if minutes is None:
            return "-"
        try:
            hours = minutes // 60
            minutes = minutes % 60
            return f"{hours}h {minutes}m"
        except Exception as e:
            print(f"Error formatting duration: {e}")
            return "-"

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

