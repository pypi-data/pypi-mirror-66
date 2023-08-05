import sys
import time
import logging
import json
import threading
import binascii
import hashlib
import hmac
import sys
sys.path.append('../')

from socket import socket, AF_INET, SOCK_STREAM
from PyQt5.QtCore import pyqtSignal, QObject

from conf.variables import *
from conf.utils import send_message, get_message

# Инициализация логера т объект блокировки для работы с сокетом.
logger = logging.getLogger('client_log')
sock_lock = threading.Lock()

class ClientTransport(threading.Thread, QObject):
    """
    Класс, реализующий взаимодействие с сервером.
    """
    # Сигналы: новое сообщение и потеря соединения.
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, ip, port, db, user_name, password, key):
        # Конструкторы предков
        threading.Thread.__init__(self)
        QObject.__init__(self)

        # Класс - БД
        self.db = db

        # Имя пользователя
        self.user_name = user_name

        # Пароль
        self.password = password

        # Набор ключей для шифрования
        self.key = key

        # Сокет для работы с сервером
        self.transport = None

        # Установка соединения
        self.connection_init(port, ip)

        # Обновление таблиц известных пользователей и контактов
        try:
            self.user_list_update()
            self.contact_list_update()
        except:
            logger.critical('Потеряно соединение с сервером')
            raise print('Потеряно соединение с сервером')

        # Флаг продолжения работы транспорта.
        self.running = True

    def connection_init(self, port, ip):
        """Метод, отвечающий за установку соединения с сервером."""
        # Инициализация сокета
        self.transport = socket(AF_INET, SOCK_STREAM)

        # Установка таймаута
        self.transport.settimeout(5)

        # 5 попыток соединения, в случае успеха, ставится флаг True.
        connected = False
        for i in range(5):
            # print(i)
            logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((ip, int(port)))
            except:
                pass
            else:
                connected = True
                break
            time.sleep(1)

        # Если соединение не удалось - исключение
        if not connected:
            logger.critical('Не удалось установить соединение с сервером')
            raise print('Не удалось установить соединение с сервером')

        logger.info('Установлено соединение с сервером')

        # Запуск процедуры авторицации
        # Получение хэш пароля
        password_bytes = self.password.encode('utf-8')
        salt = self.user_name.upper().encode('utf-8')
        password_hash = hashlib.pbkdf2_hmac('sha512', password_bytes, salt, 10000)
        password_hash_string = binascii.hexlify(password_hash)

        # Получение публичного ключа и декодирование его из байтов.
        public_key = self.key.publickey().export_key().decode('ascii')

        # Авторизация на сервере
        with sock_lock:
            message = {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: self.user_name,
                    PUBLIC_KEY: public_key
                }
            }

            # Отправка серверу сообщения - приветсвие.
            try:
                send_message(self.transport, message)
                answer = get_message(self.transport)
                # Если сервер вернул ошибку то генерируется исключение.
                if RESPONSE in answer:
                    if answer[RESPONSE]==400:
                        raise print(answer[ERROR])
                    elif answer[RESPONSE] == 511:
                        # Продолжение процедуры авторизации.
                        answer_data = answer[DATA]
                        hash = hmac.new(password_hash_string, answer_data.encode('utf-8'))
                        digest = hash.digest()
                        client_answer = RESPONSE_511
                        client_answer[DATA] = binascii.b2a_base64(digest).decode('ascii')
                        send_message(self.transport, client_answer)
                        self.read_server_message(get_message(self.transport))
            except:
                logger.critical('Потеряно соединение с сервером!')
                raise print('Потеряно соединение с сервером!')
        logger.info('Соединение с сервером успешно установлено.')



    def key_request(self, user):
        """Метод, запрашиваюший с сервера публичный ключпользователя."""
        logger.info(f'Запрос публичного ключа для {user}')
        messsage = {ACTION: PUBLIC_KEY_REQUEST, TIME: time.time(), USER: user}
        with sock_lock:
            send_message(self.transport, messsage)
            answer = get_message(self.transport)
        if RESPONSE in answer and answer[RESPONSE] == 511:
            return answer[DATA]
        else:
            logger.info(f'Не удалось получить ключ собеседника {user}')

    def read_server_message(self, message):
        """Метод, обрабатывающий постуавющие с сервера сообщения."""
        logger.debug(f'Разбор сообщения от сервера: {message}')

        # Если это подтверждение чего-либо
        if RESPONSE in message:
            if message[RESPONSE] == 511:
                # print(message)
                return message
            elif message[RESPONSE] == 200:
                print(message)
                return
            elif message[RESPONSE] == 400:
                raise print('Ошибка')
            else:
                logger.info(f'Принят неизвестный код подтверждения {message[RESPONSE]}')

        # Если это сообщение от пользователя, то оно добавляется в базу и подается сигнал о новом сообщении
        elif ACTION in message and message[
            ACTION] == MESSAGE and FROM in message and TO in message and MESSAGE_TEXT in message and message[
            TO] == self.user_name:
            logger.info(f'Получено сообщение от пользователя {message[FROM]}:{message[MESSAGE_TEXT]}')
            # self.db.save_message(message[FROM], 'in', message[MESSAGE_TEXT])
            self.new_message.emit(message)

    def contact_list_update(self):
        """Метод обновляющий с сервера список контактов."""
        logger.info(f'Запрос контактов для пользователя {self.user_name}')
        message = {ACTION: GET_CONTACTS, TIME: time.time(), USER: self.user_name}
        logger.info(f'Сформирован запрос {message}')
        with sock_lock:
            send_message(self.transport, message)
            answer = get_message(self.transport)
        logger.info(f'Получент ответ {answer}')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            for i in answer[LIST_INFO]:
                self.db.add_contact(i)
        else:
            logger.info('Не удалось получить список контактов')

    def user_list_update(self):
        """Метод, обновляющий с сервера список пользователей."""
        logger.info(f'Запрос списка пользователей для {self.user_name}')
        message = {
            ACTION: GET_USERS,
            TIME: time.time(),
            USER: self.user_name
        }
        logger.info(f'Создан запрос {message}')
        with sock_lock:
            send_message(self.transport, message)
            answer = get_message(self.transport)
        logger.info(f'Получен ответ {answer}')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            self.db.add_users(answer[LIST_INFO])
        else:
            logger.info('Не удалось получить список пользователей')

    def add_contact(self, contact):
        """Метод, отправляющий на сервер сведения о добавлении контакта."""
        logger.info(f'Создание контакта {contact}')
        message = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.user_name,
            ACCOUNT_NAME: contact
        }
        with sock_lock:
            send_message(self.transport, message)
            self.read_server_message(get_message(self.transport))

    def remove_contact(self, contact):
        """Метод, отправляющий на сервер сообщение об удалении контакта."""
        logger.info(f'Удаление контакта {contact}')
        message = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.user_name,
            ACCOUNT_NAME: contact}
        with sock_lock:
            send_message(self.transport, message)
            self.read_server_message(get_message(self.transport))

    def send_message(self, to, mess):
        """Метод, отправляющий сообщенгия на сервер для пользователя."""
        message = {
            ACTION: MESSAGE,
            FROM: self.user_name,
            TO: to,
            TIME: time.time(),
            MESSAGE_TEXT: mess
        }
        logger.info(f'Создано сообщение : {message}')
        with sock_lock:
            send_message(self.transport, message)
            self.read_server_message(get_message(self.transport))
            logger.info(f'Отправлено сообщение для пользователя {to}')

    def transport_shutdown(self):
        """Метод, уведомляющий сервер о прекращении работы пользователя."""
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            USER: self.user_name
        }
        with sock_lock:
            try:
                send_message(self.transport, message)
            except:
                pass
        logger.info('Сокер закрыт')
        time.sleep(0.5)

    def run(self):
        """Метод, содержащий основной цикл работы транспортного потока."""
        logger.info('Запущен процесс - приемник сооющений с сервера.')
        while self.running:
            time.sleep(1)
            with sock_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_message(self.transport)
                except:
                    continue
                else:
                    logger.info(f'Получено сообщение {message}')
                    self.read_server_message(message)
                finally:
                    self.transport.settimeout(5)
