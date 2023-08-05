from PyQt5.QtWidgets import QDialog, QPushButton, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt


class StatWindow(QDialog):
    """Класс - окно сос статистикой пользователей."""
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        # Настройки окна
        self.setWindowTitle('Статистика клиентов')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Кнопка закрытия окна.
        self.btn_close = QPushButton('Закрыть', self)
        self.btn_close.move(250, 650)
        self.btn_close.clicked.connect(self.close)

        # Таблица со статистикой.
        self.stat_table = QTableView(self)
        self.stat_table.move(10, 10)
        self.stat_table.setFixedSize(580, 620)
        self.create_state_model()

    def create_state_model(self):
        """Метод, реализующий заполнение таблицы статистикой пользователей."""
        # Список записей из бд.
        stat_list = self.db.message_history()
        list_table = QStandardItemModel()
        list_table.setHorizontalHeaderLabels(
            ['Имя клиента', "Крайний сеанс", "Кол-во отправленных сообщений", "Кол-во полученных сообщений"])

        for i in stat_list:
            print(i)
            user, last_connect, send, recv = i
            print(user, last_connect, send, recv)
            user = QStandardItem(user)
            user.setEditable(False)
            print(last_connect)
            last_connect = QStandardItem(str(last_connect.replace(microsecond=0)))
            last_connect.setEditable(False)
            print(send)
            send = QStandardItem(str(send))
            send.setEditable(False)
            print(recv)
            recv = QStandardItem(str(recv))
            recv.setEditable(False)

            list_table.appendRow([user, last_connect, send, recv])

        self.stat_table.setModel(list)
        self.stat_table.resizeColumnsToContents()
        self.stat_table.resizeRowsToContents()
