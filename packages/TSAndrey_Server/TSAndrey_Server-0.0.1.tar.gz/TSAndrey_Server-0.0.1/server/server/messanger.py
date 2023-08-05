import threading
import logging
import os
import select
import json
import hmac
import hashlib
import binascii

from socket import socket, AF_INET, SOCK_STREAM


from conf.metaclasses import MetaServer
from conf.descriptrs import Port
from conf.utils import *

# Загрузка логера
logger = logging.getLogger('server_log')


class MessangerClass(threading.Thread, metaclass=MetaServer):
    """
    Основной класс сервера. Принимает соединения, словари -
    пакеты от пользователей, обрабатывает и пересылает.
    Работает в качестве отдельного потока.
    """
    port = Port()

    def __init__(self, ip, port, db):
        # Конструктор предка.
        super().__init__()

        # Параметры подключения
        self.ip = ip
        self.port = port

        # База данных сервера
        self.db = db

        # Сокет, через который будет осуществляться работа.
        self.sock = None

        # Список подключенных клиентов.
        self.clients = []

        # Флаг продолжения работы.
        self.running = True

        # Словарь: ключ - имя, значение - соответсвующий имени сокет.
        self.names = dict()

        # Сокеты
        self.listen_sockets = None
        self.error_sockets = None

    def run(self):
        """Метод - основной цикл потока"""
        # Инициализация сокета.
        self.init_socket()

        # Основной цикл программы сервера.
        while self.running:
            # Ожидание подключения, если таймаут вышел, то генерируем исключение.
            try:
                client, client_address = self.sock.accept()
            except:
                pass
            else:
                logger.info(f'Установлено соединение с клиентом {client_address}')
                client.settimeout(5)
                self.clients.append(client)
            r = []

            # Проверка на наличие ждущих клиентов
            try:
                if self.clients:
                    r, self.listen_sockets, self.error_sockets = select.select(self.clients, self.clients, [], 0)
            except:
                logger.error(f'Ошибка работы с сокетами')

            # Прием сообщения, если ошибка, то исключение пользователя.
            if r:
                for client in r:
                    try:
                        self.read_message_from_client(get_message(client), client)
                    except:
                        self.remove_client(client)

    def init_socket(self):
        """Метод инициализации сокета."""
        if self.ip == '':
            logger.info(
                f'Запушен сервер: порт - {self.port}, слушает все адреса, максимальное количество клиентов\
                 - {MAX_CONNECTIONS}')
            print(
                f'Запушен сервер: порт - {self.port}, слушает все адреса, максимальное количество клиентов\
                 - {MAX_CONNECTIONS}')
        else:
            logger.info(
                f'Запушен сервер: порт - {self.port}, слушает адрес - {self.ip}, максимальное количество клиентов\
                 - {MAX_CONNECTIONS}')
            print(
                f'Запушен сервер: порт - {self.port}, слушает адрес - {self.ip}, максимальное количество клиентов\
                 - {MAX_CONNECTIONS}')

        # Подготовка сокета.
        transport = socket(AF_INET, SOCK_STREAM)
        transport.bind((self.ip, self.port))
        transport.settimeout(0.5)

        # Начало прослушки сокета.
        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)

    def remove_client(self, client):
        """
        Метод обработчик пользователя, с которым прервана связь.
        Ищет пользователя, удаляет его из списков и базы.
        """
        logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
        for user in self.names:
            if self.names[user] == client:
                self.db.user_logout(user)
                del self.names[user]
                break
        self.clients.remove(client)
        client.close()

    def process_message(self, message):
        """Метод отправки сообщения пользователю."""
        if message[TO] in self.names.keys() and self.names[message[TO]] in self.listen_sockets:
            try:
                send_message(self.names[message[TO]], message)
                logger.info(f'Отправлено сообщение пользователю {message[TO]} от {message[FROM]}')
            except:
                self.remove_client(message[TO])
        elif message[TO] in self.names.keys() and self.names[message[TO]] not in self.listen_sockets:
            logger.error(f'Связь с клиентом {message[TO]} потеряна.')
            self.remove_client(self.names[message[TO]])
        else:
            logger.error(f'Клиент {message[TO]} не зарегистрирован на сервере')

    def read_message_from_client(self, message, client):
        """Метод обработчик поступающих сообщений."""
        logger.info(f'Получено сообщение от клиента: {message}')
        # Если это сообщение о присутсвии, то принимается и отправляется ответ.
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            self.autorize_user(message, client)

        # Если это сообщение, то оправка получателю.
        elif ACTION in message and message[
            ACTION] == MESSAGE and FROM in message and TO in message and TIME in message and \
                MESSAGE_TEXT in message and self.names[message[FROM]] == client:
            if message[TO] in self.names.keys():
                self.db.process_message(message[FROM], message[TO])
                self.process_message(message)
                try:
                    send_message(client, RESPONSE_200)
                except:
                    self.remove_client(client)
            else:
                answer = RESPONSE_400
                answer[ERROR] = 'Получатель не зарегистрирован на сервере'
                try:
                    send_message(client, answer)
                except:
                    pass
            return

        # Если пользователь выходит.
        elif ACTION in message and message[ACTION] == EXIT and USER in message and self.names[message[USER]] == client:
            self.remove_client(client)

        # Если это запрос списка контактов.
        elif ACTION in message and message[ACTION] == GET_CONTACTS \
                and USER in message and self.names[message[USER]] == client:
            answer = RESPONSE_202
            answer[LIST_INFO] = self.db.get_contacts(message[USER])
            try:
                send_message(client, answer)
            except:
                self.remove_client(client)

        # Если это добавление контакта.
        elif ACTION in message and message[ACTION] == ADD_CONTACT and USER in message and ACCOUNT_NAME in message and \
                self.names[message[USER]] == client:
            self.db.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESPONSE_200)
            except:
                self.remove_client(client)

        # Если это удаление контакта.
        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and USER in message and ACCOUNT_NAME in message \
                and self.names[message[USER]] == client:
            self.db.remove_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESPONSE_200)
            except:
                self.remove_client(client)

        # Если это запрс всех известных пользователей.
        elif ACTION in message and message[ACTION] == GET_USERS and USER in message and self.names[message[USER]]\
                == client:
            answer = RESPONSE_202
            answer[LIST_INFO] = [i[0] for i in self.db.users_list()]
            try:
                send_message(client, answer)
            except:
                self.remove_client(client)

        # Если это запрос публичного ключа пользователя.
        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST and USER in message:
            answer = RESPONSE_511
            answer[DATA] = self.db.get_pubkey(message[USER])
            if answer[DATA]:
                try:
                    send_message(client, answer)
                except:
                    self.remove_client(client)
            else:
                answer = RESPONSE_400
                answer[ERROR] = 'Нет публичного ключа'
                try:
                    send_message(client, answer)
                except:
                    self.remove_client(client)

        # Иначе отправка Bad request.
        else:
            answer = RESPONSE_400
            answer[ERROR] = 'Некорректный запрос'
            try:
                send_message(client, answer)
            except:
                self.remove_client(client)

    def autorize_user(self, message, client):
        """Метод реализующий авторизацию пользователя."""
        # Если имя пользователя уже занято, то возврат 400.
        if message[USER][ACCOUNT_NAME] in self.names.keys():
            answer = RESPONSE_400
            answer[ERROR] = 'Такой пользователь уже есть'
            try:
                send_message(client, answer)
            except:
                pass
            self.remove_client(client)
            client.close()

        # Проверка, что пользователь зарегистрирован на сервере.
        elif not self.db.check_user(message[USER][ACCOUNT_NAME]):
            answer = RESPONSE_400
            answer[ERROR] = 'Пользователь не зарегистрирован.'
            try:
                send_message(client, answer)
            except:
                pass
            self.remove_client(client)
            client.close()

        # Иначе ответ 511 и проводится авторизация.
        else:

            # Словарь - зоготовка
            answer = RESPONSE_511

            # Рандомный набот байтов в hex представлении.
            random_str = binascii.hexlify(os.urandom(64))

            # Декодирование байтов в кодировке ascii.
            answer[DATA] = random_str.decode('ascii')

            # Создание хэш пароля и и связки со случайной строкой,
            # сохранение серверной версии ключа.
            hash = hmac.new(self.db.get_hash(message[USER][ACCOUNT_NAME]), random_str)
            digest = hash.digest()

            # Обмен сообщениями с пользователем, если ошиба, то закрывается сокет пользователя.
            try:
                send_message(client, answer)
                answer_from_client = get_message(client)
            except:
                client.close()
                return
            client_digest = binascii.a2b_base64(answer_from_client[DATA])

            # Если ответ пользователя корректный, то сохранение его в список пользователей.
            if RESPONSE in answer_from_client and answer_from_client[RESPONSE] == 511 and \
                    hmac.compare_digest(digest, client_digest):
                self.names[message[USER][ACCOUNT_NAME]] = client
                client_ip, client_port = client.getpeername()
                try:
                    send_message(client, RESPONSE_200)
                except:
                    self.remove_client(message[USER][ACCOUNT_NAME])

                # Добавление пользователя в список активных и если у него изменился ключ,
                # то сохраненние нового.
                self.db.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port, message[USER][PUBLIC_KEY])
            else:
                answer_2 = RESPONSE_400
                answer_2[ERROR] = 'Неверный пароль.'
                try:
                    send_message(client, answer_2)
                except:
                    pass
                self.remove_client(client)
                client.close()

    def service_update_lists(self):
        """Метод реализующий отправки сервисного сообщения 205 пользователям."""
        for i in self.names.keys():
            try:
                send_message(self.names[i], RESPONSE_205)
            except:
                self.remove_client(self.names[i])
