from PyQt5 import QtCore, QtGui, QtWidgets
from sqlConnector import connect  # Import the database connection function
from datetime import datetime  # Add datetime import


class Ui_ManagerDialog(object):  # Updated class name

    # ----------------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------------
    def setupUi(self, Dialog, stacked_widget=None, employee_id=None):
        # Initialize input widgets for close frame
        self.closeCreditInput = QtWidgets.QLineEdit()
        self.closeCashInEnvInput = QtWidgets.QLineEdit()
        self.closeExpenseInput = QtWidgets.QLineEdit()
        self.CloseCommentsInput = QtWidgets.QLineEdit()

        # Initialize expenses view attributes
        self.expenses_current_date = QtCore.QDate.currentDate()
        self.is_expenses_weekly_view = True

        self.stacked_widget = stacked_widget  # Reference to QStackedWidget for navigation
        self.employee_id = employee_id  # Set the employee ID from the login page
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 650)
        Dialog.setMinimumSize(800, 540)

        # ---------------------------------------------------------------------
        # Main vertical layout holding top‑bar + central content
        # ---------------------------------------------------------------------
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self._create_top_bar()
        self._create_content_area()

        # Default page – Enter Invoice
        self.stackedWidget.setCurrentWidget(self.page_invoice)

        self._retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # ----------------------------------------------------------------------------
    # UI construction helpers
    # ----------------------------------------------------------------------------
    def _create_top_bar(self):
        """Creates the gradient top bar shared across all pages."""
        print(f"Creating top bar with employee_id: {self.employee_id}")  # Debug print
        
        self.top_bar = QtWidgets.QWidget()
        self.top_bar.setFixedHeight(60)
        self.top_bar.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #2c3e50, stop:1 #3498db);
                border-bottom: 1px solid #1a252f;
            }
            """
        )

        bar_layout = QtWidgets.QHBoxLayout(self.top_bar)
        bar_layout.setContentsMargins(20, 0, 20, 0)
        bar_layout.setSpacing(20)

        # Logo circle
        logo = QtWidgets.QLabel("EM")
        logo.setFixedSize(40, 40)
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setStyleSheet(
            """
            QLabel {
                background-color: white;
                border-radius: 20px;
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
            }
            """
        )
        bar_layout.addWidget(logo)

        # Fetch owner name from database
        if self.employee_id:
            try:
                print(f"Fetching owner name for employee_id: {self.employee_id}")  # Debug print
                query = "SELECT firstName, lastName FROM employee WHERE employee_id = %s"
                data = (self.employee_id,)
                print(f"Executing query: {query} with data: {data}")  # Debug print
                results = connect(query, data)
                print(f"Query results: {results}")  # Debug print
                
                if results and len(results) > 0:
                    employee = results[0]
                    self.owner_name = f"{employee[0]} {employee[1]}"
                    print(f"Set owner name to: {self.owner_name}")  # Debug print
                else:
                    self.owner_name = "Owner Name"
                    print("No results found, using default owner name")  # Debug print
            except Exception as e:
                print(f"Error fetching owner name: {e}")  # Debug print
                self.owner_name = "Owner Name"
        else:
            self.owner_name = "Owner Name"
            print("No employee_id provided, using default owner name")  # Debug print

        # Owner name label
        self.owner_name_label = QtWidgets.QLabel(self.owner_name)
        self.owner_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.owner_name_label.setStyleSheet(
            """color: white; font-size: 16px; font-weight: bold;"""
        )
        bar_layout.addWidget(self.owner_name_label)
        print(f"Added owner name label with text: {self.owner_name}")  # Debug print

        # Store name label
        self.store_name_label = QtWidgets.QLabel("Store Name")
        self.store_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.store_name_label.setStyleSheet(
            """color: white; font-size: 16px; font-weight: bold;"""
        )
        bar_layout.addWidget(self.store_name_label)

        # Store selector
        self.store_combo = QtWidgets.QComboBox()
        self.store_combo.setFixedWidth(200)
        self.store_combo.setStyleSheet(
            """
            QComboBox {
                background-color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                color: #2c3e50;
            }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox:hover { background-color: #f5f5f5; }
            """
        )
        self.store_combo.currentIndexChanged.connect(self.update_store_id)
        bar_layout.addWidget(self.store_combo)

        # Populate stores from database
        self.populate_stores()

        self.main_layout.addWidget(self.top_bar)

    def populate_stores(self):
        """Fetch stores from the database and populate the combo box."""
        try:
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
        except Exception as e:
            print(f"Error populating stores: {e}")
            self.store_name_label.setText("Store Name")

    def update_store_id(self):
        """Update the store ID when a new store is selected."""
        try:
            selected_text = self.store_combo.currentText()
            if not selected_text:
                return
                
            query = "SELECT store_id FROM Store WHERE store_name = %s"
            data = (selected_text,)
            results = connect(query, data)

            if results:
                self.store_id = results[0][0]
                self.store_name_label.setText(selected_text)
                print(f"Store ID updated to: {self.store_id}")
        except Exception as e:
            print(f"Error updating store ID: {e}")
            self.store_name_label.setText("Store Name")

    def _create_content_area(self):
        """Creates sidebar + stacked pages."""
        # ---------- Wrapper widget ----------
        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setStyleSheet("background-color: #f5f7fa;")
        content_layout = QtWidgets.QHBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # ---------- Sidebar ----------
        self.sidebar = QtWidgets.QWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet(
            "background-color: white; border-right: 1px solid #e0e0e0;"
        )
        sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)

        # Button text and colors
        buttons_def = [
            ("Enter Invoice", "#16a085"),
            ("Enter Expense", "#c0392b"),
            ("Enter Merchandise", "#8e44ad"),
            ("Close Register", "#f39c12"),
            ("Employee History", "#2980b9"),
            ("Expenses History", "#d35400"),
            ("Merchandise History", "#2ecc71"),
            ("Invoice History", "#e67e22"),  # Added Invoice History button
            ("Close History", "#3498db"),
            ("Gross Profit", "#f1c40f"),
            ("Payroll", "#e67e22"),
            ("Manage Users", "#95a5a6"),
        ]

        self.sidebar_buttons = {}
        for text, color in buttons_def:
            btn = QtWidgets.QPushButton(text)
            btn.setFixedHeight(45)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {color};
                    color: {'#2c3e50' if color == '#f1c40f' else 'white'};
                    border: none;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0 10px;
                }}
                QPushButton:hover {{ background-color: {color}dd; }}
                QPushButton:pressed {{ background-color: {color}bb; }}
                """
            )
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons[text] = btn

        # Add Sign-Out button to the sidebar
        self.sign_out_btn = QtWidgets.QPushButton("Sign-Out")
        self.sign_out_btn.setFixedHeight(45)
        self.sign_out_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
            """
        )
        self.sign_out_btn.clicked.connect(self.sign_out)
        sidebar_layout.addWidget(self.sign_out_btn)

        sidebar_layout.addStretch()
        content_layout.addWidget(self.sidebar)

        # ---------- Stacked pages ----------
        self.main_content = QtWidgets.QWidget()
        self.main_content.setStyleSheet("background-color: #f5f7fa;")
        mc_layout = QtWidgets.QVBoxLayout(self.main_content)
        mc_layout.setContentsMargins(20, 20, 20, 20)

        self.stackedWidget = QtWidgets.QStackedWidget()
        self.stackedWidget.setStyleSheet(
            """QStackedWidget { background-color: white; border-radius: 8px; border: 1px solid #e0e0e0; }"""
        )

        # Create pages
        self.page_invoice = self._create_invoice_page()
        self.page_expense = self._create_expense_page()
        self.page_merchandise = self._create_merchandise_page()
        self.page_emp_hist = self._create_employee_history_page()
        self.page_exp_hist = self._create_expenses_history_page()
        self.page_merch_hist = self._create_merchandise_history_page()
        self.page_invoice_hist = self._create_invoice_history_page()  # Added invoice history page
        self.page_close_hist = self._create_close_history_page()
        self.page_close = self._create_close_page()
        self.page_gross_profit = self._create_gross_profit_page()
        self.page_payroll = self._create_payroll_page()
        self.page_manage_users = self._create_manage_users_page()

        mc_layout.addWidget(self.stackedWidget)
        content_layout.addWidget(self.main_content)
        self.main_layout.addWidget(self.content_widget)

        # ---------- Connections ----------
        mapping = {
            "Enter Invoice": self.page_invoice,
            "Enter Expense": self.page_expense,
            "Enter Merchandise": self.page_merchandise,
            "Employee History": self.page_emp_hist,
            "Expenses History": self.page_exp_hist,
            "Merchandise History": self.page_merch_hist,
            "Invoice History": self.page_invoice_hist,  # Added mapping for invoice history
            "Close History": self.page_close_hist,
            "Close Register": self.page_close,
            "Gross Profit": self.page_gross_profit,
            "Payroll": self.page_payroll,
            "Manage Users": self.page_manage_users,
        }
        for text, btn in self.sidebar_buttons.items():
            btn.clicked.connect(lambda checked, w=mapping[text]: self.stackedWidget.setCurrentWidget(w))


    def _create_invoice_page(self):
        """Create the invoice page with input fields and submit functionality."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section with icon
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title with icon
        title = QtWidgets.QLabel("Enter Invoice")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Form container with shadow
        form_container = QtWidgets.QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        form_layout = QtWidgets.QFormLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Input field styling
        input_style = """
            QLineEdit, QDateEdit, QComboBox {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
                min-height: 20px;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QDateEdit::drop-down {
                border: none;
                width: 30px;
            }
        """

        # Label styling
        label_style = """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0;
            }
        """

        # Invoice ID input
        self.invoice_id_input = QtWidgets.QLineEdit()
        self.invoice_id_input.setPlaceholderText("Enter Invoice ID")
        self.invoice_id_input.setStyleSheet(input_style)
        id_label = QtWidgets.QLabel("Invoice ID")
        id_label.setStyleSheet(label_style)
        form_layout.addRow(id_label, self.invoice_id_input)

        # Recieved date input
        self.recieved_date_input = QtWidgets.QDateEdit()
        self.recieved_date_input.setCalendarPopup(True)
        self.recieved_date_input.setDate(QtCore.QDate.currentDate())
        self.recieved_date_input.setStyleSheet(input_style)
        recieved_date_label = QtWidgets.QLabel("Recieved Date")
        recieved_date_label.setStyleSheet(label_style)
        form_layout.addRow(recieved_date_label, self.recieved_date_input)

        # Due date input
        self.date_input = QtWidgets.QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QtCore.QDate.currentDate())
        self.date_input.setStyleSheet(input_style)
        date_label = QtWidgets.QLabel("Due Date")
        date_label.setStyleSheet(label_style)
        form_layout.addRow(date_label, self.date_input)

        # Company input
        self.company_input = QtWidgets.QLineEdit()
        self.company_input.setPlaceholderText("Enter Company Name")
        self.company_input.setStyleSheet(input_style)
        company_label = QtWidgets.QLabel("Company")
        company_label.setStyleSheet(label_style)
        form_layout.addRow(company_label, self.company_input)

        # Paid status combo box
        self.paid_status_combo = QtWidgets.QComboBox()
        self.paid_status_combo.addItems(["Yes", "No"])
        self.paid_status_combo.setStyleSheet(input_style)
        status_label = QtWidgets.QLabel("Paid Status")
        status_label.setStyleSheet(label_style)
        form_layout.addRow(status_label, self.paid_status_combo)

        # Amount input
        self.amount_input = QtWidgets.QLineEdit()
        self.amount_input.setPlaceholderText("Enter Amount")
        self.amount_input.setStyleSheet(input_style)
        amount_label = QtWidgets.QLabel("Amount")
        amount_label.setStyleSheet(label_style)
        form_layout.addRow(amount_label, self.amount_input)

        # Amount paid input
        self.amount_paid_input = QtWidgets.QLineEdit()
        self.amount_paid_input.setPlaceholderText("Enter Amount Paid")
        self.amount_paid_input.setStyleSheet(input_style)
        paid_label = QtWidgets.QLabel("Amount Paid")
        paid_label.setStyleSheet(label_style)
        form_layout.addRow(paid_label, self.amount_paid_input)

        # Add form container to main layout
        main_layout.addWidget(form_container)

        # Submit button container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Submit button with modern style
        self.submit_btn = QtWidgets.QPushButton("Submit Invoice")
        self.submit_btn.setFixedHeight(50)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #16a085;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #149174;
            }
            QPushButton:pressed {
                background-color: #117a65;
            }
        """)
        self.submit_btn.clicked.connect(self.submit_invoice)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_btn)
        button_layout.addStretch()

        main_layout.addWidget(button_container)
        main_layout.addStretch()

        # Add shadow effect to the page
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QtGui.QColor(0, 0, 0, 30))
        shadow.setOffset(0, 0)
        page.setGraphicsEffect(shadow)

        self.stackedWidget.addWidget(page)
        return page

    def _create_expense_page(self):
        """Create the expense page with input fields and submit functionality."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section with icon
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title with icon
        title = QtWidgets.QLabel("Enter Expense")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Form container with shadow
        form_container = QtWidgets.QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        form_layout = QtWidgets.QFormLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Input field styling
        input_style = """
            QLineEdit, QDateEdit, QComboBox {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
                min-height: 20px;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QDateEdit::drop-down {
                border: none;
                width: 30px;
            }
        """

        # Label styling
        label_style = """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0;
            }
        """

        # Expense type input
        self.expense_type_input = QtWidgets.QLineEdit()
        self.expense_type_input.setPlaceholderText("Enter Expense Type")
        self.expense_type_input.setStyleSheet(input_style)
        type_label = QtWidgets.QLabel("Expense Type")
        type_label.setStyleSheet(label_style)
        form_layout.addRow(type_label, self.expense_type_input)

        # Expense value input
        self.expense_value_input = QtWidgets.QLineEdit()
        self.expense_value_input.setPlaceholderText("Enter Expense Value")
        self.expense_value_input.setStyleSheet(input_style)
        value_label = QtWidgets.QLabel("Expense Value")
        value_label.setStyleSheet(label_style)
        form_layout.addRow(value_label, self.expense_value_input)

        # Expense date input
        self.expense_date_input = QtWidgets.QDateEdit()
        self.expense_date_input.setCalendarPopup(True)
        self.expense_date_input.setDate(QtCore.QDate.currentDate())
        self.expense_date_input.setStyleSheet(input_style)
        date_label = QtWidgets.QLabel("Expense Date")
        date_label.setStyleSheet(label_style)
        form_layout.addRow(date_label, self.expense_date_input)

        # Add form container to main layout
        main_layout.addWidget(form_container)

        # Submit button container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Submit button with modern style
        self.submit_expense_btn = QtWidgets.QPushButton("Submit Expense")
        self.submit_expense_btn.setFixedHeight(50)
        self.submit_expense_btn.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #a93226;
            }
            QPushButton:pressed {
                background-color: #922b21;
            }
        """)
        self.submit_expense_btn.clicked.connect(self.submit_expense)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_expense_btn)
        button_layout.addStretch()

        main_layout.addWidget(button_container)
        main_layout.addStretch()

        # Add shadow effect to the page
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QtGui.QColor(0, 0, 0, 30))
        shadow.setOffset(0, 0)
        page.setGraphicsEffect(shadow)

        self.stackedWidget.addWidget(page)
        return page

    def _create_merchandise_page(self):
        """Create the merchandise page with input fields and submit functionality."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section with icon
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title with icon
        title = QtWidgets.QLabel("Enter Merchandise")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Form container with shadow
        form_container = QtWidgets.QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        form_layout = QtWidgets.QFormLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Input field styling
        input_style = """
            QLineEdit, QDateEdit, QComboBox {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
                min-height: 20px;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QDateEdit::drop-down {
                border: none;
                width: 30px;
            }
        """

        # Label styling
        label_style = """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0;
            }
        """

        # Merchandise type input
        self.merchandise_type_input = QtWidgets.QLineEdit()
        self.merchandise_type_input.setPlaceholderText("Enter Merchandise Type")
        self.merchandise_type_input.setStyleSheet(input_style)
        type_label = QtWidgets.QLabel("Merchandise Type")
        type_label.setStyleSheet(label_style)
        form_layout.addRow(type_label, self.merchandise_type_input)

        # Quantity input
        self.quantity_input = QtWidgets.QLineEdit()
        self.quantity_input.setPlaceholderText("Enter Quantity")
        self.quantity_input.setStyleSheet(input_style)
        quantity_label = QtWidgets.QLabel("Quantity")
        quantity_label.setStyleSheet(label_style)
        form_layout.addRow(quantity_label, self.quantity_input)

        # Unit price input
        self.unit_price_input = QtWidgets.QLineEdit()
        self.unit_price_input.setPlaceholderText("Enter Unit Price")
        self.unit_price_input.setStyleSheet(input_style)
        price_label = QtWidgets.QLabel("Unit Price")
        price_label.setStyleSheet(label_style)
        form_layout.addRow(price_label, self.unit_price_input)

        # Merchandise date input
        self.merchandise_date_input = QtWidgets.QDateEdit()
        self.merchandise_date_input.setCalendarPopup(True)
        self.merchandise_date_input.setDate(QtCore.QDate.currentDate())
        self.merchandise_date_input.setStyleSheet(input_style)
        date_label = QtWidgets.QLabel("Date")
        date_label.setStyleSheet(label_style)
        form_layout.addRow(date_label, self.merchandise_date_input)

        # Add form container to main layout
        main_layout.addWidget(form_container)

        # Submit button container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Submit button with modern style
        self.submit_merchandise_btn = QtWidgets.QPushButton("Submit Merchandise")
        self.submit_merchandise_btn.setFixedHeight(50)
        self.submit_merchandise_btn.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #7d3c98;
            }
            QPushButton:pressed {
                background-color: #6c3483;
            }
        """)
        self.submit_merchandise_btn.clicked.connect(self.submit_merchandise)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_merchandise_btn)
        button_layout.addStretch()

        main_layout.addWidget(button_container)
        main_layout.addStretch()

        # Add shadow effect to the page
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QtGui.QColor(0, 0, 0, 30))
        shadow.setOffset(0, 0)
        page.setGraphicsEffect(shadow)

        self.stackedWidget.addWidget(page)
        return page

    def _create_employee_history_page(self):
        """Create the employee history page with employee selection and history display."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section with icon
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title with icon
        title = QtWidgets.QLabel("Employee History")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Controls container
        controls_container = QtWidgets.QWidget()
        controls_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
        """)
        controls_layout = QtWidgets.QHBoxLayout(controls_container)
        controls_layout.setSpacing(20)

        # Employee selection
        self.employee_combo = QtWidgets.QComboBox()
        self.employee_combo.setFixedWidth(250)
        self.employee_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
            }
            QComboBox:hover {
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        self.populate_employee_combo()
        controls_layout.addWidget(self.employee_combo)

        # Week navigation
        week_nav_container = QtWidgets.QWidget()
        week_nav_layout = QtWidgets.QHBoxLayout(week_nav_container)
        week_nav_layout.setSpacing(10)

        self.prev_week_btn = QtWidgets.QPushButton("←")
        self.prev_week_btn.setFixedSize(40, 40)
        self.prev_week_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.week_label = QtWidgets.QLabel()
        self.week_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.week_label.setAlignment(QtCore.Qt.AlignCenter)

        self.next_week_btn = QtWidgets.QPushButton("→")
        self.next_week_btn.setFixedSize(40, 40)
        self.next_week_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        week_nav_layout.addWidget(self.prev_week_btn)
        week_nav_layout.addWidget(self.week_label)
        week_nav_layout.addWidget(self.next_week_btn)
        controls_layout.addWidget(week_nav_container)

        # Calendar button
        self.calendar_btn = QtWidgets.QPushButton("Select Date")
        self.calendar_btn.setFixedHeight(40)
        self.calendar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        controls_layout.addWidget(self.calendar_btn)

        main_layout.addWidget(controls_container)

        # History table
        self.history_table = QtWidgets.QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Date", "Clock In", "Clock Out", "Register In", "Register Out", "Duration"
        ])
        self.history_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
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
        self.history_table.setAlternatingRowColors(True)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self._set_row_height(self.history_table, 44)
        # Enable editing for all columns except duration
        self.history_table.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked | 
                                         QtWidgets.QAbstractItemView.EditKeyPressed)
        
        # Connect cell changed signal
        self.history_table.cellChanged.connect(self.on_cell_changed)
        
        main_layout.addWidget(self.history_table)
        
        # Submit changes button (initially hidden)
        self.submit_changes_btn = QtWidgets.QPushButton("Submit Changes")
        self.submit_changes_btn.setFixedHeight(50)
        self.submit_changes_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
        """)
        self.submit_changes_btn.clicked.connect(self.submit_changes)
        self.submit_changes_btn.hide()
        main_layout.addWidget(self.submit_changes_btn, alignment=QtCore.Qt.AlignRight)

        # Initialize current week
        self.current_week_start = self.get_week_start_date()
        self.update_week_label()
        
        # Connect signals
        self.employee_combo.currentIndexChanged.connect(self.load_employee_history)
        self.prev_week_btn.clicked.connect(self.previous_week)
        self.next_week_btn.clicked.connect(self.next_week)
        self.calendar_btn.clicked.connect(self.show_calendar)

        # Add shadow effect to the page
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QtGui.QColor(0, 0, 0, 30))
        shadow.setOffset(0, 0)
        page.setGraphicsEffect(shadow)

        self.stackedWidget.addWidget(page)
        return page

    def populate_employee_combo(self):
        """Populate the employee combo box with employee names."""
        try:
            query = "SELECT employee_id, firstName, lastName FROM employee WHERE role = 'employee'"
            results = connect(query, None)
            
            if results:
                self.employee_combo.clear()
                for employee in results:
                    self.employee_combo.addItem(
                        f"{employee[1]} {employee[2]}",
                        employee[0]  # Store employee_id as userData
                    )
        except Exception as e:
            print(f"Error populating employee combo: {e}")

    def get_week_start_date(self):
        """Get the start date of the current week (Monday)."""
        today = QtCore.QDate.currentDate()
        return today.addDays(-today.dayOfWeek() + 1)  # Adjust to Monday

    def update_week_label(self):
        """Update the week label with the current week range."""
        week_end = self.current_week_start.addDays(6)
        self.week_label.setText(
            f"{self.current_week_start.toString('MMM d')} - {week_end.toString('MMM d, yyyy')}"
        )
        self.load_employee_history()

    def previous_week(self):
        """Navigate to the previous week."""
        self.current_week_start = self.current_week_start.addDays(-7)
        self.update_week_label()

    def next_week(self):
        """Navigate to the next week."""
        self.current_week_start = self.current_week_start.addDays(7)
        self.update_week_label()

    def show_calendar(self):
        """Show calendar dialog to select a date."""
        calendar = QtWidgets.QCalendarWidget()
        calendar.setSelectedDate(self.current_week_start)
        
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select Date")
        dialog.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(calendar)
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_date = calendar.selectedDate()
            self.current_week_start = selected_date.addDays(-selected_date.dayOfWeek() + 1)
            self.update_week_label()

    def load_employee_history(self):
        """Load the selected employee's history for the current week."""
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            return

        try:
            week_end = self.current_week_start.addDays(6)
            
            query = """
                SELECT 
                    DATE(clock_in) as date,
                    TIME(clock_in) as clock_in_time,
                    TIME(clock_out) as clock_out_time,
                    reg_in,
                    reg_out
                FROM clockTable
                WHERE employee_id = %s 
                AND DATE(clock_in) BETWEEN %s AND %s
                ORDER BY clock_in
            """
            data = (
                employee_id,
                self.current_week_start.toPyDate(),
                week_end.toPyDate()
            )
            
            results = connect(query, data)
            
            # Clear existing table data
            self.history_table.setRowCount(0)
            
            if results:
                for row_data in results:
                    row = self.history_table.rowCount()
                    self.history_table.insertRow(row)
                    
                    # Format date
                    date = row_data[0].strftime("%Y-%m-%d")
                    
                    # Format times (handle timedelta objects)
                    def format_timedelta(td):
                        if td is None:
                            return "-"
                        total_seconds = int(td.total_seconds())
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        seconds = total_seconds % 60
                        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                    
                    clock_in = format_timedelta(row_data[1])
                    clock_out = format_timedelta(row_data[2])
                    
                    # Calculate duration
                    def calculate_duration(clock_in_td, clock_out_td):
                        if clock_in_td is None or clock_out_td is None:
                            return "-"
                        duration_seconds = int((clock_out_td - clock_in_td).total_seconds())
                        if duration_seconds < 0:
                            return "-"
                        hours = duration_seconds // 3600
                        minutes = (duration_seconds % 3600) // 60
                        return f"{hours}h {minutes}m"
                    
                    duration = calculate_duration(row_data[1], row_data[2])
                    
                    # Format register amounts
                    reg_in = f"${float(row_data[3]):.2f}" if row_data[3] is not None else "-"
                    reg_out = f"${float(row_data[4]):.2f}" if row_data[4] is not None else "-"
                    
                    # Add items to table
                    self.history_table.setItem(row, 0, QtWidgets.QTableWidgetItem(date))
                    self.history_table.setItem(row, 1, QtWidgets.QTableWidgetItem(clock_in))
                    self.history_table.setItem(row, 2, QtWidgets.QTableWidgetItem(clock_out))
                    self.history_table.setItem(row, 3, QtWidgets.QTableWidgetItem(reg_in))
                    self.history_table.setItem(row, 4, QtWidgets.QTableWidgetItem(reg_out))
                    self.history_table.setItem(row, 5, QtWidgets.QTableWidgetItem(duration))
                    
                    # Center align all items
                    for col in range(6):
                        self.history_table.item(row, col).setTextAlignment(QtCore.Qt.AlignCenter)
            
            # Resize columns to fit content
            self.history_table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error loading employee history: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load employee history: {e}")

    def on_cell_changed(self, row, column):
        """Handle cell changes in the history table."""
        # Don't show submit button if duration column was changed
        if column == 5:  # Duration column
            return
            
        # Show the submit button
        self.submit_changes_btn.show()
        
        # Store the changed data
        if not hasattr(self, 'changed_cells'):
            self.changed_cells = []
            
        # Check if this cell is already in the list
        for cell in self.changed_cells:
            if cell['row'] == row and cell['column'] == column:
                # Update the value
                cell['new_value'] = self.history_table.item(row, column).text()
                return
                
        # Add new changed cell
        self.changed_cells.append({
            'row': row,
            'column': column,
            'old_value': self.history_table.item(row, column).text(),
            'new_value': self.history_table.item(row, column).text()
        })

    def submit_changes(self):
        """Submit all changes to the database."""
        from decimal import Decimal
        if not hasattr(self, 'changed_cells') or not self.changed_cells:
            return
            
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            return
            
        try:
            # Get employee's hourly rate and bonus percentage
            emp_query = "SELECT bonus_percentage, hourlyRate FROM employee WHERE employee_id = %s"
            emp_result = connect(emp_query, (employee_id,))
            if not emp_result:
                raise Exception("Could not find employee information")
            
            bonus_percentage = Decimal(str(emp_result[0][0])).quantize(Decimal('0.01'))
            hourly_rate = Decimal(str(emp_result[0][1])).quantize(Decimal('0.01'))
            
            # Get unique dates and times from changed cells
            changed_records = {}
            for cell in self.changed_cells:
                date = self.history_table.item(cell['row'], 0).text()
                clock_in = self.history_table.item(cell['row'], 1).text()
                if date not in changed_records:
                    changed_records[date] = {}
                if clock_in not in changed_records[date]:
                    changed_records[date][clock_in] = {}
                changed_records[date][clock_in][cell['column']] = cell['new_value']
            
            # For each changed record, get the complete record
            for date, times in changed_records.items():
                for clock_in_time, changes in times.items():
                    # Get the original record
                    query = """
                        SELECT * FROM clockTable 
                        WHERE employee_id = %s 
                        AND DATE(clock_in) = %s 
                        AND TIME(clock_in) = %s
                    """
                    data = (employee_id, date, clock_in_time)
                    results = connect(query, data)
                    
                    if not results:
                        raise Exception(f"No record found for date {date} and time {clock_in_time}")
                    
                    # Get the original record
                    original_record = results[0]
                    store_id = original_record[2]  # store_id from clockTable
                    
                    # Create a new record with updated values
                    new_record = list(original_record)
                    
                    # Update values from the table
                    for column, new_value in changes.items():
                        if column == 1:  # Clock In
                            new_record[3] = f"{date} {new_value}"  # Combine date and time
                        elif column == 2:  # Clock Out
                            new_record[4] = f"{date} {new_value}"  # Combine date and time
                        elif column == 3:  # Register In
                            new_record[5] = float(new_value.replace('$', ''))
                        elif column == 4:  # Register Out
                            new_record[6] = float(new_value.replace('$', ''))
                    
                    # Calculate updated payroll values
                    clock_in_dt = new_record[3] if isinstance(new_record[3], datetime) else datetime.strptime(new_record[3], "%Y-%m-%d %H:%M:%S")
                    clock_out_dt = new_record[4] if isinstance(new_record[4], datetime) else datetime.strptime(new_record[4], "%Y-%m-%d %H:%M:%S") if new_record[4] else None
                    reg_in = Decimal(str(new_record[5])).quantize(Decimal('0.01'))
                    reg_out = Decimal(str(new_record[6])).quantize(Decimal('0.01')) if new_record[6] is not None else reg_in
                    
                    if clock_out_dt:
                        # Calculate hours worked and wages
                        time_diff = clock_out_dt - clock_in_dt
                        hours_worked = Decimal(str(time_diff.total_seconds() / 3600)).quantize(Decimal('0.01'))
                        wages = (hours_worked * hourly_rate).quantize(Decimal('0.01'))
                        register_diff = (reg_out - reg_in).quantize(Decimal('0.01'))
                        bonus = Decimal('0') if register_diff <= 0 else (register_diff * (bonus_percentage / Decimal('100'))).quantize(Decimal('0.01'))
                        
                        # Update or create payroll record
                        payroll_check_query = """
                            SELECT payroll_id, bonuses, wages 
                            FROM Payroll 
                            WHERE DATE(date) = %s 
                            AND store_id = %s
                        """
                        payroll_check_data = (date, store_id)
                        payroll_result = connect(payroll_check_query, payroll_check_data)
                        
                        if payroll_result:
                            # Get the original clock record to subtract old values
                            old_clock_query = """
                                SELECT 
                                    TIMESTAMPDIFF(SECOND, clock_in, clock_out) / 3600 as hours,
                                    reg_in,
                                    reg_out
                                FROM clockTable 
                                WHERE employee_id = %s 
                                AND DATE(clock_in) = %s 
                                AND TIME(clock_in) = %s
                            """
                            old_clock_data = (employee_id, date, clock_in_time)
                            old_clock_result = connect(old_clock_query, old_clock_data)
                            
                            if old_clock_result:
                                old_hours = Decimal(str(old_clock_result[0][0])).quantize(Decimal('0.01'))
                                old_reg_in = Decimal(str(old_clock_result[0][1])).quantize(Decimal('0.01'))
                                old_reg_out = Decimal(str(old_clock_result[0][2])).quantize(Decimal('0.01')) if old_clock_result[0][2] is not None else old_reg_in
                                
                                old_wages = (old_hours * hourly_rate).quantize(Decimal('0.01'))
                                old_register_diff = (old_reg_out - old_reg_in).quantize(Decimal('0.01'))
                                old_bonus = Decimal('0') if old_register_diff <= 0 else (old_register_diff * (bonus_percentage / Decimal('100'))).quantize(Decimal('0.01'))
                                
                                # Update payroll by removing old values and adding new ones
                                payroll_update_query = """
                                    UPDATE Payroll 
                                    SET bonuses = bonuses - %s + %s,
                                        wages = wages - %s + %s
                                    WHERE payroll_id = %s
                                """
                                payroll_update_data = (
                                    str(old_bonus), str(bonus),
                                    str(old_wages), str(wages),
                                    payroll_result[0][0]
                                )
                                connect(payroll_update_query, payroll_update_data)
                        else:
                            # Create new payroll record
                            payroll_insert_query = """
                                INSERT INTO Payroll (date, bonuses, wages, store_id)
                                VALUES (%s, %s, %s, %s)
                            """
                            payroll_insert_data = (date, str(bonus), str(wages), store_id)
                            connect(payroll_insert_query, payroll_insert_data)
                    
                    # Delete the old record
                    delete_query = """
                        DELETE FROM clockTable 
                        WHERE employee_id = %s 
                        AND DATE(clock_in) = %s 
                        AND TIME(clock_in) = %s
                    """
                    delete_data = (employee_id, date, clock_in_time)
                    delete_success = connect(delete_query, delete_data)
                    
                    if not delete_success:
                        raise Exception(f"Failed to delete record for date {date} and time {clock_in_time}")
                    
                    # Insert the new record
                    insert_query = """
                        INSERT INTO clockTable 
                        (employee_id, store_id, clock_in, clock_out, reg_in, reg_out)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    insert_data = (
                        new_record[1],  # employee_id
                        new_record[2],  # store_id
                        new_record[3],  # clock_in (now with full datetime)
                        new_record[4],  # clock_out (now with full datetime)
                        new_record[5],  # reg_in
                        new_record[6]   # reg_out
                    )
                    insert_success = connect(insert_query, insert_data)
                    
                    if not insert_success:
                        raise Exception(f"Failed to insert new record for date {date} and time {clock_in_time}")
            
            # Show success message
            QtWidgets.QMessageBox.information(None, "Success", "Changes submitted successfully.")
            
            # Clear changed cells and hide submit button
            self.changed_cells = []
            self.submit_changes_btn.hide()
            
            # Reload the history to show updated values
            self.load_employee_history()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to submit changes: {e}")
            # Revert changes in the table
            for cell in self.changed_cells:
                self.history_table.item(cell['row'], cell['column']).setText(cell['old_value'])
            self.changed_cells = []
            self.submit_changes_btn.hide()

    def submit_invoice(self):
        """Handle the invoice submission."""
        print("Attempting to submit invoice...")
        
        if not self.store_id:
            QtWidgets.QMessageBox.critical(None, "Error", "Store ID is missing. Please select a store.")
            print("Error: Store ID is missing")
            return
        
        # Validate inputs
        try:
            invoice_id = int(self.invoice_id_input.text())
            recievedDate = self.recieved_date_input.date().toPyDate()  
            dueDate = self.date_input.date().toPyDate()
            company = self.company_input.text().strip()
            paid_status = "paid" if self.paid_status_combo.currentText() == "Yes" else "unpaid"
            amount = float(self.amount_input.text())
            amount_paid = float(self.amount_paid_input.text()) if self.amount_paid_input.text() else 0.0

            if not company:
                raise ValueError("Company name cannot be empty")
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            if amount_paid < 0:
                raise ValueError("Amount paid cannot be negative")
            if amount_paid > amount:
                raise ValueError("Amount paid cannot be greater than total amount")

        except ValueError as e:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", str(e))
            print(f"Input validation error: {e}")
            return

        # Insert into database
        try:
            query = """
                INSERT INTO Invoice 
                (invoice_id, company_name, amount, amount_paid, recieved_date, due_date, paid_status, payment_date, store_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                invoice_id,
                company,
                amount,
                amount_paid,
                recievedDate,
                dueDate,
                paid_status,
                dueDate if paid_status == "paid" else None,
                self.store_id
            )
            print(f"Inserting invoice record. Query: {query}, Data: {data}")
            success = connect(query, data)
            print(f"Invoice insert result: {success}")

            if success:
                QtWidgets.QMessageBox.information(None, "Success", "Invoice submitted successfully.")
                # Clear input fields
                self.invoice_id_input.clear()
                self.recieved_date_input.setDate(QtCore.QDate.currentDate())  # Reset received date
                self.date_input.setDate(QtCore.QDate.currentDate())
                self.company_input.clear()
                self.paid_status_combo.setCurrentIndex(0)
                self.amount_input.clear()
                self.amount_paid_input.clear()
                print("Invoice submission successful")
            else:
                QtWidgets.QMessageBox.critical(None, "Error", "Failed to submit invoice.")
                print("Error: Invoice insert failed")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to submit invoice: {e}")
            print(f"Error during invoice submission: {e}")

    def submit_expense(self):
        """Handle the expense submission."""
        print("Attempting to submit expense...")
        
        if not self.store_id:
            QtWidgets.QMessageBox.critical(None, "Error", "Store ID is missing. Please select a store.")
            print("Error: Store ID is missing")
            return
        
        # Validate inputs
        try:
            expense_type = self.expense_type_input.text().strip()
            expense_value = float(self.expense_value_input.text())
            expense_date = self.expense_date_input.date().toPyDate()

            if not expense_type:
                raise ValueError("Expense type cannot be empty")
            if expense_value <= 0:
                raise ValueError("Expense value must be greater than 0")

        except ValueError as e:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", str(e))
            print(f"Input validation error: {e}")
            return

        # Insert into database
        try:
            query = """
                INSERT INTO expenses 
                (expense_type, expense_date, employee_id, store_id, expense_value)
                VALUES (%s, %s, %s, %s, %s)
            """
            data = (
                expense_type,
                expense_date,
                self.employee_id,
                self.store_id,
                expense_value
            )
            print(f"Inserting expense record. Query: {query}, Data: {data}")
            success = connect(query, data)
            print(f"Expense insert result: {success}")

            if success:
                QtWidgets.QMessageBox.information(None, "Success", "Expense submitted successfully.")
                # Clear input fields
                self.expense_type_input.clear()
                self.expense_value_input.clear()
                self.expense_date_input.setDate(QtCore.QDate.currentDate())
                print("Expense submission successful")
            else:
                QtWidgets.QMessageBox.critical(None, "Error", "Failed to submit expense.")
                print("Error: Expense insert failed")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to submit expense: {e}")
            print(f"Error during expense submission: {e}")

    def submit_merchandise(self):
        """Handle the merchandise submission."""
        print("Attempting to submit merchandise...")
        
        if not self.store_id:
            QtWidgets.QMessageBox.critical(None, "Error", "Store ID is missing. Please select a store.")
            print("Error: Store ID is missing")
            return

        # Validate inputs
        try:
            merchandise_type = self.merchandise_type_input.text().strip()
            quantity = int(self.quantity_input.text())
            unit_price = float(self.unit_price_input.text())
            merchandise_date = self.merchandise_date_input.date().toPyDate()

            if not merchandise_type:
                raise ValueError("Merchandise type cannot be empty")
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0")
            if unit_price <= 0:
                raise ValueError("Unit price must be greater than 0")

        except ValueError as e:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", str(e))
            print(f"Input validation error: {e}")
            return

        # Insert into database
        try:
            query = """
                INSERT INTO merchandise 
                (merchandise_type, merchandise_date, quantity, unitPrice, employee_id, store_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = (
                merchandise_type,
                merchandise_date,
                quantity,
                unit_price,
                self.employee_id,
                self.store_id
            )
            print(f"Inserting merchandise record. Query: {query}, Data: {data}")
            success = connect(query, data)
            print(f"Merchandise insert result: {success}")

            if success:
                QtWidgets.QMessageBox.information(None, "Success", "Merchandise submitted successfully.")
                # Clear input fields
                self.merchandise_type_input.clear()
                self.quantity_input.clear()
                self.unit_price_input.clear()
                self.merchandise_date_input.setDate(QtCore.QDate.currentDate())
                print("Merchandise submission successful")
            else:
                QtWidgets.QMessageBox.critical(None, "Error", "Failed to submit merchandise.")
                print("Error: Merchandise insert failed")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to submit merchandise: {e}")
            print(f"Error during merchandise submission: {e}")

    def sign_out(self):
        """Handle the sign-out operation."""
        self.employee_id = None
        self.store_id = None
        
        # Redirect to login screen immediately
        self.stacked_widget.setCurrentIndex(0)
        
        # Clear UI elements after redirection
        QtCore.QTimer.singleShot(100, self._clear_ui)
    
    def _clear_ui(self):
        """Clear UI elements after redirection."""
        self.owner_name_label.setText("Owner Name")
        self.store_name_label.setText("Store Name")
        self.store_combo.clear()

    def _add_placeholder_page(self, title_text: str) -> QtWidgets.QWidget:
        """Adds a simple centered title label page to the stackedWidget."""
        page = QtWidgets.QWidget()
        page.setObjectName(title_text.replace(" ", "_"))
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)

        title = QtWidgets.QLabel(title_text)
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet(
            """font-size: 26px; font-weight: bold; color: #2c3e50;"""
        )
        page_layout.addStretch()
        page_layout.addWidget(title)
        page_layout.addStretch()

        self.stackedWidget.addWidget(page)
        return page

    def _create_expenses_history_page(self):
        """Create the expenses history page with comprehensive view."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section with icon
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title with icon
        title = QtWidgets.QLabel("Expenses History")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Controls container
        controls_container = QtWidgets.QWidget()
        controls_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
        """)
        controls_layout = QtWidgets.QHBoxLayout(controls_container)
        controls_layout.setSpacing(20)

        # Store selector
        self.expenses_store_combo = QtWidgets.QComboBox()
        self.expenses_store_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
                min-width: 200px;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
        """)
        controls_layout.addWidget(self.expenses_store_combo)

        # View toggle button
        self.expenses_view_toggle = QtWidgets.QPushButton("Weekly View")
        self.expenses_view_toggle.setFixedHeight(40)
        self.expenses_view_toggle.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.expenses_view_toggle.clicked.connect(self.toggle_expenses_view)
        controls_layout.addWidget(self.expenses_view_toggle)

        # Week/Month navigation
        week_nav_container = QtWidgets.QWidget()
        week_nav_layout = QtWidgets.QHBoxLayout(week_nav_container)
        week_nav_layout.setSpacing(10)

        self.expenses_prev_week_btn = QtWidgets.QPushButton("←")
        self.expenses_prev_week_btn.setFixedSize(40, 40)
        self.expenses_prev_week_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.expenses_week_label = QtWidgets.QLabel()
        self.expenses_week_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.expenses_week_label.setAlignment(QtCore.Qt.AlignCenter)

        self.expenses_next_week_btn = QtWidgets.QPushButton("→")
        self.expenses_next_week_btn.setFixedSize(40, 40)
        self.expenses_next_week_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        week_nav_layout.addWidget(self.expenses_prev_week_btn)
        week_nav_layout.addWidget(self.expenses_week_label)
        week_nav_layout.addWidget(self.expenses_next_week_btn)
        controls_layout.addWidget(week_nav_container)

        # Calendar button
        self.expenses_calendar_btn = QtWidgets.QPushButton("Select Date")
        self.expenses_calendar_btn.setFixedHeight(40)
        self.expenses_calendar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        controls_layout.addWidget(self.expenses_calendar_btn)

        # Refresh button
        self.expenses_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.expenses_refresh_btn.setFixedHeight(40)
        self.expenses_refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        controls_layout.addWidget(self.expenses_refresh_btn)

        main_layout.addWidget(controls_container)

        # Expenses table
        self.expenses_table = QtWidgets.QTableWidget()
        self.expenses_table.setColumnCount(7)
        self.expenses_table.setHorizontalHeaderLabels([
            "Date", "Type", "Amount", "Employee", "Store", "Actions", "ID"
        ])
        self.expenses_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
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
        self.expenses_table.setAlternatingRowColors(True)
        self.expenses_table.horizontalHeader().setStretchLastSection(True)
        self._set_row_height(self.expenses_table, 44)
        main_layout.addWidget(self.expenses_table)

        # Total expenses label
        self.expenses_total_label = QtWidgets.QLabel()
        self.expenses_total_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.expenses_total_label, alignment=QtCore.Qt.AlignRight)

        # Initialize current date and view mode
        self.expenses_current_date = QtCore.QDate.currentDate()
        self.is_expenses_weekly_view = True
        
        # Connect signals
        self.expenses_store_combo.currentIndexChanged.connect(self.load_expenses_history)
        self.expenses_prev_week_btn.clicked.connect(self.expenses_previous_period)
        self.expenses_next_week_btn.clicked.connect(self.expenses_next_period)
        self.expenses_calendar_btn.clicked.connect(self.expenses_show_calendar)
        self.expenses_refresh_btn.clicked.connect(self.load_expenses_history)

        # Initialize the page
        self.populate_expenses_stores()
        self.update_expenses_period_label()

        self.stackedWidget.addWidget(page)
        return page

    def toggle_expenses_view(self):
        """Toggle between weekly and monthly expenses view."""
        self.is_expenses_weekly_view = not self.is_expenses_weekly_view
        self.expenses_view_toggle.setText("Weekly View" if self.is_expenses_weekly_view else "Monthly View")
        self.update_expenses_period_label()

    def update_expenses_period_label(self):
        """Update the expenses period label based on the current view mode."""
        if self.is_expenses_weekly_view:
            week_start = self.expenses_current_date.addDays(-self.expenses_current_date.dayOfWeek() + 1)
            week_end = week_start.addDays(6)
            self.expenses_week_label.setText(
                f"{week_start.toString('MMM d')} - {week_end.toString('MMM d, yyyy')}"
            )
        else:
            self.expenses_week_label.setText(self.expenses_current_date.toString('MMMM yyyy'))
        self.load_expenses_history()

    def expenses_previous_period(self):
        """Navigate to the previous period (week or month) in expenses view."""
        if self.is_expenses_weekly_view:
            self.expenses_current_date = self.expenses_current_date.addDays(-7)
        else:
            self.expenses_current_date = self.expenses_current_date.addMonths(-1)
        self.update_expenses_period_label()

    def expenses_next_period(self):
        """Navigate to the next period (week or month) in expenses view."""
        if self.is_expenses_weekly_view:
            self.expenses_current_date = self.expenses_current_date.addDays(7)
        else:
            self.expenses_current_date = self.expenses_current_date.addMonths(1)
        self.update_expenses_period_label()

    def expenses_show_calendar(self):
        """Show calendar dialog to select a date for expenses view."""
        calendar = QtWidgets.QCalendarWidget()
        calendar.setSelectedDate(self.expenses_current_date)
        
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select Date")
        dialog.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(calendar)
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.expenses_current_date = calendar.selectedDate()
            self.update_expenses_period_label()

    def load_expenses_history(self):
        """Load the expenses history for the selected store and period."""
        store_id = self.expenses_store_combo.currentData()
        if store_id is None:
            return

        try:
            # Calculate start and end dates based on view mode
            if self.is_expenses_weekly_view:
                start_date = self.expenses_current_date.addDays(-self.expenses_current_date.dayOfWeek() + 1)
                end_date = start_date.addDays(6)
            else:
                start_date = QtCore.QDate(self.expenses_current_date.year(), self.expenses_current_date.month(), 1)
                end_date = start_date.addMonths(1).addDays(-1)
            
            # Modify query based on store selection
            if store_id == -1:  # All Stores
                query = """
                    SELECT 
                        e.expense_id,
                        e.expense_date,
                        e.expense_type,
                        e.expense_value,
                        CONCAT(emp.firstName, ' ', emp.lastName) as employee_name,
                        s.store_name
                    FROM expenses e
                    JOIN employee emp ON e.employee_id = emp.employee_id
                    JOIN Store s ON e.store_id = s.store_id
                    WHERE e.expense_date BETWEEN %s AND %s
                    ORDER BY e.expense_date DESC
                """
                data = (
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            else:
                query = """
                    SELECT 
                        e.expense_id,
                        e.expense_date,
                        e.expense_type,
                        e.expense_value,
                        CONCAT(emp.firstName, ' ', emp.lastName) as employee_name,
                        s.store_name
                    FROM expenses e
                    JOIN employee emp ON e.employee_id = emp.employee_id
                    JOIN Store s ON e.store_id = s.store_id
                    WHERE e.store_id = %s 
                    AND e.expense_date BETWEEN %s AND %s
                    ORDER BY e.expense_date DESC
                """
                data = (
                    store_id,
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )

            print(f"Executing query with data: {data}")
            results = connect(query, data)

            # Clear existing table data
            self.expenses_table.setRowCount(0)
            total_expenses = 0.0

            if results:
                print(f"Found {len(results)} expense records")
                for row_data in results:
                    row = self.expenses_table.rowCount()
                    self.expenses_table.insertRow(row)

                    # Store expense ID in the hidden last column
                    id_item = QtWidgets.QTableWidgetItem(str(row_data[0]))
                    self.expenses_table.setItem(row, 6, id_item)
                    
                    # Date
                    date_item = QtWidgets.QTableWidgetItem(str(row_data[1]))
                    date_item.setFlags(date_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.expenses_table.setItem(row, 0, date_item)
                    
                    # Type
                    type_item = QtWidgets.QTableWidgetItem(row_data[2])
                    self.expenses_table.setItem(row, 1, type_item)
                    
                    # Amount
                    amount = float(row_data[3])
                    total_expenses += amount
                    amount_item = QtWidgets.QTableWidgetItem(f"${amount:.2f}")
                    self.expenses_table.setItem(row, 2, amount_item)
                    
                    # Employee
                    employee_item = QtWidgets.QTableWidgetItem(row_data[4])
                    employee_item.setFlags(employee_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.expenses_table.setItem(row, 3, employee_item)
                    
                    # Store
                    store_item = QtWidgets.QTableWidgetItem(row_data[5])
                    store_item.setFlags(store_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.expenses_table.setItem(row, 4, store_item)
                    
                    # Actions
                    actions_widget = QtWidgets.QWidget()
                    actions_layout = QtWidgets.QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(5, 2, 5, 2)
                    actions_layout.setSpacing(8)
                    
                    edit_btn = QtWidgets.QPushButton("Edit")
                    edit_btn.setMinimumSize(70, 28)
                    edit_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #3498db;
                            color: white;
                            border: none;
                            border-radius: 6px;
                            padding: 6px;
                            font-size: 13px;
                            font-weight: bold;
                            min-width: 80px;
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
                        QPushButton:pressed {
                            background-color: #1c6ea4;
                        }
                    """)
                    edit_btn.clicked.connect(lambda checked, r=row: self.edit_expense(r))
                    
                    delete_btn = QtWidgets.QPushButton("Delete")
                    delete_btn.setMinimumSize(85, 32)
                    delete_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #e74c3c;
                            color: white;
                            border: none;
                            border-radius: 6px;
                            padding: 6px;
                            font-size: 13px;
                            font-weight: bold;
                            min-width: 80px;
                        }
                        QPushButton:hover {
                            background-color: #c0392b;
                        }
                        QPushButton:pressed {
                            background-color: #a93226;
                        }
                    """)
                    delete_btn.clicked.connect(lambda checked, r=row: self.delete_expense(r))
                    
                    actions_layout.addWidget(edit_btn)
                    actions_layout.addWidget(delete_btn)
                    
                    self.expenses_table.setCellWidget(row, 5, actions_widget)

                # Hide the ID column
                self.expenses_table.setColumnHidden(6, True)
                
                # Update total expenses label
                period_type = "Weekly" if self.is_expenses_weekly_view else "Monthly"
                self.expenses_total_label.setText(f"Total {period_type} Expenses: ${total_expenses:.2f}")
                
                # Resize columns to fit content
                self.expenses_table.resizeColumnsToContents()
            else:
                print("No expense records found")
                period_type = "Weekly" if self.is_expenses_weekly_view else "Monthly"
                self.expenses_total_label.setText(f"Total {period_type} Expenses: $0.00")
                
        except Exception as e:
            print(f"Error loading expenses history: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load expenses history: {e}")

    def edit_expense(self, row):
        """Edit an expense record."""
        try:
            expense_id = int(self.expenses_table.item(row, 6).text())
            
            # Create edit dialog
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Edit Expense")
            dialog.setFixedWidth(400)
            
            layout = QtWidgets.QFormLayout(dialog)
            
            # Input styling
            input_style = """
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #e0e0e0;
                    border-radius: 6px;
                    font-size: 14px;
                }
            """
            
            # Create input fields
            type_input = QtWidgets.QLineEdit(self.expenses_table.item(row, 1).text())
            type_input.setStyleSheet(input_style)
            
            amount_input = QtWidgets.QLineEdit(self.expenses_table.item(row, 2).text().replace('$', ''))
            amount_input.setStyleSheet(input_style)
            
            # Add fields to layout
            layout.addRow("Type:", type_input)
            layout.addRow("Amount:", amount_input)
            
            # Add buttons
            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)
            
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                try:
                    # Validate inputs
                    expense_type = type_input.text().strip()
                    amount = float(amount_input.text())
                    
                    if not expense_type:
                        raise ValueError("Expense type cannot be empty")
                    if amount <= 0:
                        raise ValueError("Amount must be greater than 0")
                    
                    # Update expense in database
                    query = """
                        UPDATE expenses 
                        SET expense_type = %s,
                            expense_value = %s
                        WHERE expense_id = %s
                    """
                    data = (expense_type, amount, expense_id)
                    success = connect(query, data)
                    
                    if success:
                        QtWidgets.QMessageBox.information(None, "Success", "Expense updated successfully")
                        self.load_expenses_history()
                    else:
                        raise Exception("Failed to update expense")
                        
                except ValueError as ve:
                    QtWidgets.QMessageBox.critical(None, "Error", str(ve))
                    
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to edit expense: {e}")

    def delete_expense(self, row):
        """Delete an expense record."""
        try:
            expense_id = int(self.expenses_table.item(row, 6).text())
            
            reply = QtWidgets.QMessageBox.question(
                None,
                "Confirm Delete",
                "Are you sure you want to delete this expense?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                query = "DELETE FROM expenses WHERE expense_id = %s"
                success = connect(query, (expense_id,))
                
                if success:
                    QtWidgets.QMessageBox.information(None, "Success", "Expense deleted successfully")
                    self.load_expenses_history()
                else:
                    raise Exception("Failed to delete expense")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to delete expense: {e}")

    def _create_merchandise_history_page(self):
        """Create the merchandise history page with editable table."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section with icon
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title with icon
        title = QtWidgets.QLabel("Merchandise History")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Controls container
        controls_container = QtWidgets.QWidget()
        controls_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
        """)
        controls_layout = QtWidgets.QHBoxLayout(controls_container)
        controls_layout.setSpacing(20)

        # Store selector
        self.merchandise_store_combo = QtWidgets.QComboBox()
        self.merchandise_store_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
                min-width: 200px;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
        """)
        controls_layout.addWidget(self.merchandise_store_combo)

        # View toggle button
        self.merchandise_view_toggle = QtWidgets.QPushButton("Weekly View")
        self.merchandise_view_toggle.setFixedHeight(40)
        self.merchandise_view_toggle.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.merchandise_view_toggle.clicked.connect(self.toggle_merchandise_view)
        controls_layout.addWidget(self.merchandise_view_toggle)

        # Week/Month navigation
        nav_container = QtWidgets.QWidget()
        nav_layout = QtWidgets.QHBoxLayout(nav_container)
        nav_layout.setSpacing(10)

        self.merchandise_prev_btn = QtWidgets.QPushButton("←")
        self.merchandise_prev_btn.setFixedSize(40, 40)
        self.merchandise_prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.merchandise_period_label = QtWidgets.QLabel()
        self.merchandise_period_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.merchandise_period_label.setAlignment(QtCore.Qt.AlignCenter)

        self.merchandise_next_btn = QtWidgets.QPushButton("→")
        self.merchandise_next_btn.setFixedSize(40, 40)
        self.merchandise_next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        nav_layout.addWidget(self.merchandise_prev_btn)
        nav_layout.addWidget(self.merchandise_period_label)
        nav_layout.addWidget(self.merchandise_next_btn)
        controls_layout.addWidget(nav_container)

        # Calendar button
        self.merchandise_calendar_btn = QtWidgets.QPushButton("Select Date")
        self.merchandise_calendar_btn.setFixedHeight(40)
        self.merchandise_calendar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        controls_layout.addWidget(self.merchandise_calendar_btn)

        # Refresh button
        self.merchandise_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.merchandise_refresh_btn.setFixedHeight(40)
        self.merchandise_refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        controls_layout.addWidget(self.merchandise_refresh_btn)

        # Submit changes button
        self.merchandise_submit_btn = QtWidgets.QPushButton("Submit Changes")
        self.merchandise_submit_btn.setFixedHeight(40)
        self.merchandise_submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        controls_layout.addWidget(self.merchandise_submit_btn)

        main_layout.addWidget(controls_container)

        # Merchandise table
        self.merchandise_table = QtWidgets.QTableWidget()
        self.merchandise_table.setColumnCount(7)
        self.merchandise_table.setHorizontalHeaderLabels([
            "ID", "Date", "Type", "Quantity", "Unit Price", "Total", "Employee"
        ])
        self.merchandise_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
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
        self.merchandise_table.setAlternatingRowColors(True)
        self.merchandise_table.setEditTriggers(QtWidgets.QTableWidget.DoubleClicked | QtWidgets.QTableWidget.EditKeyPressed)
        self._set_row_height(self.merchandise_table, 44)
        self.merchandise_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        main_layout.addWidget(self.merchandise_table)

        # Total value label
        self.merchandise_total_label = QtWidgets.QLabel()
        self.merchandise_total_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.merchandise_total_label)

        # Initialize current date and view mode
        self.merchandise_current_date = QtCore.QDate.currentDate()
        self.is_merchandise_weekly_view = True
        
        # Connect signals
        self.merchandise_store_combo.currentIndexChanged.connect(self.load_merchandise_history)
        self.merchandise_prev_btn.clicked.connect(self.merchandise_previous_period)
        self.merchandise_next_btn.clicked.connect(self.merchandise_next_period)
        self.merchandise_calendar_btn.clicked.connect(self.merchandise_show_calendar)
        self.merchandise_refresh_btn.clicked.connect(self.load_merchandise_history)
        self.merchandise_submit_btn.clicked.connect(self.submit_merchandise_changes)
        self.merchandise_table.cellChanged.connect(self.calculate_merchandise_total)

        # Initialize the page
        self.populate_merchandise_stores()
        self.update_merchandise_period_label()

        self.stackedWidget.addWidget(page)
        return page

    def toggle_merchandise_view(self):
        """Toggle between weekly and monthly merchandise view."""
        self.is_merchandise_weekly_view = not self.is_merchandise_weekly_view
        self.merchandise_view_toggle.setText("Weekly View" if self.is_merchandise_weekly_view else "Monthly View")
        self.update_merchandise_period_label()

    def update_merchandise_period_label(self):
        """Update the merchandise period label based on the current view mode."""
        if self.is_merchandise_weekly_view:
            week_start = self.merchandise_current_date.addDays(-self.merchandise_current_date.dayOfWeek() + 1)
            week_end = week_start.addDays(6)
            self.merchandise_period_label.setText(
                f"{week_start.toString('MMM d')} - {week_end.toString('MMM d, yyyy')}"
            )
        else:
            self.merchandise_period_label.setText(self.merchandise_current_date.toString('MMMM yyyy'))
        self.load_merchandise_history()

    def merchandise_previous_period(self):
        """Navigate to the previous period (week or month) in merchandise view."""
        if self.is_merchandise_weekly_view:
            self.merchandise_current_date = self.merchandise_current_date.addDays(-7)
        else:
            self.merchandise_current_date = self.merchandise_current_date.addMonths(-1)
        self.update_merchandise_period_label()

    def merchandise_next_period(self):
        """Navigate to the next period (week or month) in merchandise view."""
        if self.is_merchandise_weekly_view:
            self.merchandise_current_date = self.merchandise_current_date.addDays(7)
        else:
            self.merchandise_current_date = self.merchandise_current_date.addMonths(1)
        self.update_merchandise_period_label()

    def merchandise_show_calendar(self):
        """Show calendar dialog to select a date for merchandise view."""
        calendar = QtWidgets.QCalendarWidget()
        calendar.setSelectedDate(self.merchandise_current_date)
        
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select Date")
        dialog.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(calendar)
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.merchandise_current_date = calendar.selectedDate()
            self.update_merchandise_period_label()

    def load_merchandise_history(self):
        """Load the merchandise history for the selected store and period."""
        store_id = self.merchandise_store_combo.currentData()
        if store_id is None:
            return

        try:
            # Calculate start and end dates based on view mode
            if self.is_merchandise_weekly_view:
                start_date = self.merchandise_current_date.addDays(-self.merchandise_current_date.dayOfWeek() + 1)
                end_date = start_date.addDays(6)
            else:
                start_date = QtCore.QDate(self.merchandise_current_date.year(), self.merchandise_current_date.month(), 1)
                end_date = start_date.addMonths(1).addDays(-1)
            
            # Modify query based on store selection
            if store_id == -1:  # All Stores
                query = """
                    SELECT 
                        m.merchandise_id,
                        m.merchandise_date,
                        m.merchandise_type,
                        m.quantity,
                        m.unitPrice,
                        (m.quantity * m.unitPrice) as total,
                        CONCAT(emp.firstName, ' ', emp.lastName) as employee_name
                    FROM merchandise m
                    JOIN employee emp ON m.employee_id = emp.employee_id
                    WHERE DATE(m.merchandise_date) BETWEEN %s AND %s
                    ORDER BY m.merchandise_date DESC
                """
                data = (
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            else:
                query = """
                    SELECT 
                        m.merchandise_id,
                        m.merchandise_date,
                        m.merchandise_type,
                        m.quantity,
                        m.unitPrice,
                        (m.quantity * m.unitPrice) as total,
                        CONCAT(emp.firstName, ' ', emp.lastName) as employee_name
                    FROM merchandise m
                    JOIN employee emp ON m.employee_id = emp.employee_id
                    WHERE m.store_id = %s 
                    AND DATE(m.merchandise_date) BETWEEN %s AND %s
                    ORDER BY m.merchandise_date DESC
                """
                data = (
                    store_id,
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )

            results = connect(query, data)

            # Disconnect the cellChanged signal temporarily
            self.merchandise_table.cellChanged.disconnect()
            
            self.merchandise_table.setRowCount(0)
            if results:
                for row_data in results:
                    row = self.merchandise_table.rowCount()
                    self.merchandise_table.insertRow(row)
                    
                    # ID (hidden)
                    id_item = QtWidgets.QTableWidgetItem(str(row_data[0]))
                    id_item.setFlags(id_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.merchandise_table.setItem(row, 0, id_item)
                    
                    # Date
                    date_item = QtWidgets.QTableWidgetItem(str(row_data[1]))
                    date_item.setFlags(date_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.merchandise_table.setItem(row, 1, date_item)
                    
                    # Type
                    type_item = QtWidgets.QTableWidgetItem(row_data[2])
                    self.merchandise_table.setItem(row, 2, type_item)
                    
                    # Quantity
                    quantity_item = QtWidgets.QTableWidgetItem(str(row_data[3]))
                    self.merchandise_table.setItem(row, 3, quantity_item)
                    
                    # Unit Price
                    price_item = QtWidgets.QTableWidgetItem(f"${row_data[4]:.2f}")
                    self.merchandise_table.setItem(row, 4, price_item)
                    
                    # Total
                    total_item = QtWidgets.QTableWidgetItem(f"${row_data[5]:.2f}")
                    total_item.setFlags(total_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.merchandise_table.setItem(row, 5, total_item)
                    
                    # Employee
                    employee_item = QtWidgets.QTableWidgetItem(row_data[6])
                    employee_item.setFlags(employee_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.merchandise_table.setItem(row, 6, employee_item)

            # Hide the ID column
            self.merchandise_table.setColumnHidden(0, True)
            
            # Reconnect the cellChanged signal
            self.merchandise_table.cellChanged.connect(self.calculate_merchandise_total)
            
            # Calculate and display total
            self.calculate_merchandise_total()
            
        except Exception as e:
            print(f"Error loading merchandise history: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load merchandise history: {e}")

    def calculate_merchandise_total(self, row=None, column=None):
        """Calculate and display the total value of merchandise."""
        try:
            # Skip calculation if the signal was triggered by a non-editable column
            if column is not None and column not in [2, 3, 4]:  # Only Type, Quantity, and Unit Price are editable
                return

            total = 0.0
            for row in range(self.merchandise_table.rowCount()):
                quantity_item = self.merchandise_table.item(row, 3)
                price_item = self.merchandise_table.item(row, 4)
                
                if quantity_item is None or price_item is None:
                    continue
                    
                try:
                    quantity = float(quantity_item.text())
                    price_text = price_item.text().replace('$', '')
                    price = float(price_text)
                    row_total = quantity * price
                    total += row_total
                    
                    # Update the total cell
                    total_item = QtWidgets.QTableWidgetItem(f"${row_total:.2f}")
                    total_item.setFlags(total_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.merchandise_table.setItem(row, 5, total_item)
                except ValueError:
                    continue

            self.merchandise_total_label.setText(f"Total Value: ${total:.2f}")
        except Exception as e:
            print(f"Error calculating total: {e}")

    def submit_merchandise_changes(self):
        """Submit changes made to merchandise records."""
        try:
            for row in range(self.merchandise_table.rowCount()):
                merchandise_id = int(self.merchandise_table.item(row, 0).text())
                merchandise_type = self.merchandise_table.item(row, 2).text()
                quantity = int(self.merchandise_table.item(row, 3).text())
                price_text = self.merchandise_table.item(row, 4).text().replace('$', '')
                unit_price = float(price_text)

                query = """
                    UPDATE merchandise 
                    SET merchandise_type = %s,
                        quantity = %s,
                        unitPrice = %s
                    WHERE merchandise_id = %s
                """
                data = (merchandise_type, quantity, unit_price, merchandise_id)
                success = connect(query, data)

                if not success:
                    raise Exception(f"Failed to update merchandise record {merchandise_id}")

            QtWidgets.QMessageBox.information(None, "Success", "Changes saved successfully")
            self.load_merchandise_history()  # Refresh the table

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to save changes: {e}")

    def _create_close_history_page(self):
        """Create the close history page with comprehensive view."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section with icon
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title with icon
        title = QtWidgets.QLabel("Close History")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Controls container
        controls_container = QtWidgets.QWidget()
        controls_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
        """)
        controls_layout = QtWidgets.QHBoxLayout(controls_container)
        controls_layout.setSpacing(20)

        # Store selector
        self.close_store_combo = QtWidgets.QComboBox()
        self.close_store_combo.setFixedWidth(250)
        self.close_store_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
            }
            QComboBox:hover {
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        controls_layout.addWidget(self.close_store_combo)

        # View toggle button
        self.close_view_toggle = QtWidgets.QPushButton("Weekly View")
        self.close_view_toggle.setFixedHeight(40)
        self.close_view_toggle.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.close_view_toggle.clicked.connect(self.toggle_close_view)
        controls_layout.addWidget(self.close_view_toggle)

        # Week/Month navigation
        nav_container = QtWidgets.QWidget()
        nav_layout = QtWidgets.QHBoxLayout(nav_container)
        nav_layout.setSpacing(10)

        self.close_prev_btn = QtWidgets.QPushButton("←")
        self.close_prev_btn.setFixedSize(40, 40)
        self.close_prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.close_period_label = QtWidgets.QLabel()
        self.close_period_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.close_period_label.setAlignment(QtCore.Qt.AlignCenter)

        self.close_next_btn = QtWidgets.QPushButton("→")
        self.close_next_btn.setFixedSize(40, 40)
        self.close_next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        nav_layout.addWidget(self.close_prev_btn)
        nav_layout.addWidget(self.close_period_label)
        nav_layout.addWidget(self.close_next_btn)
        controls_layout.addWidget(nav_container)

        # Calendar button
        self.close_calendar_btn = QtWidgets.QPushButton("Select Date")
        self.close_calendar_btn.setFixedHeight(40)
        self.close_calendar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        controls_layout.addWidget(self.close_calendar_btn)

        # Refresh button
        self.close_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_refresh_btn.setFixedHeight(40)
        self.close_refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        controls_layout.addWidget(self.close_refresh_btn)

        main_layout.addWidget(controls_container)

        # Initialize the close table with all columns
        self.close_table = QtWidgets.QTableWidget()
        self.close_table.setColumnCount(9)
        self.close_table.setHorizontalHeaderLabels([
            "Date", "Employee", "Store", "Credit", "Cash in Envelope", 
            "Expense", "Total", "Comments", "Actions"
        ])
        
        # Set table style
        self.close_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
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
        self.close_table.setAlternatingRowColors(True)
        self.close_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.close_table)

        vh = self.close_table.verticalHeader()
        vh.setVisible(False)              # no "1, 2, 3…" column
        vh.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # Center the header text
        hh = self.close_table.horizontalHeader()
        hh.setDefaultAlignment(QtCore.Qt.AlignCenter)

        # Tell Qt exactly how each column should resize
        for col in range(self.close_table.columnCount()):
            mode = QtWidgets.QHeaderView.Stretch          # sensible default
            if col in (3, 4, 5):                          # Credit / Cash / Expense
                mode = QtWidgets.QHeaderView.ResizeToContents
            elif col == 8:                                # Actions (Save btns)
                mode = QtWidgets.QHeaderView.ResizeToContents
            hh.setSectionResizeMode(col, mode)

        # Initialize current date and view mode
        self.close_current_date = QtCore.QDate.currentDate()
        self.is_close_weekly_view = True
        
        # Connect signals
        self.close_store_combo.currentIndexChanged.connect(self.load_close_history)
        self.close_prev_btn.clicked.connect(self.close_previous_period)
        self.close_next_btn.clicked.connect(self.close_next_period)
        self.close_calendar_btn.clicked.connect(self.close_show_calendar)
        self.close_refresh_btn.clicked.connect(self.load_close_history)

        # Initialize the page
        self.populate_close_stores()
        self.update_close_period_label()

        self.stackedWidget.addWidget(page)
        return page

    def toggle_close_view(self):
        """Toggle between weekly and monthly close history view."""
        self.is_close_weekly_view = not self.is_close_weekly_view
        self.close_view_toggle.setText("Weekly View" if self.is_close_weekly_view else "Monthly View")
        self.update_close_period_label()

    def update_close_period_label(self):
        """Update the close period label based on the current view mode."""
        if self.is_close_weekly_view:
            week_start = self.close_current_date.addDays(-self.close_current_date.dayOfWeek() + 1)
            week_end = week_start.addDays(6)
            self.close_period_label.setText(
                f"{week_start.toString('MMM d')} - {week_end.toString('MMM d, yyyy')}"
            )
        else:
            self.close_period_label.setText(self.close_current_date.toString('MMMM yyyy'))
        self.load_close_history()

    def close_previous_period(self):
        """Navigate to the previous period (week or month) in close history."""
        if self.is_close_weekly_view:
            self.close_current_date = self.close_current_date.addDays(-7)
        else:
            self.close_current_date = self.close_current_date.addMonths(-1)
        self.update_close_period_label()

    def close_next_period(self):
        """Navigate to the next period (week or month) in close history."""
        if self.is_close_weekly_view:
            self.close_current_date = self.close_current_date.addDays(7)
        else:
            self.close_current_date = self.close_current_date.addMonths(1)
        self.update_close_period_label()

    def close_show_calendar(self):
        """Show calendar dialog to select a date for close history."""
        calendar = QtWidgets.QCalendarWidget()
        calendar.setSelectedDate(self.close_current_date)
        
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select Date")
        dialog.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(calendar)
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.close_current_date = calendar.selectedDate()
            self.update_close_period_label()

    def load_close_history(self):
        """Load the close history for the selected store and period."""
        store_id = self.close_store_combo.currentData()
        if store_id is None:
            return

        try:
            # Calculate start and end dates based on view mode
            if self.is_close_weekly_view:
                start_date = self.close_current_date.addDays(-self.close_current_date.dayOfWeek() + 1)
                end_date = start_date.addDays(6)
            else:
                start_date = QtCore.QDate(self.close_current_date.year(), self.close_current_date.month(), 1)
                end_date = start_date.addMonths(1).addDays(-1)
            
            # Modify query based on store selection
            if store_id == -1:  # All Stores
                query = """
                    SELECT 
                        COALESCE(ec.close_id, 0) as close_id,
                        DATE(ec.timestamp) as date,
                        CONCAT(ec.firstName, ' ', ec.lastName) as employee_name,
                        ec.store_name,
                        COALESCE(ec.credit, 0) as credit,
                        COALESCE(ec.cash_in_envelope, 0) as cash_in_envelope,
                        COALESCE(ec.expense, 0) as expense,
                        COALESCE(ec.credit, 0) + COALESCE(ec.cash_in_envelope, 0) - COALESCE(ec.expense, 0) as total,
                        ec.comments,
                        ec.employee_id,
                        ec.timestamp
                    FROM employee_close ec
                    WHERE DATE(ec.timestamp) BETWEEN %s AND %s
                    ORDER BY ec.timestamp DESC
                """
                data = (
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            else:
                query = """
                    SELECT 
                        COALESCE(ec.close_id, 0) as close_id,
                        DATE(ec.timestamp) as date,
                        CONCAT(ec.firstName, ' ', ec.lastName) as employee_name,
                        ec.store_name,
                        COALESCE(ec.credit, 0) as credit,
                        COALESCE(ec.cash_in_envelope, 0) as cash_in_envelope,
                        COALESCE(ec.expense, 0) as expense,
                        COALESCE(ec.credit, 0) + COALESCE(ec.cash_in_envelope, 0) - COALESCE(ec.expense, 0) as total,
                        ec.comments,
                        ec.employee_id,
                        ec.timestamp
                    FROM employee_close ec
                    WHERE ec.store_name = (
                        SELECT store_name FROM Store WHERE store_id = %s
                    )
                    AND DATE(ec.timestamp) BETWEEN %s AND %s
                    ORDER BY ec.timestamp DESC
                """
                data = (
                    store_id,
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )

            results = connect(query, data)
            
            # Clear existing table data
            self.close_table.setRowCount(0)
            
            if results:
                for row_data in results:
                    row = self.close_table.rowCount()
                    self.close_table.insertRow(row)
                    
                    # Store close data in the first column's UserRole
                    date_item = QtWidgets.QTableWidgetItem(row_data[1].strftime("%Y-%m-%d"))
                    date_item.setFlags(date_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    # Store both close_id and timestamp for accurate updating
                    date_item.setData(QtCore.Qt.UserRole, {
                        'close_id': row_data[0],
                        'employee_id': row_data[9],
                        'timestamp': row_data[10].strftime("%Y-%m-%d %H:%M:%S")
                    })
                    self.close_table.setItem(row, 0, date_item)
                    
                    # Employee name (non-editable)
                    emp_item = QtWidgets.QTableWidgetItem(row_data[2])
                    emp_item.setFlags(emp_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.close_table.setItem(row, 1, emp_item)
                    
                    # Store name (non-editable)
                    store_item = QtWidgets.QTableWidgetItem(row_data[3])
                    store_item.setFlags(store_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.close_table.setItem(row, 2, store_item)
                    
                    # Credit (editable)
                    credit = float(row_data[4]) if row_data[4] is not None else 0.0
                    credit_item = QtWidgets.QTableWidgetItem(f"${credit:.2f}")
                    credit_item.setFlags(credit_item.flags() | QtCore.Qt.ItemIsEditable)
                    self.close_table.setItem(row, 3, credit_item)
                    
                    # Cash in envelope (editable)
                    cash = float(row_data[5]) if row_data[5] is not None else 0.0
                    cash_item = QtWidgets.QTableWidgetItem(f"${cash:.2f}")
                    cash_item.setFlags(cash_item.flags() | QtCore.Qt.ItemIsEditable)
                    self.close_table.setItem(row, 4, cash_item)
                    
                    # Expense (editable)
                    expense = float(row_data[6]) if row_data[6] is not None else 0.0
                    expense_item = QtWidgets.QTableWidgetItem(f"${expense:.2f}")
                    expense_item.setFlags(expense_item.flags() | QtCore.Qt.ItemIsEditable)
                    self.close_table.setItem(row, 5, expense_item)
                    
                    # Total (non-editable)
                    total = float(row_data[7]) if row_data[7] is not None else 0.0
                    total_item = QtWidgets.QTableWidgetItem(f"${total:.2f}")
                    total_item.setFlags(total_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.close_table.setItem(row, 6, total_item)
                    
                    # Comments (non-editable)
                    comment_item = QtWidgets.QTableWidgetItem(row_data[8] or "")
                    comment_item.setFlags(comment_item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.close_table.setItem(row, 7, comment_item)
                    
                    edit_btn = QtWidgets.QPushButton("Save")
                    edit_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
                    edit_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #3498db;
                            color: white;
                            border: none;
                            border-radius: 0px;      /* flush with cell edges */
                            font-size: 14px;
                            font-weight: bold;
                        }
                        QPushButton:hover   { background-color: #2980b9; }
                        QPushButton:pressed { background-color: #1c6ea4; }
                    """)
                    edit_btn.clicked.connect(lambda checked, r=row: self.save_close_changes(r))

                    self.close_table.setCellWidget(row, 8, edit_btn)

                    btn_h = edit_btn.sizeHint().height() + 6   # 3‑px top + 3‑px bottom
                    if self.close_table.rowHeight(row) < btn_h:
                        self.close_table.setRowHeight(row, btn_h)

            # Resize columns to fit content
            self.close_table.resizeColumnsToContents()

        except Exception as e:
            print(f"Error loading close history: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load close history: {e}")

    def save_close_changes(self, row):
        """Save changes made to the close record."""
        try:
            close_data = self.close_table.item(row, 0).data(QtCore.Qt.UserRole)
            if not close_data:
                raise ValueError("Close data not found")
            
            # Get and validate the values
            try:
                credit = float(self.close_table.item(row, 3).text().replace('$', ''))
                cash = float(self.close_table.item(row, 4).text().replace('$', ''))
                expense = float(self.close_table.item(row, 5).text().replace('$', ''))
                
                if credit < 0 or cash < 0 or expense < 0:
                    raise ValueError("Values cannot be negative")
                
            except ValueError as e:
                raise ValueError("Invalid amount format. Please enter valid numbers.")
            
            # Update the close record
            if close_data['close_id'] > 0:
                # Update existing record
                query = """
                    UPDATE employee_close 
                    SET credit = %s,
                        cash_in_envelope = %s,
                        expense = %s
                    WHERE close_id = %s
                """
                data = (credit, cash, expense, close_data['close_id'])
            else:
                # Insert new record
                query = """
                    UPDATE employee_close 
                    SET credit = %s,
                        cash_in_envelope = %s,
                        expense = %s
                    WHERE employee_id = %s AND timestamp = %s
                """
                data = (credit, cash, expense, close_data['employee_id'], close_data['timestamp'])
            
            success = connect(query, data)
            
            if success:
                QtWidgets.QMessageBox.information(None, "Success", "Close record updated successfully")
                self.load_close_history()  # Refresh the table
            else:
                raise Exception("Failed to update close record")
                
        except Exception as e:
            print(f"Error saving close changes: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to save changes: {e}")
            self.load_close_history()  # Revert changes

    def _create_manage_users_page(self):
        """Create the user management page with three tabs."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section with icon
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title with icon
        title = QtWidgets.QLabel("Manage Users")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Tab widget for the three sections
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                padding: 10px 20px;
                margin-right: 5px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #e0e0e0;
            }
        """)

        # Create the three tabs
        self._create_add_user_tab()
        self._create_edit_user_tab()
        self._create_delete_user_tab()

        main_layout.addWidget(self.tab_widget)

        # Add shadow effect to the page
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QtGui.QColor(0, 0, 0, 30))
        shadow.setOffset(0, 0)
        page.setGraphicsEffect(shadow)

        # Populate user combos
        self._populate_user_combos()

        self.stackedWidget.addWidget(page)
        return page

    def _create_add_user_tab(self):
        """Create the Add User tab with input fields."""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Form container
        form_container = QtWidgets.QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        form_layout = QtWidgets.QFormLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Input field styling
        input_style = """
            QLineEdit, QComboBox {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """

        # Label styling
        label_style = """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0;
            }
        """

        # Role selection
        self.role_combo = QtWidgets.QComboBox()
        self.role_combo.addItems(["employee"])  # Manager can only create employees
        self.role_combo.setStyleSheet(input_style)
        self.role_combo.currentTextChanged.connect(self._update_bonus_field)
        role_label = QtWidgets.QLabel("Role")
        role_label.setStyleSheet(label_style)
        form_layout.addRow(role_label, self.role_combo)

        # First Name
        self.first_name_input = QtWidgets.QLineEdit()
        self.first_name_input.setStyleSheet(input_style)
        first_name_label = QtWidgets.QLabel("First Name")
        first_name_label.setStyleSheet(label_style)
        form_layout.addRow(first_name_label, self.first_name_input)

        # Last Name
        self.last_name_input = QtWidgets.QLineEdit()
        self.last_name_input.setStyleSheet(input_style)
        last_name_label = QtWidgets.QLabel("Last Name")
        last_name_label.setStyleSheet(label_style)
        form_layout.addRow(last_name_label, self.last_name_input)

        # Username
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setStyleSheet(input_style)
        username_label = QtWidgets.QLabel("Username")
        username_label.setStyleSheet(label_style)
        form_layout.addRow(username_label, self.username_input)

        # Password
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)
        password_label = QtWidgets.QLabel("Password")
        password_label.setStyleSheet(label_style)
        form_layout.addRow(password_label, self.password_input)

        # Bonus Percentage (only for employees)
        self.bonus_input = QtWidgets.QLineEdit()
        self.bonus_input.setStyleSheet(input_style)
        self.bonus_input.setPlaceholderText("Enter percentage (e.g., 3.5)")
        bonus_label = QtWidgets.QLabel("Bonus Percentage")
        bonus_label.setStyleSheet(label_style)
        form_layout.addRow(bonus_label, self.bonus_input)

        # Hourly Rate
        self.hourly_rate_input = QtWidgets.QLineEdit()
        self.hourly_rate_input.setStyleSheet(input_style)
        self.hourly_rate_input.setText("15.00")  # Default value
        hourly_rate_label = QtWidgets.QLabel("Hourly Rate ($)")
        hourly_rate_label.setStyleSheet(label_style)
        form_layout.addRow(hourly_rate_label, self.hourly_rate_input)

        layout.addWidget(form_container)

        # Submit button
        self.add_user_btn = QtWidgets.QPushButton("Add User")
        self.add_user_btn.setFixedHeight(50)
        self.add_user_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
        """)
        self.add_user_btn.clicked.connect(self.add_user)
        layout.addWidget(self.add_user_btn, alignment=QtCore.Qt.AlignRight)

        self.tab_widget.addTab(tab, "Add User")

    def _create_edit_user_tab(self):
        """Create the Edit User tab with user selection and edit fields."""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Form container
        form_container = QtWidgets.QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        form_layout = QtWidgets.QFormLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Input field styling
        input_style = """
            QLineEdit, QComboBox {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """

        # Label styling
        label_style = """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0;
            }
        """

        # User selection
        self.edit_user_combo = QtWidgets.QComboBox()
        self.edit_user_combo.setStyleSheet(input_style)
        self.edit_user_combo.currentIndexChanged.connect(self._load_user_data)
        user_label = QtWidgets.QLabel("Select User")
        user_label.setStyleSheet(label_style)
        form_layout.addRow(user_label, self.edit_user_combo)

        # Password
        self.edit_password_input = QtWidgets.QLineEdit()
        self.edit_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.edit_password_input.setStyleSheet(input_style)
        password_label = QtWidgets.QLabel("New Password")
        password_label.setStyleSheet(label_style)
        form_layout.addRow(password_label, self.edit_password_input)

        # Bonus Percentage (only for employees)
        self.edit_bonus_input = QtWidgets.QLineEdit()
        self.edit_bonus_input.setStyleSheet(input_style)
        self.edit_bonus_input.setPlaceholderText("Enter percentage (e.g., 3.5)")
        bonus_label = QtWidgets.QLabel("Bonus Percentage")
        bonus_label.setStyleSheet(label_style)
        form_layout.addRow(bonus_label, self.edit_bonus_input)

        # Hourly Rate
        self.edit_hourly_rate_input = QtWidgets.QLineEdit()
        self.edit_hourly_rate_input.setStyleSheet(input_style)
        self.edit_hourly_rate_input.setText("15.00")  # Default value
        hourly_rate_label = QtWidgets.QLabel("Hourly Rate ($)")
        hourly_rate_label.setStyleSheet(label_style)
        form_layout.addRow(hourly_rate_label, self.edit_hourly_rate_input)

        layout.addWidget(form_container)

        # Submit button
        self.edit_user_btn = QtWidgets.QPushButton("Update User")
        self.edit_user_btn.setFixedHeight(50)
        self.edit_user_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2472a4;
            }
        """)
        self.edit_user_btn.clicked.connect(self.update_user)
        layout.addWidget(self.edit_user_btn, alignment=QtCore.Qt.AlignRight)

        self.tab_widget.addTab(tab, "Edit User")

    def _create_delete_user_tab(self):
        """Create the Delete User tab with user selection."""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Form container
        form_container = QtWidgets.QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        form_layout = QtWidgets.QFormLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Input field styling
        input_style = """
            QComboBox {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """

        # Label styling
        label_style = """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0;
            }
        """

        # User selection
        self.delete_user_combo = QtWidgets.QComboBox()
        self.delete_user_combo.setStyleSheet(input_style)
        user_label = QtWidgets.QLabel("Select User to Delete")
        user_label.setStyleSheet(label_style)
        form_layout.addRow(user_label, self.delete_user_combo)

        layout.addWidget(form_container)

        # Delete button
        self.delete_user_btn = QtWidgets.QPushButton("Delete User")
        self.delete_user_btn.setFixedHeight(50)
        self.delete_user_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.delete_user_btn.clicked.connect(self.delete_user)
        layout.addWidget(self.delete_user_btn, alignment=QtCore.Qt.AlignRight)

        self.tab_widget.addTab(tab, "Delete User")

    def _update_bonus_field(self, role):
        """Update the bonus input field based on the selected role."""
        if role in ["manager", "owner"]:
            self.bonus_input.setText("1.0")
            self.bonus_input.setEnabled(False)
        else:
            self.bonus_input.clear()
            self.bonus_input.setEnabled(True)

    def _load_user_data(self, index):
        """Load user data when a user is selected in the edit tab."""
        if index < 0:
            return

        user_id = self.edit_user_combo.currentData()
        if not user_id:
            return

        try:
            query = """
                SELECT role, bonus_percentage, hourlyRate 
                FROM employee 
                WHERE employee_id = %s
            """
            data = (user_id,)
            results = connect(query, data)

            if results:
                role, bonus, hourly_rate = results[0]
                if role in ["manager", "owner"]:
                    self.edit_bonus_input.setText("1.00")
                    self.edit_bonus_input.setEnabled(False)
                else:
                    # Display bonus percentage with 2 decimal places
                    self.edit_bonus_input.setText(f"{float(bonus):.2f}")
                    self.edit_bonus_input.setEnabled(True)
                
                # Set hourly rate
                self.edit_hourly_rate_input.setText(f"{float(hourly_rate):.2f}" if hourly_rate else "15.00")
        except Exception as e:
            print(f"Error loading user data: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load user data: {e}")

    def add_user(self):
        """Handle adding a new user."""
        from decimal import Decimal
        try:
            # Get input values
            role = self.role_combo.currentText()
            first_name = self.first_name_input.text().strip()
            last_name = self.last_name_input.text().strip()
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()
            bonus = self.bonus_input.text().strip()
            hourly_rate = self.hourly_rate_input.text().strip()

            # Validate inputs
            if not all([first_name, last_name, username, password]):
                raise ValueError("All fields are required")

            try:
                hourly_rate = Decimal(hourly_rate).quantize(Decimal('0.01'))
                if hourly_rate <= 0:
                    raise ValueError("Hourly rate must be greater than 0")
            except ValueError:
                raise ValueError("Invalid hourly rate")

            if role == "employee":
                try:
                    # Store bonus percentage as is with 2 decimal precision
                    bonus_value = Decimal(bonus).quantize(Decimal('0.01'))
                    if bonus_value < 0:
                        raise ValueError("Bonus percentage cannot be negative")
                except ValueError as e:
                    if "cannot be negative" in str(e):
                        raise e
                    raise ValueError("Bonus percentage must be a number")
            else:
                bonus_value = Decimal('1.00')  # Managers and owners always have 1.0

            # Insert into database
            query = """
                INSERT INTO employee 
                (firstName, lastName, userName, password, role, bonus_percentage, hourlyRate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            data = (first_name, last_name, username, password, role, str(bonus_value), str(hourly_rate))
            success = connect(query, data)

            if success:
                QtWidgets.QMessageBox.information(None, "Success", "User added successfully")
                # Clear input fields
                self.first_name_input.clear()
                self.last_name_input.clear()
                self.username_input.clear()
                self.password_input.clear()
                self.bonus_input.clear()
                self.hourly_rate_input.setText("15.00")  # Reset to default
                # Refresh user lists
                self._populate_user_combos()
            else:
                raise Exception("Failed to add user")

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", str(e))

    def update_user(self):
        """Handle updating an existing user."""
        from decimal import Decimal
        try:
            user_id = self.edit_user_combo.currentData()
            if not user_id:
                raise ValueError("Please select a user")

            # Get input values
            password = self.edit_password_input.text().strip()
            bonus = self.edit_bonus_input.text().strip()
            hourly_rate = self.edit_hourly_rate_input.text().strip()

            # Validate inputs
            if not password:
                raise ValueError("Password is required")

            try:
                hourly_rate = Decimal(hourly_rate).quantize(Decimal('0.01'))
                if hourly_rate <= 0:
                    raise ValueError("Hourly rate must be greater than 0")
            except ValueError:
                raise ValueError("Invalid hourly rate")

            # Get user role and verify it's an employee
            query = "SELECT role FROM employee WHERE employee_id = %s"
            data = (user_id,)
            results = connect(query, data)
            if not results:
                raise Exception("User not found")

            role = results[0][0]
            if role != "employee":
                raise ValueError("You can only edit employee accounts")

            try:
                # Store bonus percentage as is with 2 decimal precision
                bonus_value = Decimal(bonus).quantize(Decimal('0.01'))
                if bonus_value < 0:
                    raise ValueError("Bonus percentage cannot be negative")
            except ValueError as e:
                if "cannot be negative" in str(e):
                    raise e
                raise ValueError("Bonus percentage must be a number")

            # Update database
            query = """
                UPDATE employee 
                SET password = %s, 
                    bonus_percentage = %s,
                    hourlyRate = %s
                WHERE employee_id = %s
                AND role = 'employee'
            """
            data = (password, str(bonus_value), str(hourly_rate), user_id)
            success = connect(query, data)

            if success:
                QtWidgets.QMessageBox.information(None, "Success", "User updated successfully")
                # Clear input fields
                self.edit_password_input.clear()
                self.edit_bonus_input.clear()
                self.edit_hourly_rate_input.setText("15.00")  # Reset to default
            else:
                raise Exception("Failed to update user")

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", str(e))

    def delete_user(self):
        """Handle deleting a user."""
        try:
            user_id = self.delete_user_combo.currentData()
            if not user_id:
                raise ValueError("Please select a user")

            # Verify the user is an employee
            query = "SELECT role FROM employee WHERE employee_id = %s"
            data = (user_id,)
            results = connect(query, data)
            if not results:
                raise Exception("User not found")

            role = results[0][0]
            if role != "employee":
                raise ValueError("You can only delete employee accounts")

            # Confirm deletion
            reply = QtWidgets.QMessageBox.question(
                None,
                'Confirm Deletion',
                'Are you sure you want to delete this employee? This will remove their personal information but keep their associated records.',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )

            if reply == QtWidgets.QMessageBox.Yes:
                # First, set all foreign key references to NULL
                tables_to_update = [
                    "expenses",
                    "merchandise",
                    "clockTable",
                    "employee_close",
                    "Payroll"
                ]

                for table in tables_to_update:
                    query = f"UPDATE {table} SET employee_id = NULL WHERE employee_id = %s"
                    data = (user_id,)
                    connect(query, data)

                # Now delete the user
                query = "DELETE FROM employee WHERE employee_id = %s AND role = 'employee'"
                data = (user_id,)
                success = connect(query, data)

                if success:
                    QtWidgets.QMessageBox.information(None, "Success", "Employee deleted successfully")
                    # Refresh user lists
                    self._populate_user_combos()
                else:
                    raise Exception("Failed to delete employee")

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", str(e))

    def _populate_user_combos(self):
        """Populate the user combo boxes with all users except owners."""
        try:
            query = """
                SELECT employee_id, firstName, lastName, userName, role 
                FROM employee 
                WHERE role = 'employee'
                ORDER BY lastName, firstName
            """
            results = connect(query, None)

            if results:
                # Clear existing items
                self.edit_user_combo.clear()
                self.delete_user_combo.clear()

                # Add users to both combo boxes
                for user in results:
                    display_text = f"{user[1]} {user[2]} ({user[3]}) - {user[4]}"
                    self.edit_user_combo.addItem(display_text, user[0])
                    self.delete_user_combo.addItem(display_text, user[0])
        except Exception as e:
            print(f"Error populating user combos: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load users: {e}")

    def _retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Manager Dashboard"))  # Updated dialog title

    def update_expenses_week_label(self):
        """Update the expenses week label with the current week range."""
        week_end = self.expenses_current_week_start.addDays(6)
        self.expenses_week_label.setText(
            f"{self.expenses_current_week_start.toString('MMM d')} - {week_end.toString('MMM d, yyyy')}"
        )
        self.load_expenses_history()

    def expenses_previous_week(self):
        """Navigate to the previous week in expenses history."""
        self.expenses_current_week_start = self.expenses_current_week_start.addDays(-7)
        self.update_expenses_week_label()

    def expenses_next_week(self):
        """Navigate to the next week in expenses history."""
        self.expenses_current_week_start = self.expenses_current_week_start.addDays(7)
        self.update_expenses_week_label()

    def expenses_show_calendar(self):
        """Show calendar dialog to select a date for expenses history."""
        calendar = QtWidgets.QCalendarWidget()
        calendar.setSelectedDate(self.expenses_current_week_start)
        
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select Date")
        dialog.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(calendar)
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_date = calendar.selectedDate()
            self.expenses_current_week_start = selected_date.addDays(-selected_date.dayOfWeek() + 1)
            self.update_expenses_week_label()

    def _create_close_page(self):
        """Create the close register page with input fields and submit functionality."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(page)
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
        self.stackedWidget.addWidget(page)
        return page

    def close_submit(self):
        """Handle the close register submission."""
        print(f"Attempting to submit close register for employee ID: {self.employee_id}")
        
        if not self.employee_id:
            QtWidgets.QMessageBox.critical(None, "Error", "Employee ID is missing. Please log in again.")
            print("Error: Employee ID is missing")
            return

        if not self.store_id:
            QtWidgets.QMessageBox.critical(None, "Error", "Store ID is missing. Please select a store.")
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
                QtWidgets.QMessageBox.critical(None, "Error", "Could not find store information.")
                print("Error: Store not found")
                return
                
            store_name = results[0][0]
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to get store information: {e}")
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
                QtWidgets.QMessageBox.critical(None, "Error", "Could not find employee information.")
                print("Error: Employee not found")
                return
                
            first_name = results[0][0]
            last_name = results[0][1]
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to get employee information: {e}")
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
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "Please enter valid numbers for credit, cash, and expense amounts.")
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
                QtWidgets.QMessageBox.information(None, "Success", "Close register submitted successfully.")
                # Clear input fields
                self.closeCreditInput.clear()
                self.closeCashInEnvInput.clear()
                self.closeExpenseInput.clear()
                self.CloseCommentsInput.clear()
                print("Close register submission successful")
            else:
                QtWidgets.QMessageBox.critical(None, "Error", "Failed to submit close register.")
                print("Error: Close register insert failed")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to submit close register: {e}")
            print(f"Error during close register submission: {e}")

    def _create_payroll_page(self):
        """Create the payroll page with employee selection and weekly/monthly pay details."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title = QtWidgets.QLabel("Payroll")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Controls container
        controls_container = QtWidgets.QWidget()
        controls_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
        """)
        controls_layout = QtWidgets.QHBoxLayout(controls_container)
        controls_layout.setSpacing(20)

        # Employee selection
        self.payroll_employee_combo = QtWidgets.QComboBox()
        self.payroll_employee_combo.setFixedWidth(250)
        self.payroll_employee_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
            }
            QComboBox:hover {
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        controls_layout.addWidget(self.payroll_employee_combo)

        # View toggle button
        self.payroll_view_toggle = QtWidgets.QPushButton("Weekly View")
        self.payroll_view_toggle.setFixedHeight(40)
        self.payroll_view_toggle.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.payroll_view_toggle.clicked.connect(self.toggle_payroll_view)
        controls_layout.addWidget(self.payroll_view_toggle)

        # Week/Month navigation
        nav_container = QtWidgets.QWidget()
        nav_layout = QtWidgets.QHBoxLayout(nav_container)
        nav_layout.setSpacing(10)

        self.payroll_prev_btn = QtWidgets.QPushButton("←")
        self.payroll_prev_btn.setFixedSize(40, 40)
        self.payroll_prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.payroll_period_label = QtWidgets.QLabel()
        self.payroll_period_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.payroll_period_label.setAlignment(QtCore.Qt.AlignCenter)

        self.payroll_next_btn = QtWidgets.QPushButton("→")
        self.payroll_next_btn.setFixedSize(40, 40)
        self.payroll_next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        nav_layout.addWidget(self.payroll_prev_btn)
        nav_layout.addWidget(self.payroll_period_label)
        nav_layout.addWidget(self.payroll_next_btn)
        controls_layout.addWidget(nav_container)

        # Calendar button
        self.payroll_calendar_btn = QtWidgets.QPushButton("Select Date")
        self.payroll_calendar_btn.setFixedHeight(40)
        self.payroll_calendar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        controls_layout.addWidget(self.payroll_calendar_btn)

        # Refresh button
        self.payroll_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.payroll_refresh_btn.setFixedHeight(40)
        self.payroll_refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        controls_layout.addWidget(self.payroll_refresh_btn)

        main_layout.addWidget(controls_container)

        # Payroll table
        self.payroll_table = QtWidgets.QTableWidget()
        self.payroll_table.setColumnCount(8)  # Increased from 7 to 8 columns
        self.payroll_table.setHorizontalHeaderLabels([
            "Date", "Employee", "Hours Worked", "Hourly Rate", "Hourly Pay", 
            "Register Diff", "Bonus", "Total Pay"
        ])
        self.payroll_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
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
        self.payroll_table.setAlternatingRowColors(True)
        self.payroll_table.horizontalHeader().setStretchLastSection(True)
        self._set_row_height(self.payroll_table, 44)
        main_layout.addWidget(self.payroll_table)

        # Total pay label
        self.total_pay_label = QtWidgets.QLabel()
        self.total_pay_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.total_pay_label, alignment=QtCore.Qt.AlignRight)

        # Initialize current date and view mode
        self.payroll_current_date = QtCore.QDate.currentDate()
        self.is_payroll_weekly_view = True
        
        # Connect signals
        self.payroll_employee_combo.currentIndexChanged.connect(self.load_payroll)
        self.payroll_prev_btn.clicked.connect(self.payroll_previous_period)
        self.payroll_next_btn.clicked.connect(self.payroll_next_period)
        self.payroll_calendar_btn.clicked.connect(self.payroll_show_calendar)
        self.payroll_refresh_btn.clicked.connect(self.load_payroll)

        # Initialize the page
        self.populate_payroll_employees()
        self.update_payroll_period_label()

        self.stackedWidget.addWidget(page)
        return page

    def toggle_payroll_view(self):
        """Toggle between weekly and monthly payroll view."""
        self.is_payroll_weekly_view = not self.is_payroll_weekly_view
        self.payroll_view_toggle.setText("Weekly View" if self.is_payroll_weekly_view else "Monthly View")
        self.update_payroll_period_label()

    def update_payroll_period_label(self):
        """Update the payroll period label based on the current view mode."""
        if self.is_payroll_weekly_view:
            week_start = self.payroll_current_date.addDays(-self.payroll_current_date.dayOfWeek() + 1)
            week_end = week_start.addDays(6)
            self.payroll_period_label.setText(
                f"{week_start.toString('MMM d')} - {week_end.toString('MMM d, yyyy')}"
            )
        else:
            self.payroll_period_label.setText(self.payroll_current_date.toString('MMMM yyyy'))
        self.load_payroll()

    def payroll_previous_period(self):
        """Navigate to the previous period (week or month) in payroll view."""
        if self.is_payroll_weekly_view:
            self.payroll_current_date = self.payroll_current_date.addDays(-7)
        else:
            self.payroll_current_date = self.payroll_current_date.addMonths(-1)
        self.update_payroll_period_label()

    def payroll_next_period(self):
        """Navigate to the next period (week or month) in payroll view."""
        if self.is_payroll_weekly_view:
            self.payroll_current_date = self.payroll_current_date.addDays(7)
        else:
            self.payroll_current_date = self.payroll_current_date.addMonths(1)
        self.update_payroll_period_label()

    def payroll_show_calendar(self):
        """Show calendar dialog to select a date for payroll view."""
        calendar = QtWidgets.QCalendarWidget()
        calendar.setSelectedDate(self.payroll_current_date)
        
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select Date")
        dialog.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(calendar)
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.payroll_current_date = calendar.selectedDate()
            self.update_payroll_period_label()

    def load_payroll(self):
        """Load the payroll data for the selected employee and period."""
        from decimal import Decimal

        employee_id = self.payroll_employee_combo.currentData()
        if employee_id is None:
            return

        try:
            # Calculate start and end dates based on view mode
            if self.is_payroll_weekly_view:
                start_date = self.payroll_current_date.addDays(-self.payroll_current_date.dayOfWeek() + 1)
                end_date = start_date.addDays(6)
            else:
                start_date = QtCore.QDate(self.payroll_current_date.year(), self.payroll_current_date.month(), 1)
                end_date = start_date.addMonths(1).addDays(-1)
            
            if employee_id == -1:  # All Employees
                # Get all employees' hourly rates and bonus percentages
                query = """
                    SELECT e.employee_id, 
                           COALESCE(e.hourlyRate, 15.00) as hourlyRate, 
                           COALESCE(e.bonus_percentage, 0) as bonus_percentage,
                           CONCAT(e.firstName, ' ', e.lastName) as employee_name,
                           c.clock_in,
                           c.clock_out,
                           c.reg_in,
                           c.reg_out
                    FROM employee e
                    LEFT JOIN clockTable c ON e.employee_id = c.employee_id
                    WHERE e.role IN ('employee', 'manager')
                    AND (c.clock_in IS NULL OR DATE(c.clock_in) BETWEEN %s AND %s)
                    ORDER BY c.clock_in DESC, e.lastName, e.firstName
                """
                data = (
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            else:
                # Get single employee's data
                query = """
                    SELECT e.employee_id,
                           COALESCE(e.hourlyRate, 15.00) as hourlyRate,
                           COALESCE(e.bonus_percentage, 0) as bonus_percentage,
                           CONCAT(e.firstName, ' ', e.lastName) as employee_name,
                           c.clock_in,
                           c.clock_out,
                           c.reg_in,
                           c.reg_out
                    FROM employee e
                    LEFT JOIN clockTable c ON e.employee_id = c.employee_id
                    WHERE e.employee_id = %s
                    AND (c.clock_in IS NULL OR DATE(c.clock_in) BETWEEN %s AND %s)
                    ORDER BY c.clock_in DESC
                """
                data = (
                    employee_id,
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )

            print(f"Executing payroll query with data: {data}")
            results = connect(query, data)
            print(f"Found {len(results) if results else 0} payroll records")

            # Clear existing table data
            self.payroll_table.setRowCount(0)
            total_period_pay = Decimal('0.00')

            if results:
                for row_data in results:
                    # Skip if no clock in/out data
                    if row_data[4] is None or row_data[5] is None:
                        continue

                    row = self.payroll_table.rowCount()
                    self.payroll_table.insertRow(row)

                    # Calculate hours worked
                    clock_in = row_data[4]
                    clock_out = row_data[5]
                    hours = (clock_out - clock_in).total_seconds() / 3600
                    
                    # Get register values
                    reg_in = float(row_data[6] if row_data[6] is not None else 0)
                    reg_out = float(row_data[7] if row_data[7] is not None else reg_in)

                    # Calculate pays using Decimal for precision
                    hourly_rate = Decimal(str(row_data[1])).quantize(Decimal('0.01'))
                    hourly_pay = (Decimal(str(hours)) * hourly_rate).quantize(Decimal('0.01'))
                    register_diff = Decimal(str(reg_out - reg_in)).quantize(Decimal('0.01'))
                    
                    # Calculate bonus
                    bonus_percentage = Decimal(str(row_data[2])).quantize(Decimal('0.01'))
                    if register_diff > 0:
                        bonus = (register_diff * (bonus_percentage / Decimal('100'))).quantize(Decimal('0.01'))
                    else:
                        bonus = Decimal('0.00')

                    total_pay = (hourly_pay + bonus).quantize(Decimal('0.01'))
                    total_period_pay += total_pay

                    # Add items to table
                    items = [
                        clock_in.strftime("%Y-%m-%d"),  # Date
                        row_data[3],                    # Employee name
                        f"{hours:.2f}",                 # Hours worked
                        f"${hourly_rate:.2f}",         # Hourly rate
                        f"${hourly_pay:.2f}",          # Hourly pay
                        f"${register_diff:.2f}",       # Register difference
                        f"${bonus:.2f}",               # Bonus
                        f"${total_pay:.2f}"            # Total pay
                    ]

                    for col, item in enumerate(items):
                        table_item = QtWidgets.QTableWidgetItem(item)
                        table_item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.payroll_table.setItem(row, col, table_item)

            # Update total pay label
            period_type = "Weekly" if self.is_payroll_weekly_view else "Monthly"
            employee_text = "All Employees" if employee_id == -1 else self.payroll_employee_combo.currentText()
            self.total_pay_label.setText(f"Total {period_type} Pay ({employee_text}): ${total_period_pay:.2f}")

            # Resize columns to fit content
            self.payroll_table.resizeColumnsToContents()

        except Exception as e:
            print(f"Error loading payroll: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load payroll: {e}")

    def load_stores(self):
        """Load existing stores into the list widget."""
        try:
            query = "SELECT store_id, store_name, location FROM Store ORDER BY store_name"
            results = connect(query, None)
            
            self.store_list.clear()
            if results:
                for store in results:
                    item = QtWidgets.QListWidgetItem(f"{store[1]} ({store[2]})")
                    item.setData(QtCore.Qt.UserRole, store[0])  # Store ID
                    self.store_list.addItem(item)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load stores: {e}")

    def on_store_selected(self):
        """Handle store selection in the list."""
        selected_items = self.store_list.selectedItems()
        if selected_items:
            store_id = selected_items[0].data(QtCore.Qt.UserRole)
            try:
                query = "SELECT store_name, location FROM Store WHERE store_id = %s"
                results = connect(query, (store_id,))
                
                if results:
                    store = results[0]
                    self.store_name_input.setText(store[0])
                    self.store_location_input.setText(store[1])
                    
                    self.update_store_btn.setEnabled(True)
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load store details: {e}")
        else:
            self.store_name_input.clear()
            self.store_location_input.clear()
            self.update_store_btn.setEnabled(False)

    def add_store(self):
        """Add a new store to the database."""
        try:
            store_name = self.store_name_input.text().strip()
            location = self.store_location_input.text().strip()
            
            if not store_name or not location:
                raise ValueError("Store name and location are required")
            
            query = "INSERT INTO Store (store_name, location) VALUES (%s, %s)"
            data = (store_name, location)
            success = connect(query, data)
            
            if success:
                QtWidgets.QMessageBox.information(None, "Success", "Store added successfully")
                self.store_name_input.clear()
                self.store_location_input.clear()
                self.load_stores()
                
                # Refresh store combo boxes throughout the application
                self.populate_stores()
                self.populate_expenses_stores()
                self.populate_merchandise_stores()
                self.populate_close_stores()
            else:
                raise Exception("Failed to add store")
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", str(e))

    def update_store(self):
        """Update the selected store."""
        selected_items = self.store_list.selectedItems()
        if not selected_items:
            return
            
        try:
            store_id = selected_items[0].data(QtCore.Qt.UserRole)
            store_name = self.store_name_input.text().strip()
            location = self.store_location_input.text().strip()
            
            if not store_name or not location:
                raise ValueError("Store name and location are required")
            
            query = "UPDATE Store SET store_name = %s, location = %s WHERE store_id = %s"
            data = (store_name, location, store_id)
            success = connect(query, data)
            
            if success:
                QtWidgets.QMessageBox.information(None, "Success", "Store updated successfully")
                self.load_stores()
                
                # Refresh store combo boxes throughout the application
                self.populate_stores()
                self.populate_expenses_stores()
                self.populate_merchandise_stores()
                self.populate_close_stores()
            else:
                raise Exception("Failed to update store")
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", str(e))

    def _create_gross_profit_page(self):
        """Create the gross profit page with store selection and profit details."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title = QtWidgets.QLabel("Gross Profit")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Controls container
        controls_container = QtWidgets.QWidget()
        controls_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
        """)
        controls_layout = QtWidgets.QHBoxLayout(controls_container)
        controls_layout.setSpacing(20)

        # Store selection
        self.profit_store_combo = QtWidgets.QComboBox()
        self.profit_store_combo.setFixedWidth(250)
        self.profit_store_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
            }
            QComboBox:hover {
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        controls_layout.addWidget(self.profit_store_combo)

        # View toggle button
        self.profit_view_toggle = QtWidgets.QPushButton("Weekly View")
        self.profit_view_toggle.setFixedHeight(40)
        self.profit_view_toggle.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.profit_view_toggle.clicked.connect(self.toggle_profit_view)
        controls_layout.addWidget(self.profit_view_toggle)

        # Week/Month navigation
        week_nav_container = QtWidgets.QWidget()
        week_nav_layout = QtWidgets.QHBoxLayout(week_nav_container)
        week_nav_layout.setSpacing(10)

        self.profit_prev_btn = QtWidgets.QPushButton("←")
        self.profit_prev_btn.setFixedSize(40, 40)
        self.profit_prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.profit_period_label = QtWidgets.QLabel()
        self.profit_period_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.profit_period_label.setAlignment(QtCore.Qt.AlignCenter)

        self.profit_next_btn = QtWidgets.QPushButton("→")
        self.profit_next_btn.setFixedSize(40, 40)
        self.profit_next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        week_nav_layout.addWidget(self.profit_prev_btn)
        week_nav_layout.addWidget(self.profit_period_label)
        week_nav_layout.addWidget(self.profit_next_btn)
        controls_layout.addWidget(week_nav_container)

        # Calendar button
        self.profit_calendar_btn = QtWidgets.QPushButton("Select Date")
        self.profit_calendar_btn.setFixedHeight(40)
        self.profit_calendar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        controls_layout.addWidget(self.profit_calendar_btn)

        # Refresh button
        self.profit_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.profit_refresh_btn.setFixedHeight(40)
        self.profit_refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        controls_layout.addWidget(self.profit_refresh_btn)

        main_layout.addWidget(controls_container)

        # Profit table
        self.profit_table = QtWidgets.QTableWidget()
        self.profit_table.setColumnCount(8)
        self.profit_table.setHorizontalHeaderLabels([
            "Date", "Cash", "Credit", "Expenses", "Merchandise", "Payroll", "Total", "Details"
        ])
        self.profit_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
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
        self.profit_table.setAlternatingRowColors(True)
        self.profit_table.horizontalHeader().setStretchLastSection(True)
        self._set_row_height(self.profit_table, 44)
        main_layout.addWidget(self.profit_table)

        # Total profit label
        self.total_profit_label = QtWidgets.QLabel()
        self.total_profit_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.total_profit_label, alignment=QtCore.Qt.AlignRight)

        # Initialize current date and view mode
        self.profit_current_date = QtCore.QDate.currentDate()
        self.is_weekly_view = True
        
        # Connect signals
        self.profit_store_combo.currentIndexChanged.connect(self.load_profit)
        self.profit_prev_btn.clicked.connect(self.profit_previous_period)
        self.profit_next_btn.clicked.connect(self.profit_next_period)
        self.profit_calendar_btn.clicked.connect(self.profit_show_calendar)
        self.profit_refresh_btn.clicked.connect(self.load_profit)

        # Initialize the page
        self.populate_profit_stores()
        self.update_profit_period_label()

        self.stackedWidget.addWidget(page)
        return page

    def toggle_profit_view(self):
        """Toggle between weekly and monthly view."""
        self.is_weekly_view = not self.is_weekly_view
        self.profit_view_toggle.setText("Weekly View" if self.is_weekly_view else "Monthly View")
        self.update_profit_period_label()

    def update_profit_period_label(self):
        """Update the period label based on the current view mode."""
        if self.is_weekly_view:
            week_start = self.profit_current_date.addDays(-self.profit_current_date.dayOfWeek() + 1)
            week_end = week_start.addDays(6)
            self.profit_period_label.setText(
                f"{week_start.toString('MMM d')} - {week_end.toString('MMM d, yyyy')}"
            )
        else:
            self.profit_period_label.setText(self.profit_current_date.toString('MMMM yyyy'))
        self.load_profit()

    def profit_previous_period(self):
        """Navigate to the previous period (week or month) in profit view."""
        if self.is_weekly_view:
            self.profit_current_date = self.profit_current_date.addDays(-7)
        else:
            self.profit_current_date = self.profit_current_date.addMonths(-1)
        self.update_profit_period_label()

    def profit_next_period(self):
        """Navigate to the next period (week or month) in profit view."""
        if self.is_weekly_view:
            self.profit_current_date = self.profit_current_date.addDays(7)
        else:
            self.profit_current_date = self.profit_current_date.addMonths(1)
        self.update_profit_period_label()

    def profit_show_calendar(self):
        """Show calendar dialog to select a date for profit view."""
        calendar = QtWidgets.QCalendarWidget()
        calendar.setSelectedDate(self.profit_current_date)
        
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select Date")
        dialog.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(calendar)
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.profit_current_date = calendar.selectedDate()
            self.update_profit_period_label()

    def load_profit(self):
        """Load the profit data for the selected store and period."""
        from decimal import Decimal

        store_id = self.profit_store_combo.currentData()
        if store_id is None:
            return

        try:
            # Calculate start and end dates based on view mode
            if self.is_weekly_view:
                start_date = self.profit_current_date.addDays(-self.profit_current_date.dayOfWeek() + 1)
                end_date = start_date.addDays(6)
            else:
                start_date = QtCore.QDate(self.profit_current_date.year(), self.profit_current_date.month(), 1)
                end_date = start_date.addMonths(1).addDays(-1)
            
            # Get daily data from employee_close table
            if store_id == -1:  # All Stores
                close_query = """
                    SELECT 
                        DATE(timestamp) as date,
                        store_name,
                        COALESCE(SUM(cash_in_envelope), 0) as cash,
                        COALESCE(SUM(credit), 0) as credit,
                        COALESCE(SUM(expense), 0) as expenses
                    FROM employee_close
                    WHERE DATE(timestamp) BETWEEN %s AND %s
                    GROUP BY DATE(timestamp), store_name
                    ORDER BY date DESC, store_name
                """
                close_data = (
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            else:
                close_query = """
                    SELECT 
                        DATE(timestamp) as date,
                        store_name,
                        COALESCE(SUM(cash_in_envelope), 0) as cash,
                        COALESCE(SUM(credit), 0) as credit,
                        COALESCE(SUM(expense), 0) as expenses
                    FROM employee_close
                    WHERE store_name = (SELECT store_name FROM Store WHERE store_id = %s)
                    AND DATE(timestamp) BETWEEN %s AND %s
                    GROUP BY DATE(timestamp), store_name
                    ORDER BY date DESC
                """
                close_data = (
                    store_id,
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            
            close_results = connect(close_query, close_data)
            
            # Get merchandise data
            if store_id == -1:
                merch_query = """
                    SELECT 
                        DATE(m.merchandise_date) as date,
                        s.store_name,
                        COALESCE(SUM(m.quantity * m.unitPrice), 0) as total
                    FROM merchandise m
                    JOIN Store s ON m.store_id = s.store_id
                    WHERE DATE(m.merchandise_date) BETWEEN %s AND %s
                    GROUP BY DATE(m.merchandise_date), s.store_name
                """
                merch_data = (
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            else:
                merch_query = """
                    SELECT 
                        DATE(m.merchandise_date) as date,
                        s.store_name,
                        COALESCE(SUM(m.quantity * m.unitPrice), 0) as total
                    FROM merchandise m
                    JOIN Store s ON m.store_id = s.store_id
                    WHERE m.store_id = %s 
                    AND DATE(m.merchandise_date) BETWEEN %s AND %s
                    GROUP BY DATE(m.merchandise_date), s.store_name
                """
                merch_data = (
                    store_id,
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            
            merch_results = connect(merch_query, merch_data)
            
            # Get payroll data
            if store_id == -1:
                payroll_query = """
                    SELECT 
                        DATE(p.date) as date,
                        s.store_name,
                        COALESCE(SUM(p.bonuses), 0) as bonuses,
                        COALESCE(SUM(p.wages), 0) as wages
                    FROM Payroll p
                    JOIN Store s ON p.store_id = s.store_id
                    WHERE DATE(p.date) BETWEEN %s AND %s
                    GROUP BY DATE(p.date), s.store_name
                """
                payroll_data = (
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            else:
                payroll_query = """
                    SELECT 
                        DATE(p.date) as date,
                        s.store_name,
                        COALESCE(SUM(p.bonuses), 0) as bonuses,
                        COALESCE(SUM(p.wages), 0) as wages
                    FROM Payroll p
                    JOIN Store s ON p.store_id = s.store_id
                    WHERE p.store_id = %s 
                    AND DATE(p.date) BETWEEN %s AND %s
                    GROUP BY DATE(p.date), s.store_name
                """
                payroll_data = (
                    store_id,
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            
            payroll_results = connect(payroll_query, payroll_data)
            
            # Clear existing table data
            self.profit_table.setRowCount(0)
            
            # Create dictionaries for merchandise and payroll data
            merch_dict = {}
            if merch_results:
                for row in merch_results:
                    date_key = str(row[0])
                    store_key = row[1]
                    if date_key not in merch_dict:
                        merch_dict[date_key] = {}
                    merch_dict[date_key][store_key] = float(row[2])

            payroll_dict = {}
            if payroll_results:
                for row in payroll_results:
                    date_key = str(row[0])
                    store_key = row[1]
                    if date_key not in payroll_dict:
                        payroll_dict[date_key] = {}
                    payroll_dict[date_key][store_key] = float(row[2] + row[3])
            
            total_period_profit = Decimal('0.00')
            
            if close_results:
                for row_data in close_results:
                    row = self.profit_table.rowCount()
                    self.profit_table.insertRow(row)
                    
                    date = str(row_data[0])
                    store_name = row_data[1]
                    cash = Decimal(str(row_data[2])).quantize(Decimal('0.01'))
                    credit = Decimal(str(row_data[3])).quantize(Decimal('0.01'))
                    expenses = Decimal(str(row_data[4])).quantize(Decimal('0.01'))
                    
                    # Get merchandise and payroll values for this date and store
                    merchandise = Decimal(str(merch_dict.get(date, {}).get(store_name, 0))).quantize(Decimal('0.01'))
                    payroll = Decimal(str(payroll_dict.get(date, {}).get(store_name, 0))).quantize(Decimal('0.01'))
                    
                    # Calculate daily profit
                    daily_profit = (cash + credit - expenses - merchandise - payroll).quantize(Decimal('0.01'))
                    total_period_profit += daily_profit
                    
                    # Create details button
                    details_btn = QtWidgets.QPushButton("View")
                    details_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #3498db;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 5px 10px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
                    """)
                    
                    # Add items to table
                    items = [
                        f"{date} ({store_name})" if store_id == -1 else date,
                        f"${cash:.2f}",
                        f"${credit:.2f}",
                        f"${expenses:.2f}",
                        f"${merchandise:.2f}",
                        f"${payroll:.2f}",
                        f"${daily_profit:.2f}"
                    ]
                    
                    for col, item in enumerate(items):
                        table_item = QtWidgets.QTableWidgetItem(item)
                        table_item.setTextAlignment(QtCore.Qt.AlignCenter)
                        
                        # Color the profit/loss column
                        if col == 6:  # Total column
                            if daily_profit >= 0:
                                table_item.setForeground(QtGui.QColor("#27ae60"))  # Green for profit
                            else:
                                table_item.setForeground(QtGui.QColor("#c0392b"))  # Red for loss
                                
                        self.profit_table.setItem(row, col, table_item)
                    
                    # Add details button to the last column
                    self.profit_table.setCellWidget(row, 7, details_btn)
                    
                    # Connect the details button to show the breakdown
                    details_btn.clicked.connect(
                        lambda checked, d=date, p={
                            'Cash': cash,
                            'Credit': credit,
                            'Expenses': expenses,
                            'Merchandise': merchandise,
                            'Payroll': payroll,
                            'Total': daily_profit
                        }: self.show_profit_details(d, p)
                    )
            
            # Update total profit label with color based on profit/loss
            color = "#27ae60" if total_period_profit >= 0 else "#c0392b"
            period_type = "Weekly" if self.is_weekly_view else "Monthly"
            store_text = "All Stores" if store_id == -1 else self.profit_store_combo.currentText()
            self.total_profit_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 18px;
                    font-weight: bold;
                    color: {color};
                    padding: 15px;
                    background-color: #f8f9fa;
                    border-radius: 6px;
                }}
            """)
            self.total_profit_label.setText(f"Total {period_type} Profit ({store_text}): ${total_period_profit:.2f}")
            
            # Resize columns to fit content
            self.profit_table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error loading profit data: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load profit data: {e}")

    def show_profit_details(self, date, profit_data):
        """Show a detailed breakdown of the profit calculation for a specific date."""
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle(f"Profit Details - {date}")
        dialog.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # Create a table for the breakdown
        table = QtWidgets.QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Item", "Amount"])
        table.setRowCount(len(profit_data))
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Add the data
        for row, (item, amount) in enumerate(profit_data.items()):
            # Item name
            name_item = QtWidgets.QTableWidgetItem(item)
            table.setItem(row, 0, name_item)
            
            # Amount with color coding for the total
            amount_item = QtWidgets.QTableWidgetItem(f"${amount:.2f}")
            if item == "Total":
                color = "#27ae60" if amount >= 0 else "#c0392b"
                amount_item.setForeground(QtGui.QColor(color))
                font = amount_item.font()
                font.setBold(True)
                amount_item.setFont(font)
            table.setItem(row, 1, amount_item)
        
        # Adjust table properties
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        
        layout.addWidget(table)
        
        # Add close button
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.exec_()
    
    def _set_row_height(self, table: QtWidgets.QTableWidget, px: int = 44):
        vh = table.verticalHeader()
        vh.setDefaultSectionSize(px)          # all rows get this height
        vh.setMinimumSectionSize(px)          # prevents users from shrinking them

    def populate_profit_stores(self):
        """Populate the profit store combo box with store names."""
        try:
            query = "SELECT store_id, store_name FROM Store ORDER BY store_name"
            results = connect(query, None)
            
            if results:
                self.profit_store_combo.clear()
                # Add "All Stores" option
                self.profit_store_combo.addItem("All Stores", -1)
                for store in results:
                    self.profit_store_combo.addItem(store[1], store[0])
        except Exception as e:
            print(f"Error populating profit stores: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load stores: {e}")

    def populate_payroll_employees(self):
        """Populate the payroll employee combo box with employee names."""
        try:
            query = """
                SELECT employee_id, firstName, lastName, role 
                FROM employee 
                WHERE role IN ('employee', 'manager')
                ORDER BY role, lastName, firstName
            """
            results = connect(query, None)
            
            if results:
                self.payroll_employee_combo.clear()
                # Add "All Employees" option
                self.payroll_employee_combo.addItem("All Employees", -1)
                for employee in results:
                    display_text = f"{employee[1]} {employee[2]} ({employee[3]})"
                    self.payroll_employee_combo.addItem(display_text, employee[0])
        except Exception as e:
            print(f"Error populating payroll employees: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load employees: {e}")

    def populate_close_stores(self):
        """Populate the close history store combo box with store names and IDs."""
        try:
            query = "SELECT store_id, store_name FROM Store"
            results = connect(query, None)
            
            if results:
                self.close_store_combo.clear()
                # Add "All Stores" option
                self.close_store_combo.addItem("All Stores", -1)
                for store in results:
                    self.close_store_combo.addItem(store[1], store[0])  # Store name and ID
                # Set the first store as default
                if results:
                    self.close_store_combo.setCurrentIndex(0)
        except Exception as e:
            print(f"Error populating close stores: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load stores: {e}")

    def populate_merchandise_stores(self):
        """Populate the merchandise store combo box with store names and IDs."""
        try:
            print("Attempting to populate merchandise stores...")
            query = "SELECT store_id, store_name FROM Store"
            results = connect(query, None)
            
            if results:
                print(f"Found {len(results)} stores")
                self.merchandise_store_combo.clear()
                # Add "All Stores" option
                self.merchandise_store_combo.addItem("All Stores", -1)
                for store in results:
                    print(f"Adding store: {store[1]} (ID: {store[0]})")
                    self.merchandise_store_combo.addItem(store[1], store[0])  # Store name and ID
            else:
                print("No stores found in database")
        except Exception as e:
            print(f"Error populating merchandise stores: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load stores: {e}")

    def _create_invoice_history_page(self):
        """Create the invoice history page with comprehensive view."""
        page = QtWidgets.QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        # Main layout with shadow effect
        main_layout = QtWidgets.QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Title section with icon
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title with icon
        title = QtWidgets.QLabel("Invoice History")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding-left: 10px;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addWidget(title_container)

        # Controls container
        controls_container = QtWidgets.QWidget()
        controls_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
        """)
        controls_layout = QtWidgets.QHBoxLayout(controls_container)
        controls_layout.setSpacing(20)

        # Store selector
        self.invoice_store_combo = QtWidgets.QComboBox()
        self.invoice_store_combo.setFixedWidth(250)
        self.invoice_store_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
            }
            QComboBox:hover {
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        controls_layout.addWidget(self.invoice_store_combo)

        # View toggle button
        self.invoice_view_toggle = QtWidgets.QPushButton("Weekly View")
        self.invoice_view_toggle.setFixedHeight(40)
        self.invoice_view_toggle.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.invoice_view_toggle.clicked.connect(self.toggle_invoice_view)
        controls_layout.addWidget(self.invoice_view_toggle)

        # Week/Month navigation
        nav_container = QtWidgets.QWidget()
        nav_layout = QtWidgets.QHBoxLayout(nav_container)
        nav_layout.setSpacing(10)

        self.invoice_prev_btn = QtWidgets.QPushButton("←")
        self.invoice_prev_btn.setFixedSize(40, 40)
        self.invoice_prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.invoice_period_label = QtWidgets.QLabel()
        self.invoice_period_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.invoice_period_label.setAlignment(QtCore.Qt.AlignCenter)

        self.invoice_next_btn = QtWidgets.QPushButton("→")
        self.invoice_next_btn.setFixedSize(40, 40)
        self.invoice_next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        nav_layout.addWidget(self.invoice_prev_btn)
        nav_layout.addWidget(self.invoice_period_label)
        nav_layout.addWidget(self.invoice_next_btn)
        controls_layout.addWidget(nav_container)

        # Calendar button
        self.invoice_calendar_btn = QtWidgets.QPushButton("Select Date")
        self.invoice_calendar_btn.setFixedHeight(40)
        self.invoice_calendar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        controls_layout.addWidget(self.invoice_calendar_btn)

        # Refresh button
        self.invoice_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.invoice_refresh_btn.setFixedHeight(40)
        self.invoice_refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        controls_layout.addWidget(self.invoice_refresh_btn)

        main_layout.addWidget(controls_container)

        # Invoice table
        self.invoice_table = QtWidgets.QTableWidget()
        self.invoice_table.setColumnCount(10)  # Updated column count
        self.invoice_table.setHorizontalHeaderLabels([
            "Invoice ID", "Company", "Original Amount", "Amount Paid", "Amount Due", "Received Date", 
            "Due Date", "Status", "Payment Date", "Actions"
        ])
        self.invoice_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
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
        self.invoice_table.setAlternatingRowColors(True)
        self.invoice_table.horizontalHeader().setStretchLastSection(True)
        self._set_row_height(self.invoice_table, 44)
        main_layout.addWidget(self.invoice_table)

        # Total amount label
        self.total_invoice_label = QtWidgets.QLabel()
        self.total_invoice_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.total_invoice_label, alignment=QtCore.Qt.AlignRight)

        # Initialize current date and view mode
        self.invoice_current_date = QtCore.QDate.currentDate()
        self.is_invoice_weekly_view = True
        
        # Connect signals
        self.invoice_store_combo.currentIndexChanged.connect(self.load_invoice_history)
        self.invoice_prev_btn.clicked.connect(self.invoice_previous_period)
        self.invoice_next_btn.clicked.connect(self.invoice_next_period)
        self.invoice_calendar_btn.clicked.connect(self.invoice_show_calendar)
        self.invoice_refresh_btn.clicked.connect(self.load_invoice_history)

        # Initialize the page
        self.populate_invoice_stores()
        self.update_invoice_period_label()

        self.stackedWidget.addWidget(page)
        return page

    def toggle_invoice_view(self):
        """Toggle between weekly and monthly invoice view."""
        self.is_invoice_weekly_view = not self.is_invoice_weekly_view
        self.invoice_view_toggle.setText("Weekly View" if self.is_invoice_weekly_view else "Monthly View")
        self.update_invoice_period_label()

    def update_invoice_period_label(self):
        """Update the invoice period label based on the current view mode."""
        if self.is_invoice_weekly_view:
            week_start = self.invoice_current_date.addDays(-self.invoice_current_date.dayOfWeek() + 1)
            week_end = week_start.addDays(6)
            self.invoice_period_label.setText(
                f"{week_start.toString('MMM d')} - {week_end.toString('MMM d, yyyy')}"
            )
        else:
            self.invoice_period_label.setText(self.invoice_current_date.toString('MMMM yyyy'))
        self.load_invoice_history()

    def invoice_previous_period(self):
        """Navigate to the previous period (week or month) in invoice view."""
        if self.is_invoice_weekly_view:
            self.invoice_current_date = self.invoice_current_date.addDays(-7)
        else:
            self.invoice_current_date = self.invoice_current_date.addMonths(-1)
        self.update_invoice_period_label()

    def invoice_next_period(self):
        """Navigate to the next period (week or month) in invoice view."""
        if self.is_invoice_weekly_view:
            self.invoice_current_date = self.invoice_current_date.addDays(7)
        else:
            self.invoice_current_date = self.invoice_current_date.addMonths(1)
        self.update_invoice_period_label()

    def invoice_show_calendar(self):
        """Show calendar dialog to select a date for invoice view."""
        calendar = QtWidgets.QCalendarWidget()
        calendar.setSelectedDate(self.invoice_current_date)
        
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Select Date")
        dialog.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(calendar)
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.invoice_current_date = calendar.selectedDate()
            self.update_invoice_period_label()

    def populate_invoice_stores(self):
        """Populate the invoice store combo box with store names."""
        try:
            query = "SELECT store_id, store_name FROM Store ORDER BY store_name"
            results = connect(query, None)
            
            if results:
                self.invoice_store_combo.clear()
                # Add "All Stores" option
                self.invoice_store_combo.addItem("All Stores", -1)
                for store in results:
                    self.invoice_store_combo.addItem(store[1], store[0])
        except Exception as e:
            print(f"Error populating invoice stores: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load stores: {e}")

    def load_invoice_history(self):
        """Load the invoice history for the selected store and period."""
        store_id = self.invoice_store_combo.currentData()
        if store_id is None:
            return

        try:
            # Calculate start and end dates based on view mode
            if self.is_invoice_weekly_view:
                start_date = self.invoice_current_date.addDays(-self.invoice_current_date.dayOfWeek() + 1)
                end_date = start_date.addDays(6)
            else:
                start_date = QtCore.QDate(self.invoice_current_date.year(), self.invoice_current_date.month(), 1)
                end_date = start_date.addMonths(1).addDays(-1)
            
            # Modify query based on store selection
            if store_id == -1:  # All Stores
                query = """
                    SELECT 
                        invoice_id,
                        company_name,
                        amount,
                        COALESCE(amount_paid, 0) as amount_paid,
                        (amount - COALESCE(amount_paid, 0)) as amount_due,
                        recieved_date,
                        due_date,
                        paid_status,
                        payment_date,
                        s.store_name
                    FROM Invoice i
                    JOIN Store s ON i.store_id = s.store_id
                    WHERE recieved_date BETWEEN %s AND %s
                    ORDER BY recieved_date DESC
                """
                data = (
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )
            else:
                query = """
                    SELECT 
                        invoice_id,
                        company_name,
                        amount,
                        COALESCE(amount_paid, 0) as amount_paid,
                        (amount - COALESCE(amount_paid, 0)) as amount_due,
                        recieved_date,
                        due_date,
                        paid_status,
                        payment_date,
                        s.store_name
                    FROM Invoice i
                    JOIN Store s ON i.store_id = s.store_id
                    WHERE i.store_id = %s 
                    AND recieved_date BETWEEN %s AND %s
                    ORDER BY recieved_date DESC
                """
                data = (
                    store_id,
                    start_date.toPyDate(),
                    end_date.toPyDate()
                )

            results = connect(query, data)
            
            # Clear existing table data
            self.invoice_table.setRowCount(0)
            
            total_original = 0.0
            total_paid = 0.0
            total_due = 0.0
            
            if results:
                for row_data in results:
                    row = self.invoice_table.rowCount()
                    self.invoice_table.insertRow(row)
                    
                    # Get amounts from query results
                    original_amount = float(row_data[2])
                    amount_paid = float(row_data[3])
                    amount_due = float(row_data[4])
                    
                    # Update totals
                    total_original += original_amount
                    total_paid += amount_paid
                    total_due += amount_due
                    
                    # Add items to table
                    items = [
                        str(row_data[0]),  # Invoice ID
                        row_data[1],       # Company
                        f"${original_amount:.2f}",  # Original Amount
                        f"${amount_paid:.2f}",  # Amount Paid
                        f"${amount_due:.2f}",  # Amount Due
                        row_data[5].strftime("%Y-%m-%d"),  # Received Date
                        row_data[6].strftime("%Y-%m-%d"),  # Due Date
                        row_data[7].title(),  # Status
                        row_data[8].strftime("%Y-%m-%d") if row_data[8] else "-"  # Payment Date
                    ]
                    
                    for col, item in enumerate(items):
                        table_item = QtWidgets.QTableWidgetItem(item)
                        table_item.setTextAlignment(QtCore.Qt.AlignCenter)
                        
                        # Color amount due based on value
                        if col == 4:  # Amount Due column
                            if amount_due <= 0:
                                table_item.setForeground(QtGui.QColor("#27ae60"))  # Green for paid
                            else:
                                table_item.setForeground(QtGui.QColor("#c0392b"))  # Red for unpaid
                                
                        self.invoice_table.setItem(row, col, table_item)
                    
                    # Add edit button
                    edit_btn = QtWidgets.QPushButton("Edit")
                    edit_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #3498db;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 5px 10px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
                    """)
                    edit_btn.clicked.connect(lambda checked, r=row: self.edit_invoice(r))
                    self.invoice_table.setCellWidget(row, 9, edit_btn)
            
            # Update total amount label with all three totals
            period_type = "Weekly" if self.is_invoice_weekly_view else "Monthly"
            self.total_invoice_label.setText(
                f"Total {period_type} Invoices: Original: ${total_original:.2f} | "
                f"Paid: ${total_paid:.2f} | Due: ${total_due:.2f}"
            )
            
            # Resize columns to fit content
            self.invoice_table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error loading invoice history: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load invoice history: {e}")

    def edit_invoice(self, row):
        """Edit an invoice record."""
        try:
            invoice_id = int(self.invoice_table.item(row, 0).text())
            
            # Create edit dialog
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Edit Invoice")
            dialog.setFixedWidth(400)
            
            layout = QtWidgets.QFormLayout(dialog)
            
            # Input styling
            input_style = """
                QLineEdit, QComboBox {
                    padding: 8px;
                    border: 2px solid #e0e0e0;
                    border-radius: 6px;
                    font-size: 14px;
                }
            """
            
            # Create input fields
            company_input = QtWidgets.QLineEdit(self.invoice_table.item(row, 1).text())
            company_input.setStyleSheet(input_style)
            
            original_amount_input = QtWidgets.QLineEdit(self.invoice_table.item(row, 2).text().replace('$', ''))
            original_amount_input.setStyleSheet(input_style)
            
            amount_paid_input = QtWidgets.QLineEdit(self.invoice_table.item(row, 3).text().replace('$', ''))
            amount_paid_input.setStyleSheet(input_style)
            
            status_combo = QtWidgets.QComboBox()
            status_combo.addItems(["paid", "unpaid"])
            status_combo.setCurrentText(self.invoice_table.item(row, 7).text().lower())
            status_combo.setStyleSheet(input_style)
            
            # Add fields to layout
            layout.addRow("Company:", company_input)
            layout.addRow("Original Amount:", original_amount_input)
            layout.addRow("Amount Paid:", amount_paid_input)
            layout.addRow("Status:", status_combo)
            
            # Add calculated amount due label that updates when amounts change
            amount_due_label = QtWidgets.QLabel()
            amount_due_label.setStyleSheet("font-weight: bold;")
            layout.addRow("Amount Due:", amount_due_label)
            
            def update_amount_due():
                try:
                    original = float(original_amount_input.text())
                    paid = float(amount_paid_input.text())
                    due = original - paid
                    amount_due_label.setText(f"${due:.2f}")
                    # Update color based on amount
                    if due <= 0:
                        amount_due_label.setStyleSheet("font-weight: bold; color: #27ae60;")
                        status_combo.setCurrentText("paid")
                    else:
                        amount_due_label.setStyleSheet("font-weight: bold; color: #c0392b;")
                        status_combo.setCurrentText("unpaid")
                except ValueError:
                    amount_due_label.setText("Invalid input")
                    amount_due_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
            
            # Connect signals for real-time updates
            original_amount_input.textChanged.connect(update_amount_due)
            amount_paid_input.textChanged.connect(update_amount_due)
            
            # Initialize amount due display
            update_amount_due()
            
            # Add buttons
            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)
            
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                try:
                    # Validate inputs
                    original_amount = float(original_amount_input.text())
                    amount_paid = float(amount_paid_input.text())
                    
                    if original_amount < 0 or amount_paid < 0:
                        raise ValueError("Amounts cannot be negative")
                    
                    if amount_paid > original_amount:
                        raise ValueError("Amount paid cannot exceed original amount")
                    
                    # Update invoice in database
                    query = """
                        UPDATE Invoice 
                        SET company_name = %s,
                            amount = %s,
                            amount_paid = %s,
                            paid_status = %s,
                            payment_date = CASE 
                                WHEN %s = 'paid' OR %s >= %s THEN CURDATE()
                                ELSE NULL
                            END
                        WHERE invoice_id = %s
                    """
                    data = (
                        company_input.text(),
                        original_amount,
                        amount_paid,
                        status_combo.currentText(),
                        status_combo.currentText(),
                        amount_paid,
                        original_amount,
                        invoice_id
                    )
                    success = connect(query, data)
                    
                    if success:
                        QtWidgets.QMessageBox.information(None, "Success", "Invoice updated successfully")
                        self.load_invoice_history()
                    else:
                        raise Exception("Failed to update invoice")
                        
                except ValueError as ve:
                    QtWidgets.QMessageBox.critical(None, "Error", str(ve))
                    
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to edit invoice: {e}")

    def populate_expenses_stores(self):
        """Populate the expenses store combo box with store names and IDs."""
        try:
            print("Attempting to populate expenses stores...")
            query = "SELECT store_id, store_name FROM Store"
            results = connect(query, None)
            
            if results:
                print(f"Found {len(results)} stores")
                self.expenses_store_combo.clear()
                # Add "All Stores" option
                self.expenses_store_combo.addItem("All Stores", -1)
                for store in results:
                    print(f"Adding store: {store[1]} (ID: {store[0]})")
                    self.expenses_store_combo.addItem(store[1], store[0])  # Store name and ID
            else:
                print("No stores found in database")
        except Exception as e:
            print(f"Error populating expenses stores: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to load stores: {e}")


# -----------------------------------------------------------------------------
# Stand‑alone test
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()

    ui = Ui_ManagerDialog()
    ui.setupUi(Dialog)

    Dialog.show()
    sys.exit(app.exec_())

