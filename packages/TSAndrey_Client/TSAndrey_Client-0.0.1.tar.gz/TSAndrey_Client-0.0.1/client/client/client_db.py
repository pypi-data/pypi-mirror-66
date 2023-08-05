import os
import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import sys
sys.path.append('../')

class ClientDB:
    """
    Класс - оболочка для работы с базой данных клиента.
    Используется SQLite, применяется SQLAlchemy ORM классический подход.
    """

    class KnownUsers:
        """
        Класс - отображение для таблицы всех пользователей.
        """

        def __init__(self, user):
            self.id = None
            self.user = user

    class MessageHistory:
        """
        Класс - отображение для таблицы статистики переданных сообщений.
        """

        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """Класс - отображение для таблицы контактов."""

        def __init__(self, contacts):
            self.id = None
            self.name = contacts

    # Конструктор класса
    def __init__(self, name):
        # Создание движка бд, так как разрешено несколько потоков,
        # то каждый должен иметь свою бд. Так как модуль многопоточный,
        # то отключена проверка на подключение с разных потоков.
        file_name = f'client_{name}.db3'
        self.engine = create_engine(f'sqlite:///{os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)}',
                                    echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})

        # Создание объекта MetaData
        self.metadata = MetaData()

        # Создание таблицы известных пользователей
        users = Table('Users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user', String, unique=True))

        # Создание таблицы истории сообщений
        message_history = Table('message_history', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('contact', String),
                                Column('direction', String),
                                Column('message', Text),
                                Column('date', DateTime))

        # Создание таблицы контактов
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True))

        # Создание таблиц
        self.metadata.create_all(self.engine)

        # Создание привязок классов к таблицам
        mapper(self.KnownUsers, users)
        mapper(self.MessageHistory, message_history)
        mapper(self.Contacts, contacts)

        # Создание сессии
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Очистка таблицы контактов, так как при при подключении они загружаются с сервера
        self.session.query(self.Contacts).delete()

        # Сохранение изменений
        self.session.commit()

    def add_contact(self, contact):
        """Метод, добавляющий контакт в БД."""
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            new_contact = self.Contacts(contact)
            self.session.add(new_contact)
            self.session.commit()

    def del_contact(self, contact):
        """Метод, удаляющий определенный контакт."""
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        """Метод, заполняющий таблицу известных пользователей."""
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            new_user = self.KnownUsers(user)
            self.session.add(new_user)
        self.session.commit()

    def save_message(self, contact, direction, message):
        """Метод, сохраняющий сообщение в БД."""
        new_message = self.MessageHistory(contact, direction, message)
        self.session.add(new_message)
        self.session.commit()

    def get_contacts(self):
        """Метод, возвращающий список всехконтактов."""
        return [data[0] for data in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """Метод, возвращающий список всех известных пользователей."""
        return [data[0] for data in self.session.query(self.KnownUsers.user).all()]

    def check_user(self, user):
        """Метод, проверяющий существование пользователя."""
        if self.session.query(self.KnownUsers).filter_by(user=user).count():
            return True
        else:
            return False

    def check_contact(self, contact):
        """Метод, проверяющий существование контакта."""
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_history(self, contact):
        """Метод, возвращающий историю сообщений с определенным пользователем."""
        hist = self.session.query(self.MessageHistory).filter_by(contact=contact)
        return [(data.contact, data.direction, data.message, data.date) for data in hist.all()]


if __name__ == '__main__':
    db = ClientDB('user_1')
    for i in ['test1', 'test2', 'test5']:
        db.add_contact(i)
    db.add_users(['user_5', 'user_8', 't1'])
    db.save_message('user_5', 't1', 'Просто сообщение в тесте')

    print(db.get_contacts())
    print(db.get_users())
    print(db.check_contact('a1'))
    print(db.check_user('user_5'))
    print(db.get_history('user_5'))
