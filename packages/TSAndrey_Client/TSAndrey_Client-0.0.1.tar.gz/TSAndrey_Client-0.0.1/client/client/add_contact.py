import sys
import logging
sys.path.append('../')
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt

logger = logging.getLogger('client_log')


class AddContactDialog(QDialog):
    """
    Класс - диалог добавления пользователя в список контактов.
    """

    def __init__(self, transport, db):
        super().__init__()
        self.transport = transport
        self.db = db

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Обновить список', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.possible_contacts_update()
        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def possible_contacts_update(self):
        """
        Метод, заполняющий список возможных контактов,
        за исключением уже добавленных в контакты и самого себя.
        """
        self.selector.clear()
        # Получение всех контактов.
        contact_list = set(self.db.get_contacts())
        users_list = set(self.db.get_users())
        # Удаление из списка контактов, пользователя
        users_list.remove(self.transport.user_name)
        # ДОбавление списка возможных контактов.
        self.selector.addItems(sorted(users_list - contact_list))

    def update_possible_contacts(self):
        """
        Метод, обновляющий список возможных контактов. Запрос с сервера
        списка известных пользователей и обновление окна.
        """
        try:
            self.transport.user_list_update()
        except:
            pass
        else:
            logging.info('Обновление списка пользователей выполнено')
            self.possible_contacts_update()
