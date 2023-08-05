from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import Qt, pyqtSlot
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import base64
import sys
sys.path.append('../')
from client.main_window_conv import Ui_MainClientWindow
from client.add_contact import AddContactDialog
from client.del_contact import DelContactDialog
from conf.variables import *

client_log = logging.getLogger('client_log')


class ClientMainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    Содержит всю логику работы клиентского модуля.
    """

    def __init__(self, db, sock, key):
        super().__init__()
        # Основные переменные
        self.db = db
        self.sock = sock

        # Объект -дешифровщик сообщений с предзагруженным ключем
        self.decryptor = PKCS1_OAEP.new(key)

        # Загрузка конфигурации окна из дизайнера
        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)

        # Кновка выход
        self.ui.menu_exit.triggered.connect(self.client_exit)

        # Кнопка отправить сообщение
        self.ui.btn_send.clicked.connect(self.send_message)

        # Кнопка добавить контакт
        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)

        # Кнопка удалить контакт
        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.menu_del_contact.triggered.connect(self.delete_contact_window)

        # Дополнительные атрибуты
        self.messages = QMessageBox()
        self.contacts_model = None
        self.current_chat = None
        self.current_chat_key = None
        self.encryptor = None
        self.history_model = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        # Войной клик по листу контактов запускает обработчик
        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.client_list_update()
        self.set_disabled_input()
        self.show()

    def client_exit(self):
        """Метод остановки клиента."""
        self.sock.transport_shutdown()
        qApp.exit()

    def set_disabled_input(self):
        """Метод, деактивирующий поле ввода сообщения."""
        self.ui.label_new_message.setText('Для выбора получателя дважды кликните на нем в окне контактов.')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        # Кнопка отправки и поле ввода неактивны до выбора получателя.
        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)
        self.encryptor = None
        self.current_chat = None
        self.current_chat_key = None

    def history_list_update(self):
        """
        Метод, заполняющий QListView
        историей переписки с текущим пользователем.
        """
        # Получение истории переписки, сортированой по датам.
        history = sorted(self.db.get_history(self.current_chat), key=lambda item: item[3])
        # Если модели нет, то создание ее.
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        # Очистка от старых записей.
        self.history_model.clear()

        # Берутся не более 20-ти крайних записей.
        long = len(history)
        start = 0
        if long > 20:
            start = long - 20

        # Заполнение модели записями с разделением на входящие и исходящие.
        for i in range(start, long):
            item = history[i]
            if item[1] == 'in':
                message = QStandardItem(f'Входящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                message.setEditable(False)
                message.setBackground(QBrush(QColor(255, 213, 213)))
                message.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(message)
            else:
                message = QStandardItem(f'Исходящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                message.setEditable(False)
                message.setBackground(QBrush(QColor(204, 255, 204)))
                message.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(message)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        """Метод - обработчик события двойного клика по списку контактов."""
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

    def set_active_user(self):
        """Метод ативации чата с пользователем."""
        # Запрос публичного ключа пользователя и создание объекта шифрования.
        try:
            self.current_chat_key = self.sock.key_request(self.current_chat)
            client_log.info(f'Получен открытый ключ для {self.current_chat}')
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(RSA.import_key(self.current_chat_key))
        except:
            self.current_chat_key = None
            self.encryptor = None
            client_log.info(f'Не удалось получить ключ для {self.current_chat}')

        # Если ключа нет, то ошибка, открыть чат не удалось.
        if not self.current_chat_key:
            self.messages.warning(self, 'Ошибка', 'Для выбранного собеседника нет ключа шифрования')
            return
        # Надпись и активация кнопок.
        self.ui.label_new_message.setText(f'Введите сообщение для {self.current_chat}')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)

        # Заполнение окна истории по текущему пользователю.
        self.history_list_update()

    def client_list_update(self):
        """Метод, обновляющий список контактов."""
        contacts = self.db.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def send_message(self):
        """
        Функция отправки сообщения текущему пользователю.
        Шифрование и отправка.
        """
        # Берется текст из поля и затем поле очищается.
        message = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message:
            return
        # Шифрование сообщения и упаковка в base64.
        message_text_encript = self.encryptor.encrypt(message.encode('utf-8'))
        message_text_encript_base64 = base64.b64encode(message_text_encript)
        try:
            self.sock.send_message(self.current_chat, message_text_encript_base64.decode('ascii'))
            pass
        except:
            self.messages.critical(self, 'Ошибка', '')
        else:
            self.db.save_message(self.current_chat, 'out', message)
            client_log.info(f'Отправлено сообщение для {self.current_chat}: {message}')
            self.history_list_update()

    def add_contact_window(self):
        """Метод,создающий окно - диалог добавления контакта."""
        global select_dialog
        select_dialog = AddContactDialog(self.sock, self.db)
        select_dialog.btn_ok.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, obj):
        """Метод - обработчик нажатия кнопки Добавить."""
        new_contact = obj.selector.currentText()
        self.add_contact(new_contact)
        obj.close()

    def add_contact(self, contact):
        """
        Метод, добавляющий контакт в сервернуюи клиентскую БД.
        После добавления обновляется содержимое окна.
        """
        try:
            self.sock.add_contact(contact)
        except:
            self.messages.critical(self, 'Ошибка', 'Ошибка сервера')
        else:
            self.db.add_contact(contact)
            contact = QStandardItem(contact)
            contact.setEditable(False)
            self.contacts_model.appendRow(contact)
            client_log.info(f'Добавлен контакт {contact}')
            self.messages.information(self, 'Успех', 'Контакт добавлен.')

    def delete_contact_window(self):
        """Метод, создающий окно удаления контакта."""
        global remove_dialog
        remove_dialog = DelContactDialog(self.db)
        remove_dialog.btn_ok.clicked.connect(lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, obj):
        """
        Метод, удаляющий контакт из серверной и клиентской БД.
        После удаления обновляется содержимое окна.
        """
        contact = obj.selector.currentText()
        try:
            self.sock.remove_contact(contact)
        except:
            self.messages.critical(self, 'Ошибка', 'Ошибка сервера')
        else:
            self.db.del_contact(contact)
            self.client_list_update()
            client_log.info(f'Контакт {contact}, удален.')
            self.messages.information(self, 'Успех', ' Контакт удален.')
            obj.close()
            if contact == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    @pyqtSlot(dict)
    def message(self, message):
        """
        Слот обработчик поступаемых сообщений, выполняет дешифровку
        поступаемых сообщений и их сохранение в истории сообщений.
        Запрашивает пользователя если пришло сообщение не от текущего
        собеседника. При необходимости меняет собеседника.
        """
        # Получение строки байтов
        encrypt_message = base64.b64decode(message[MESSAGE_TEXT])

        # Декодирование строки, при ошибкевыдается сообщение и завершение функции.
        try:
            decrypt_message = self.decryptor.decrypt((encrypt_message))
        except:
            self.messages.warning(self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return
        # Сохранение сообщения в БД
        self.db.save_message(self.current_chat, 'in', decrypt_message.decode('utf-8'))
        from_client = message[FROM]

        if from_client == self.current_chat:
            self.history_list_update()
        else:
            # Проверка пользователя в контактах.
            if self.db.check_contact(from_client):
                # Если есть, то запрос о согласии открыть с ним чат.
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {from_client}, открыть с ним чат?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = from_client
                    self.set_active_user()
            else:
                print('NO')
                # Если пользователя нет, то добавляем его в контакты.
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {from_client}.\n \
                                          Его нет в вашем списке контактов.\n Добавить?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(from_client)
                    self.current_chat = from_client
                    # Сохранение сообщения.
                    self.db.save_message(self.current_chat, 'in', decrypt_message.decode('utf-8'))
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        """Слот - обработчик потери соединения с сервером."""
        self.messages.warning(self, 'Сбой соединения', 'Потеряно соединение с сервером. ')
        self.close()

    @pyqtSlot()
    def sig_205(self):
        """Слот, выполняющий обновление БД по команде сервера."""
        if self.current_chat and not self.db.check_user(self.current_chat):
            self.messages.warning(self, 'Упс. . . .', 'Собеседник удален с сервера.')
            self.set_disabled_input()
            self.current_chat = None
        self.client_list_update()

    def make_connection(self, obj):
        """Метод, обеспечивающий соединение сигналов и слотов."""
        obj.new_message.connect(self.message)
        obj.connection_lost.connect(self.connection_lost)
        obj.message_205.connect(self.sig_205)
