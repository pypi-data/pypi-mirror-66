from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QTableView, QLabel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QTimer

from server.stat_window import StatWindow
from server.config_window import ConfigWindow
from server.add_user import RegisterUser
from server.remove_user import DelUserDialog


class MyWindow(QMainWindow):
    """Класс - основное окно сервера."""

    def __init__(self, db, server, config):
        # Конструктор предка.
        super().__init__()
        # База данных сервера
        self.db = db

        self.server = server
        self.config = config

        # Ярлык выхода
        exitAction = QAction('Выход', self)
        exitAction.triggered.connect(qApp.quit)

        # Кнопка обновление списка пользователей.
        self.refresh_button = QAction('Обновить список', self)

        # Кнопка настроек сервера
        self.config_button = QAction('Настройки сервера', self)

        # Кнопка регистрации пользователя
        self.register_button = QAction('Регистрация пользователя', self)

        # Кнопка удаления пользователя
        self.remove_button = QAction('Удаление пользователя', self)

        # Кнопка вывода истории сообщений
        self.history_button = QAction('История клиентов', self)

        # Статусбар
        self.statusBar()
        self.statusBar().showMessage('Сервер запущен')

        # Тулбар
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.config_button)
        self.toolbar.addAction(self.history_button)
        self.toolbar.addAction(self.register_button)
        self.toolbar.addAction(self.remove_button)

        # Настройки геометрии основного окна.
        self.setFixedSize(800, 600)
        self.setWindowTitle('Программа для обмена сообщениями альфа версия')

        # Надпись - подключенные пользователи.
        self.label = QLabel('Список подключенных клиентов:', self)
        self.label.move(10, 25)
        self.label.setFixedSize(240, 15)

        # Окно со списком подключенных пользователей.
        self.active_client = QTableView(self)
        self.active_client.move(10, 45)
        self.active_client.setFixedSize(780, 400)

        # Таймер, обновляющий список активных пользователей 1 раз в секунду.
        self.timer = QTimer()
        self.timer.timeout.connect(self.create_users_model)
        self.timer.start(1000)

        # Связка кнопок с действияви
        self.refresh_button.triggered.connect(self.create_users_model)
        self.history_button.triggered.connect(self.show_statistic)
        self.config_button.triggered.connect(self.server_config)
        self.register_button.triggered.connect(self.register_user)
        self.remove_button.triggered.connect(self.remove_user)

        # Отображение окна
        self.show()

    def create_users_model(self):
        """Метод, заполняющий таблицу активных пользователей."""
        users_list = self.db.active_users_list()
        active_list = QStandardItemModel()
        active_list.setHorizontalHeaderLabels(['Имя пользователя', 'IP адресс', 'Порт', 'Время подключения'])
        for i in users_list:
            user, ip, port, time = i
            user = QStandardItem(user)
            user.setEditable(False)
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(port)
            port.setEditable(False)
            # Отсекание милисекунд
            time = QStandardItem(str(time.replace(microsecond=0)))
            time.setEditable(False)
            active_list.appendRow([user, ip, port, time])
        self.active_client.setModel(active_list)
        self.active_client.resizeColumnsToContents()
        self.active_client.resizeRowsToContents()

    def show_statistic(self):
        """Метод, создающий окно со статистикой пользователей."""
        global stat_window
        stat_window = StatWindow(self.db)
        stat_window.show()

    def server_config(self):
        """Метод, создающий окно с настройками сервера."""
        global config_window
        config_window = ConfigWindow(self.config)

    def register_user(self):
        """Метод, создающий окно регистрации пользователя."""
        global register_window
        register_window = RegisterUser(self.db, self.server)
        register_window.show()

    def remove_user(self):
        """Метод, создающий окно удаления пользователя."""
        global remove_window
        remove_window = DelUserDialog(self.db, self.server)
        remove_window.show()
