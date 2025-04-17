from PyQt5 import QtWidgets, QtCore

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("OwnerPage")
        Dialog.resize(900, 600)
        Dialog.setWindowTitle("Owner Page")
        layout = QtWidgets.QVBoxLayout(Dialog)
        label = QtWidgets.QLabel("Welcome to the Owner Page!")
        label.setStyleSheet("font-size: 24px; font-weight: bold;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
