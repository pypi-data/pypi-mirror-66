import logging
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from Cryptodome.PublicKey import RSA

from conf.decos import log
from client.client_db import ClientDB
from client.start_window import GetNameDialog
from client.transport import ClientTransport
import logs.config_client_logs
from conf.variables import *
from client.main_window import ClientMainWindow

# Инициализация клиентского логера
logger = logging.getLogger('client_log')


# Парсер аргументов командной строки
@log
def get_attrs():
    """
    Парсер аргументов коммандной строки, возвращает кортеж из 4 элементов
    адрес сервера, порт, имя пользователя, пароль.
    """
    args = sys.argv
    try:
        if '-p' in args:
            server_port = int(args[args.index('-p') + 1])
        else:
            server_port = DEFAULT_PORT
    except IndexError:
        logger.error(f'В аргументах не указан номер порта сервера')
        print('После параметра "-p" надо указать номер порта сервера')
        exit(1)

    try:
        if '-a' in args:
            server_addr = int(args[args.index('-a') + 1])
        else:
            server_addr = DEFAULT_IP_ADDRESS
    except IndexError:
        logger.error('В аргументах не указан ip адрес сервера')
        print('После параметра "-a" надо указать  ip адрес сервера')
        exit(1)

    try:
        if '-u' in args:
            user_name = args[args.index('-u') + 1]
        else:
            # user_name=input('Введите имя пользователя: ')
            user_name = None
    except IndexError:
        logger.error('В аргументе "-u" долно  быть указано имя клиента')
        exit(1)
    try:
        if '-pass' in args:
            client_password = args[args.index('-pass') + 1]
        else:
            # user_name=input('Введите имя пользователя: ')
            client_password = None
    except IndexError:
        logger.error('В аргументе "-pass" долно  быть указано имя клиента')
        exit(1)


    return server_addr, server_port, user_name, client_password


# Основная функция клиента
if __name__ == '__main__':
    # Загрузка параментов командной строки
    s_addr, s_port, user_name, client_password = get_attrs()

    # Создание клиентскогоприложения
    client_app = QApplication(sys.argv)

    sock = None

    # Если имя или парольне были указаны, то запрос их.
    start_dialog = GetNameDialog()
    if not user_name or not client_password:
        client_app.exec_()
        # Если пользователь заполнил поля и нажал ОК, то сохраняется и удаляется объект,
        # иначе выход
        if start_dialog.ok_press:
            user_name = start_dialog.client_name.text()
            client_password = start_dialog.client_password.text()
        else:
            exit(0)

    #  Запись логов
    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {s_addr} , порт: {s_port}, имя пользователя: {user_name}')

    # Загрузка ключей из файла, если файла нет, то генерация нового ключа.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_key = os.path.join(dir_path, f'{user_name}.key')
    if not os.path.exists(file_key):
        key = RSA.generate(2048, os.urandom)
        with open(file_key, 'wb') as k:
            k.write(key.export_key())
    else:
        with open(file_key, 'rb') as k:
            key = RSA.import_key(k.read())
    key.publickey().export_key()

    # Создание объекта базы данных
    db = ClientDB(user_name)

    # Создание объекта - транспорта и запуск транспортного потока.
    try:
        sock = ClientTransport(s_addr, s_port, db, user_name, client_password, key)

    except:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', 'Ошибка')
        exit(1)
    sock.setDaemon(True)
    sock.start()

    # Удаление объекта диалога
    del start_dialog

    # Создание GUI
    main_window = ClientMainWindow(db, sock, key)
    main_window.make_connection(sock)
    main_window.setWindowTitle(f'Программа -ЧАТ. Клиент - {user_name}')
    client_app.exec_()

    # Закрытие транспорта
    sock.transport_shutdown()
    sock.join()

"""
from socket import *
import sys
from conf.variables import *
from conf.utils import *
import time
import logging
import logs.config_client_logs
from conf.decos import log
import threading
from metaclasses import MetaClient
from client.client_db import ClientDB

sock_lock = threading.Lock()
db_lock = threading.Lock()

client_log = logging.getLogger('client_log')


def help():
    print('help - помощь')
    print('message - отправка сообщения')
    print('exit - выход')
    print('contacts - получение контактов')
    print('edit - редактирование контактов')
    print('history - история переписки')



@log
def get_attrs():
    args = sys.argv
    try:
        if '-p' in args:
            server_port = int(args[args.index('-p') + 1])
        else:
            server_port = DEFAULT_PORT
    except IndexError:
        client_log.error(f'В аргументах не указан номер порта сервера')
        print('После параметра "-p" надо указать номер порта сервера')
        exit(1)

    try:
        if '-a' in args:
            server_addr = int(args[args.index('-a') + 1])
        else:
            server_addr = DEFAULT_IP_ADDRESS
    except IndexError:
        client_log.error('В аргументах не указан ip адрес сервера')
        print('После параметра "-a" надо указать  ip адрес сервера')
        exit(1)

    try:
        if '-u' in args:
            user_name = args[args.index('-u') + 1]
        else:
            user_name = input('Введите имя пользователя')
    except IndexError:
        client_log.error('В аргументе "-u" долно  быть указано имя клиента')
        exit(1)
    return server_addr, server_port, user_name


def get_contacts(sock, user):
    message = {ACTION: GET_CONTACTS, TIME: time.time(), USER: user}
    try:
        send_message(sock, message)
        client_log.info(f'Отравлен запрос всех контактов пользователя {user}')
        answer = get_message(sock)
        if RESPONSE in answer and answer[RESPONSE] == 202:
            return answer[LIST_INFO]
        else:
            print('Ошибка сервера')
    except:
        pass


def get_users(sock, user):
    message = {ACTION: GET_USERS, TIME: time.time(), USER: user}
    send_message(sock, message)
    client_log.info(f'Запрос на получение списка всех пользователей от клиента {user} отправлен')
    # print(f'Запрос на получение списка всех пользователей от клиента {user} отправлен')
    answer = get_message(sock)

    if RESPONSE in answer and answer[RESPONSE]==202:
        # print(answer[LIST_INFO])
        return answer[LIST_INFO]
    else:
        raise ('Ошибка сервера')


def add_contact(sock, user, contact):
    message = {ACTION: ADD_CONTACT, TIME: time.time(), USER: user, ACCOUNT_NAME: contact}
    try:
        send_message(sock, message)
        client_log.info(f'Запрос на добавление контакта {contact} от клиента {self.user_name} отправлен')
        answer = get_message(sock)
        if RESPONSE in answer and answer[RESPONSE] == 200:
            print('Контакт создан')
    except:
        pass


def remove_contact(sock, user, contact):
    message = {ACTION: REMOVE_CONTACT, TIME: time.time(), USER: user, ACCOUNT_NAME: contact}
    try:
        send_message(sock, message)
        answer = get_message(sock)
        if RESPONSE in answer and answer[RESPONSE] == 200:
            print('Контакт удален')

    except:
        pass


class ClientReader(threading.Thread, metaclass=MetaClient):
    def __init__(self, user_name, sock, db):
        self.user_name = user_name
        self.sock = sock
        self.db = db
        super().__init__()

    def run(self):
        while True:
            time.sleep(1)
            with sock_lock:
                try:
                    # print('0')
                    message = get_message(self.sock)
                    # print('1')
                except:
                    # client_log.critical('Соединение с серверов потеряно1')
                    pass
                else:
                    if ACTION in message and message[
                        ACTION] == MESSAGE and FROM in message and TIME in message and MESSAGE_TEXT in message:
                        print(\
                            f'Получено сообщение от пользователя {message[FROM]} \n {message[MESSAGE_TEXT]} \n \nВведите команду, help - помощь:\n')
                        client_log.info(f'Получено сообщение {message[MESSAGE_TEXT]} от пользователя {message[FROM]}')
                        with db_lock:

                            try:
                                self.db.save_message(message[FROM], message[TO], message[MESSAGE_TEXT])
                                self.db.add_contact(message[FROM])
                            except:
                                client_log.error('Ошибка обращения с базой данных')
                    else:
                        pass

                    # elif RESPONSE in message and message[RESPONSE] == 202:
                    #     print(message[LIST_INFO])
                    # elif RESPONSE in message and message[RESPONSE] == 200:
                    #     print(RESPONSE_200)





class ClientWriter(threading.Thread, metaclass=MetaClient):
    def __init__(self, user_name, sock, db):
        self.user_name = user_name
        self.sock = sock
        self.db = db
        super().__init__()

    def create_exit_message(self):
        return {ACTION: EXIT, TIME: time.time(), USER: self.user_name}

    def create_message(self):
        adress = input('Введите получателя сообщения:\n ')
        message = input('Введите сообщение: ')
        # if adress == 'all':
        #     adr = '#all'
        # else:
        adr = adress
        message = {ACTION: MESSAGE, FROM: self.user_name, TO: adr, TIME: time.time(), MESSAGE_TEXT: message}
        client_log.info(f'Создано сообщение {message}')
        with db_lock:
            self.db.save_message(self.user_name, adr, message[MESSAGE_TEXT])
            self.db.add_contact(adr)
        with sock_lock:
            try:
                send_message(self.sock, message)
                client_log.info(f'Сообщение для клиента {adr} отправлено')
                time.sleep(0.2)
            except:
                client_log.critical('Соединение с сервером потеряно12')
                exit(1)

    def edit_contact(self):
        action = input('del- удаление, add- добавление :')
        if action == 'add':
            contact = input('Добавляемый контакт: ')
            if self.db.check_user(contact) and not self.db.check_contact(contact):
                with db_lock:
                    self.db.add_contact(contact)
                with sock_lock:
                    add_contact(self.sock, self.user_name, contact)
        elif action == 'del':
            contact = input('Удаляемый контакт: ')
            with db_lock:
                if self.db.check_user(contact) and self.db.check_contact(contact):
                    self.db.del_contact(contact)
            with sock_lock:
                try:
                    remove_contact(self.sock, self.user_name, contact)
                except:
                    print('Попытка удаления не удаласть')

    def get_history(self):
        action=input('in - входящие сообщения,  out - исходящие сообщения, Enter - все сообщения')
        with db_lock:
            if action=='in':
                message_list=self.db.get_history(to_user=self.user_name)
                for i in message_list:
                    print(f'Сообщение от пользователя: {i[0]} от {i[3]}: \n {i[2]}')
            elif action=='out':
                message_list = self.db.get_history(from_user=self.user_name)
                for i in message_list:
                    print(f'Сообщение пользователю: {i[1]} от {i[3]}: \n {i[2]}')
            else:
                message_list=self.db.get_history()
                for i in message_list:
                    print(f'Сообщение от пользователя: {i[0]}, пользователю {i[1]} от {i[3]}: \n{i[2]} ')



    def run(self):
        print(f'Имя пользователя: {self.user_name}')
        help()
        while True:
            command = input('Введите команду:\n ')
            if command == 'exit':
                send_message(self.sock, self.create_exit_message())
                print('Завершение работы по команде пользователя')
                client_log.info('Завершение работы по команде пользователя')
                time.sleep(0.5)
                break
            elif command == 'help':
                help()
            elif command == 'message':
                self.create_message()
            elif command == 'contacts':
                with db_lock:
                    contacts_list = self.db.get_contacts()
                for i in contacts_list:
                    print(i)
            elif command == 'edit':
                self.edit_contact()
            elif command=='history':
                self.get_history()
            else:
                print('Низвестная команда')


@log
def create_presence_message(account_name):
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    client_log.info(f'Сообщение {PRESENCE} создано')
    return message


def load_db(sock, db, user):
    try:
        users_list = get_users(sock, user)
    except:
        client_log.error('Ошибка запроса списка пользователей')
    else:
        db.add_users(users_list)

    try:
        contact_list = get_contacts(sock, user)
        # print(contact_list)
    except:
        client_log.error('Ошибка запроса списка контактов')
    else:
        if contact_list:
            for i in contact_list:
                db.add_contact(i)


def main():
    server_addr, server_port, user_name = get_attrs()
    client_log.info(f'Запущен клиент {user_name} с параметрами: сервер-{server_addr} , порт - {server_port}')

    sok = socket(AF_INET, SOCK_STREAM)

    sok.connect((server_addr, server_port))
    sok.settimeout(1)
    client_log.info(f' Установлено соединение с сервером по порту {server_port}, по адресу {server_addr}')
    print(f' Установлено соединение с сервером по порту {server_port}, по адресу {server_addr}')
    message_to_server = create_presence_message(user_name)
    send_message(sok, message_to_server)
    client_log.info(f'Сообщение {PRESENCE} отправлено на сервер')

    try:
        answer_from_server = get_message(sok)
        client_log.info(f'Получен ответ от сервера {answer_from_server}')
        print(f'Получен ответ от сервера {answer_from_server}')
        if answer_from_server[RESPONSE] == 400:
            exit(1)
    except:
        # print('Не удалось декодировать сообщение сервера.')
        client_log.error('Получен некорректный ответ от сервера')

        exit(1)
    else:
        db = ClientDB(user_name)
        load_db(sok, db, user_name)
        reader = ClientReader(user_name, sok, db)
        reader.daemon = True
        reader.start()
        # reader.join()

        writer = ClientWriter(user_name, sok, db)
        writer.daemon = True
        writer.start()
        # writer.join()
        client_log.info('Запущены процессы')
        print('Запущены процессы')
        while True:
            time.sleep(1)
            if reader.is_alive() and writer.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
"""
