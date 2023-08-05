from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel, QApplication, qApp
import sys
sys.path.append('../')

class GetNameDialog(QDialog):
    """
    Класс - стартовый диалог с запросом логина и пароля.
    """

    def __init__(self):
        super().__init__()
        self.ok_press = False
        self.setWindowTitle('Привет')
        self.setFixedSize(175, 135)

        self.label = QLabel('Введите имя пользователя', self)
        self.label.setGeometry(15, 10, 150, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setGeometry(10, 30, 154, 20)

        self.btn_ok = QPushButton('OK', self)
        self.btn_ok.move(10, 105)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 105)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.label_password = QLabel('Введите пароль: ', self)
        self.label_password.move(10, 55)
        self.label_password.setFixedSize(150, 15)

        self.client_password = QLineEdit(self)
        self.client_password.move(10, 75)
        self.client_password.setFixedSize(154, 20)
        self.client_password.setEchoMode(QLineEdit.Password)

        self.show()

    def click(self):
        """Метод - обработчик кнопки ОК"""
        if self.client_name.text() and self.client_password.text():
            self.ok_press = True
            # print('zdlfjhasdf')
            qApp.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = GetNameDialog()

    app.exec_()
