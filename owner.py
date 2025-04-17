from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OwnerDialog(object):
    """A PyQt5 owner page UI with modern aesthetics and placeholder frames.
    No backend logic is included – this is strictly the front‑end layout.
    """

    # ----------------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------------
    def setupUi(self, Dialog):
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

        # Static owner name
        owner_name = QtWidgets.QLabel("Owner Name")
        owner_name.setAlignment(QtCore.Qt.AlignCenter)
        owner_name.setStyleSheet(
            """color: white; font-size: 16px; font-weight: bold;"""
        )
        bar_layout.addWidget(owner_name)

        # Static store name (updates if combo changed)
        self.store_name_label = QtWidgets.QLabel("Store Name")
        self.store_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.store_name_label.setStyleSheet(
            """color: white; font-size: 16px; font-weight: bold;"""
        )
        bar_layout.addWidget(self.store_name_label)

        # Store selector – populated with placeholder data
        self.store_combo = QtWidgets.QComboBox()
        self.store_combo.setFixedWidth(200)
        self.store_combo.addItems(["Store A", "Store B", "Store C"])
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
        self.store_combo.currentTextChanged.connect(self.store_name_label.setText)
        bar_layout.addWidget(self.store_combo)

        self.main_layout.addWidget(self.top_bar)

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

        # Create empty placeholder pages
        self.page_invoice = self._add_placeholder_page("Enter Invoice")
        self.page_expense = self._add_placeholder_page("Enter Expense")
        self.page_merchandise = self._add_placeholder_page("Enter Merchandise")
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
