from PyQt5 import QtCore, QtGui, QtWidgets
from sqlConnector import connect  # Import the database connection function


class Ui_OwnerDialog(object):
    """A PyQt5 owner page UI with modern aesthetics and placeholder frames.
    No backend logic is included – this is strictly the front‑end layout.
    """

    # ----------------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------------
    def setupUi(self, Dialog, stacked_widget=None, employee_id=None):
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
            QComboBox::down-arrow { image: url(down_arrow.png); width: 12px; height: 12px; }
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
            ("Clock In", "#2ecc71"),
            ("Clock Out", "#e74c3c"),
            ("Enter Invoice", "#16a085"),
            ("Enter Expense", "#c0392b"),
            ("Enter Merchandise", "#8e44ad"),
            ("Employee History", "#2980b9"),
            ("Expenses History", "#d35400"),
            ("Merchandise History", "#2ecc71"),
            ("Gross Profit", "#f1c40f"),
            ("Payroll", "#e67e22"),
            ("Manage Employees", "#95a5a6"),
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
        self.page_clock_in = self._create_clock_in_page()
        self.page_clock_out = self._create_clock_out_page()
        self.page_invoice = self._create_invoice_page()
        self.page_expense = self._create_expense_page()
        self.page_merchandise = self._create_merchandise_page()
        self.page_emp_hist = self._add_placeholder_page("Employee History")
        self.page_exp_hist = self._add_placeholder_page("Expenses History")
        self.page_merch_hist = self._add_placeholder_page("Merchandise History")
        self.page_gross_profit = self._add_placeholder_page("Gross Profit")
        self.page_payroll = self._add_placeholder_page("Payroll")
        self.page_manage_emp = self._add_placeholder_page("Manage Employees")

        mc_layout.addWidget(self.stackedWidget)
        content_layout.addWidget(self.main_content)
        self.main_layout.addWidget(self.content_widget)

        # ---------- Connections ----------
        mapping = {
            "Clock In": self.page_clock_in,
            "Clock Out": self.page_clock_out,
            "Enter Invoice": self.page_invoice,
            "Enter Expense": self.page_expense,
            "Enter Merchandise": self.page_merchandise,
            "Employee History": self.page_emp_hist,
            "Expenses History": self.page_exp_hist,
            "Merchandise History": self.page_merch_hist,
            "Gross Profit": self.page_gross_profit,
            "Payroll": self.page_payroll,
            "Manage Employees": self.page_manage_emp,
        }
        for text, btn in self.sidebar_buttons.items():
            btn.clicked.connect(lambda checked, w=mapping[text]: self.stackedWidget.setCurrentWidget(w))

    def _create_clock_in_page(self):
        """Create the clock in page."""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
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
        self.reg_in_balance = QtWidgets.QLineEdit()
        self.reg_in_balance.setPlaceholderText("Enter Register Balance")
        self.reg_in_balance.setStyleSheet("""
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
        layout.addWidget(self.reg_in_balance)

        # Clock In button
        self.clock_in_btn = QtWidgets.QPushButton("Clock In")
        self.clock_in_btn.setStyleSheet("""
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
        self.clock_in_btn.clicked.connect(self.clock_in)
        layout.addWidget(self.clock_in_btn)

        layout.addStretch()
        self.stackedWidget.addWidget(page)
        return page

    def _create_clock_out_page(self):
        """Create the clock out page."""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
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
        self.reg_out_balance = QtWidgets.QLineEdit()
        self.reg_out_balance.setPlaceholderText("Enter Register Balance")
        self.reg_out_balance.setStyleSheet("""
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
        layout.addWidget(self.reg_out_balance)

        # Clock Out button
        self.clock_out_btn = QtWidgets.QPushButton("Clock Out")
        self.clock_out_btn.setStyleSheet("""
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
        self.clock_out_btn.clicked.connect(self.clock_out)
        layout.addWidget(self.clock_out_btn)

        layout.addStretch()
        self.stackedWidget.addWidget(page)
        return page

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

        # Date input
        self.date_input = QtWidgets.QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QtCore.QDate.currentDate())
        self.date_input.setStyleSheet(input_style)
        date_label = QtWidgets.QLabel("Date")
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

    def submit_invoice(self):
        """Handle the invoice submission."""
        print("Attempting to submit invoice...")
        
        # Validate inputs
        try:
            invoice_id = int(self.invoice_id_input.text())
            date = self.date_input.date().toPyDate()
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
                (invoice_id, company_name, amount_due, due_date, paid_status, payment_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = (
                invoice_id,
                company,
                amount,
                date,
                paid_status,
                date if paid_status == "paid" else None
            )
            print(f"Inserting invoice record. Query: {query}, Data: {data}")
            success = connect(query, data)
            print(f"Invoice insert result: {success}")

            if success:
                QtWidgets.QMessageBox.information(None, "Success", "Invoice submitted successfully.")
                # Clear input fields
                self.invoice_id_input.clear()
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
                (expense_type, expense_date, employee_id)
                VALUES (%s, %s, %s)
            """
            data = (
                expense_type,
                expense_date,
                self.employee_id
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

            # Calculate total price
            total_price = quantity * unit_price

        except ValueError as e:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", str(e))
            print(f"Input validation error: {e}")
            return

        # Insert into database
        try:
            query = """
                INSERT INTO merchandise 
                (merchandise_type, merchandise_date, quantity, unitPrice, totalPrice)
                VALUES (%s, %s, %s, %s, %s)
            """
            data = (
                merchandise_type,
                merchandise_date,
                quantity,
                unit_price,
                total_price
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

    def clock_in(self):
        """Handle the clock-in operation."""
        print(f"Attempting to clock in employee ID: {self.employee_id}")
        
        if not self.employee_id:
            QtWidgets.QMessageBox.critical(None, "Error", "Employee ID is missing. Please log in again.")
            print("Error: Employee ID is missing")
            return

        if not self.store_id:
            QtWidgets.QMessageBox.critical(None, "Error", "Store ID is missing. Please select a store.")
            print("Error: Store ID is missing")
            return

        # Get the current time
        try:
            from datetime import datetime
            current_time = datetime.now()
            print(f"Current time: {current_time}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to get current time: {e}")
            print(f"Error getting current time: {e}")
            return

        # Get the cash-in value from the input
        try:
            reg_in = float(self.reg_in_balance.text())
            print(f"Register in amount: ${reg_in:.2f}")
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "Please enter a valid cash-in amount.")
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
                QtWidgets.QMessageBox.warning(None, "Already Clocked In", "You are already clocked in. Please clock out first.")
                print("Error: Employee already clocked in")
                return
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to check clock-in status: {e}")
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
                QtWidgets.QMessageBox.information(None, "Clock-In Successful", "You have successfully clocked in.")
                self.reg_in_balance.clear()  # Clear the input field
                print("Clock-in successful")
            else:
                QtWidgets.QMessageBox.critical(None, "Clock-In Failed", "An error occurred while clocking in.")
                print("Error: Clock-in insert failed")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to clock in: {e}")
            print(f"Error during clock-in: {e}")

    def clock_out(self):
        """Handle the clock-out operation."""
        print(f"Attempting to clock out employee ID: {self.employee_id}")
        
        if not self.employee_id:
            QtWidgets.QMessageBox.critical(None, "Error", "Employee ID is missing. Please log in again.")
            print("Error: Employee ID is missing")
            return

        if not self.store_id:
            QtWidgets.QMessageBox.critical(None, "Error", "Store ID is missing. Please select a store.")
            print("Error: Store ID is missing")
            return

        # Get the current time
        try:
            from datetime import datetime
            current_time = datetime.now()
            print(f"Current time: {current_time}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to get current time: {e}")
            print(f"Error getting current time: {e}")
            return

        # Get the cash-out value from the input
        try:
            reg_out = float(self.reg_out_balance.text())
            print(f"Register out amount: ${reg_out:.2f}")
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "Please enter a valid cash-out amount.")
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
                QtWidgets.QMessageBox.warning(None, "Not Clocked In", "You are not clocked in. Please clock in first.")
                print("Error: Employee not clocked in")
                return
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to check clock-out status: {e}")
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
                QtWidgets.QMessageBox.information(None, "Clock-Out Successful", "You have successfully clocked out.")
                self.reg_out_balance.clear()  # Clear the input field
                print("Clock-out successful")
            else:
                QtWidgets.QMessageBox.critical(None, "Clock-Out Failed", "An error occurred while clocking out.")
                print("Error: Clock-out update failed")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to clock out: {e}")
            print(f"Error during clock-out: {e}")

    def sign_out(self):
        """Handle the sign-out operation."""
        # Show confirmation dialog
        reply = QtWidgets.QMessageBox.question(
            None,
            'Sign Out',
            'Are you sure you want to sign out?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes and self.stacked_widget:
            # Minimize cleanup operations
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

    def _retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Owner Dashboard"))


# -----------------------------------------------------------------------------
# Stand‑alone test
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()

    ui = Ui_OwnerDialog()
    ui.setupUi(Dialog)

    Dialog.show()
    sys.exit(app.exec_())
