import datetime

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker


class ServerDB:
    """
    Класс- оболочка для работы с базой данных сервера.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM класическим подходом.
    """

    class AllUsers:
        """Класс - отображение таблицы всех пользователей."""

        def __init__(self, username, password_hash):
            self.name = username
            self.last_session = datetime.datetime.now()
            self.password_hash = password_hash
            self.pubkey = None
            self.id = None

    class ActiveUsers:
        """Класс - отображение таблицы активных пользователей."""

        def __init__(self, user_id, ip_address, port, login_time):
            self.user_id = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    class LoginHistory:
        """Класс - отображение таблицы истории входов пользователей."""

        def __init__(self, name, date, ip_address, port):
            self.name = name
            self.date = date
            self.ip_address = ip_address
            self.port = port
            self.id = None

    class UsersContact:
        """Класс - отображение таблицы контактов пользователей."""

        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    class UsersHistory:
        """Класс - отображение таблицы истории отправки и получения сообщений пользователями."""

        def __init__(self, user, send=0, recv=0):
            self.id = None
            self.user = user
            self.shipped = send
            self.recieved = recv

    def __init__(self, path):
        # Создание движка базы данных
        self.engine = create_engine(
            f'sqlite:///{path}',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})

        # Создание объекта MetaData
        self.metadata = MetaData()

        # Создание таблици пользователей
        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_session', DateTime),
                            Column('password_hash', String),
                            Column('pubkey', Text))

        # Создание таблицы активных пользователей
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user_id', ForeignKey('Users.id'), unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime))

        # Создание таблицы истории входов пользователей
        user_login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date', DateTime),
                                   Column('ip_address', String),
                                   Column('port', Integer))

        # Создание таблицы контактов пользователей
        contacts = Table('Contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('user', ForeignKey('Users.id')),
                         Column('contact', ForeignKey('Users.id')))

        # Создание таблицы статистики пользователей
        users_history = Table('History', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('user', ForeignKey('Users.id')),
                              Column('shipped', Integer),
                              Column('recieved', Integer))

        # Реализация таблиц
        self.metadata.create_all(self.engine)

        # Привязка таблиц к классам - отображениям
        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, user_login_history)
        mapper(self.UsersContact, contacts)
        mapper(self.UsersHistory, users_history)

        # Создание сессии
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Удалениеданных из таблицы активных пользователей
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, user_name, ip_address, port, key):
        """
        Метод выполняющийся при входе пользователя, записывает в базу факт подключения.
        Обновляет открытый ключ пользователя при его изменении.
        """
        # Запрос в таблицу пользователей на наличие там пользователя с таким именем
        simple = self.session.query(self.AllUsers).filter_by(name=user_name)

        # Если имя пользователя присутсвует в таблице, обновляется время подключения
        # и проверяется актуальность ключа. Если пользователь прислал новый ключ,
        # то сохраняем его.
        if simple.count():
            user = simple.first()
            user.last_session = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key
        # Если нет пользователя в таблице пользователей, то генерируется исключение
        else:
            raise print('Пользователь не зарегистрирован')

        # Создается запись в таблицу активных пользователей о факте подключения пользователя.
        active_user = self.ActiveUsers(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(active_user)

        # Создается запись в таблицу истории подключений
        history = self.LoginHistory(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(history)

        # Сохранение изменений
        self.session.commit()

    def add_user(self, name, password_hash):
        """
        Метод регистрации пользователя.
        Принимает имя пользователя и хэш паароля, создает запись в таблице статики.
        """
        user = self.AllUsers(name, password_hash)
        self.session.add(user)
        self.session.commit()
        history = self.UsersHistory(user.id, 0, 0)
        self.session.add(history)
        self.session.commit()

    def remove_user(self, name):
        """Метод удаляющий пользователя из базы."""
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        self.session.query(self.ActiveUsers).filter_by(user_id=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(name=user.id).delete()
        self.session.query(self.UsersContact).filter_by(user=user.id).delete()
        self.session.query(self.UsersHistory).filter_by(user=user.id).delete()
        self.session.query(self.AllUsers).filter_by(name=name).delete()

    def get_hash(self, name):
        """Метод получения хэша пароля пользователя."""
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.password_hash

    def get_pubkey(self, name):
        """Метод получения публичного ключа пользователя."""
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.pubkey

    def user_logout(self, user_name):
        """Метод отключения пользователя."""
        # Запрос отключаемого пользователя
        user = self.session.query(self.AllUsers).filter_by(name=user_name).first()

        # Удаление пользователя из таблицы активных пользователей.
        self.session.query(self.ActiveUsers).filter_by(user_id=user.id).delete()

        # Сохранение изменений
        self.session.commit()

    def check_user(self, name):
        """Метод проверяющий существование пользователя в базе."""
        if self.session.query(self.AllUsers).filter_by(name=name).count():
            return True
        else:
            return False

    def process_message(self, send, recv):
        """Метод записывающий в таблицу статистики факт передачи сообщения."""
        # Получение отправителя и получателя
        send = self.session.query(
            self.AllUsers).filter_by(
            name=send).first()
        recv = self.session.query(
            self.AllUsers).filter_by(
            name=recv).first()
        # Запрос строк изистории и увеличение счетчиков
        sender = self.session.query(self.UsersHistory).filter_by(user=send.id).first()
        sender.shipped += 1
        recipient = self.session.query(self.UsersHistory).filter_by(user=recv.id).first()
        recipient.recieved += 1
        # Сохранение изменений
        self.session.commit()

    def add_contact(self, user, contact):
        """Метод добавления контакта пользователя."""
        # Получение ID пользователя
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()

        # Проверка, что контакта еще нет и что контакт реален
        if not contact or self.session.query(self.UsersContact).filter_by(user=user.id, contact=contact.id).count():
            return

        # Создание объекта - контакт и запись в таблицу
        new_contact = self.UsersContact(user.id, contact.id)
        self.session.add(new_contact)
        self.session.commit()

    def remove_contact(self, user, contact):
        """Метод удаления контакта пользователя."""
        # Получение ID пользователя и контакта
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()

        # Проверка контакта - существует ли он
        if not contact:
            return

        # Удаление записи
        self.session.query(self.UsersContact).filter(
            self.UsersContact.user == user.id,
            self.UsersContact.contact == contact.id).delete()
        self.session.commit()

    def users_list(self):
        """Метод возвращающий список известных пользователей со временем крайнего подключения."""
        # Запрос строк таблицы пользователей.
        user_list = self.session.query(self.AllUsers.name, self.AllUsers.last_session)

        # Возврат списка кортежей
        return user_list.all()

    def active_users_list(self):
        """Метод возвращающий список активных пользователей."""
        # Запрос соединения таблиц и сборка котежа имя, адрес, порт, время.
        users_list = self.session.query(self.AllUsers.name,
                                        self.ActiveUsers.ip_address,
                                        self.ActiveUsers.port,
                                        self.ActiveUsers.login_time).join(self.AllUsers)

        # Возврат списка кортежей
        return users_list.all()

    def login_history(self, user_name=None):
        """Метод возвращающий историю входов."""
        # Запрос истории входов
        history_list = self.session.query(self.AllUsers.name,
                                          self.LoginHistory.date,
                                          self.LoginHistory.ip_address,
                                          self.LoginHistory.port).join(self.AllUsers)

        # Если было указано имя пользователя, то филитрация по нему
        if user_name:
            history_list = history_list.filter(self.AllUsers.name == user_name)

        # Возврат списка кортежей
        return history_list.all()

    def get_contacts(self, user):
        """Метод возвращающий список контактов пользователя."""
        # Запрос пользователя из таблицы пользователей
        user = self.session.query(self.AllUsers).filter_by(name=user).first()

        # Запрос списка контактов пользователя
        contacts_list = self.session.query(self.UsersContact, self.AllUsers.name).filter_by(user=user.id).join(
            self.AllUsers, self.UsersContact.contact == self.AllUsers.id)

        # Возврат имен пользователей
        return [c[1] for c in contacts_list.all()]

    def message_history(self):
        """Метод возвращающий статистику сообщений."""
        message_history_list = self.session.query(self.AllUsers.name, self.AllUsers.last_session,
                                                  self.UsersHistory.shipped, self.UsersHistory.recieved).join(
            self.AllUsers)
        return message_history_list.all()


if __name__ == '__main__':
    a = ServerDB()
    a.user_login('user_1', '192.168.0.5', 6666)
    a.user_login('user_2', '168.192.0.9', 9999)
    print(a.users_list())
    print(a.active_users_list())
    a.user_logout('user_2')
    print(a.active_users_list())
    print(a.login_history('user_1'))
