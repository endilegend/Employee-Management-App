from PyQt5 import QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("ManagerPage")
        Dialog.resize(900, 600)
        Dialog.setWindowTitle("Manager Page")
        layout = QtWidgets.QVBoxLayout(Dialog)
        label = QtWidgets.QLabel("Welcome to the Manager Page!")
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
