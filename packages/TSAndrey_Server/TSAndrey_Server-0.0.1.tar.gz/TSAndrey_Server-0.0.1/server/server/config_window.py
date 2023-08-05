from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import os


class ConfigWindow(QDialog):
    """Класс- окно настроек сервера."""
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.initUI()

    def initUI(self):
        """Настройка окна."""
        self.setFixedSize(365, 260)
        self.setWindowTitle('Настройки сервера')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        # Надпись о файле базы данных.
        self.db_path_label = QLabel('Путь к файлу базы данных:', self)
        self.db_path_label.move(10, 10)
        self.db_path_label.setFixedSize(240, 15)

        # Строка с путем к базе.
        self.db_path = QLineEdit(self)
        self.db_path.move(10, 30)
        self.db_path.setFixedSize(250, 20)
        self.db_path.setReadOnly(True)

        # Кнопка выбора пути.
        self.db_path_select = QPushButton('Обзор', self)
        self.db_path_select.move(275, 28)
        self.db_path_select.clicked.connect(self.open_file_dialog)

        # Надпись с именем поля файла базы сервера.
        self.db_file_label = QLabel('Имя файла базы данных: ', self)
        self.db_file_label.move(10, 68)
        self.db_file_label.setFixedSize(180, 15)

        # Поле для ввода файла базы данных.
        self.db_file = QLineEdit(self)
        self.db_file.move(200, 66)
        self.db_file.setFixedSize(150, 20)

        # Надпись номер порта.
        self.port_label = QLabel('Номер порта для соединений:', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)

        # Поле для ввода номера порта.
        self.port = QLineEdit(self)
        self.port.move(200, 108)
        self.port.setFixedSize(150, 20)

        # Надпись адрес
        self.ip_label = QLabel('С какого IP принимаем соединения:', self)
        self.ip_label.move(10, 148)
        self.ip_label.setFixedSize(180, 15)

        # Надпись напоминание о пустом поля для адреса.
        self.ip_label_note = QLabel(' оставьте это поле пустым, чтобы\n принимать соединения с любых адресов.', self)
        self.ip_label_note.move(10, 168)
        self.ip_label_note.setFixedSize(500, 30)

        # Пола для ввода ip адреса.
        self.ip = QLineEdit(self)
        self.ip.move(200, 148)
        self.ip.setFixedSize(150, 20)

        # Кнопка сохранения настроек.
        self.save_button = QPushButton('Сохранить', self)
        self.save_button.move(190, 220)

        # Кнопка закрытия окна.
        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(275, 220)
        self.close_button.clicked.connect(self.close)

        self.show()

        self.db_path.insert(self.config['db_path'])
        self.db_file.insert(self.config['db_file'])
        self.port.insert(self.config['default_port'])
        self.ip.insert(self.config['default_ip'])
        self.save_button.clicked.connect(self.save_server_config)

    def open_file_dialog(self):
        """Метод обработчик открытия окна выбора папки."""
        global d
        d = QFileDialog(self)
        path = d.getExistingDirectory()
        path = path.replace('/', '\\')
        self.db_path.insert(path)

    def save_server_config(self):
        """
        Метод сохранения насттроек.
        Проверка правильности введенных данных и
        сохранение их в server.ini.
        """
        global config_window
        message = QMessageBox()
        self.config['db_path'] = self.db_path.text()
        self.config['db_file'] = self.db_file.text()

        try:
            port = int(self.port.text())
        except:
            message.warning(self, 'Ошибка', 'Порт должен быть числом.')
        else:

            self.config['default_ip'] = self.ip.text()
            if 1023 < port < 65536:
                self.config['default_port'] = str(port)
                dir_path = os.path.dirname(os.path.realpath(__file__))
                dir_path=os.path.split(dir_path)[0]
                dir_path=os.path.join(dir_path, 'server.ini')
                with open(dir_path, 'w') as f:
                    f.write('SETTINGS\n')
                    for i in self.config.keys():
                        f.write(f'{i}={self.config[i]}\n')
                message.information(self, 'OK', 'Настройки успешно сохранены')
            else:
                message.warning(self, 'Ошибка', 'Порт должен быть в диапазоне от 1024 до 65535')
