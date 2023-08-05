from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel, QApplication, QMessageBox
from PyQt5.QtCore import QEvent, Qt
import hashlib
import binascii


class RegisterUser(QDialog):
    """Класс - диалог регистрации пользователя на сервере."""

    def __init__(self, db, server):
        super().__init__()
        self.db = db
        self.server = server

        self.setWindowTitle('Регистрация')
        self.setFixedSize(175, 183)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.label_user_name = QLabel('Введите имя пользователя', self)
        self.label_user_name.move(10, 10)
        self.label_user_name.setFixedSize(150, 15)

        self.user_name = QLineEdit(self)
        self.user_name.move(10, 30)
        self.user_name.setFixedSize(154, 20)

        self.label_password = QLabel('Пароль', self)
        self.label_password.move(10, 55)
        self.label_password.setFixedSize(150, 15)

        self.user_password = QLineEdit(self)
        self.user_password.move(10, 75)
        self.user_password.setFixedSize(154, 20)
        self.user_password.setEchoMode(QLineEdit.Password)

        self.label_conf = QLabel('Введите подтверждение', self)
        self.label_conf.move(10, 100)
        self.label_conf.setFixedSize(150, 15)

        self.user_conf = QLineEdit(self)
        self.user_conf.move(10, 120)
        self.user_conf.setFixedSize(154, 20)
        self.user_conf.setEchoMode(QLineEdit.Password)

        self.btn_ok = QPushButton('Сохранить', self)
        self.btn_ok.move(10, 150)
        self.btn_ok.clicked.connect(self.save_data)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 150)
        self.btn_cancel.clicked.connect(self.close)

        self.messages = QMessageBox()

        self.show()

    def save_data(self):
        """Метод проверки правильности ввода и сохраненния в базу нового пользователя."""
        if not self.user_name.text():
            self.messages.critical(self, 'Ошибка', 'Не указано имя пользователя.')
            return
        elif self.user_password.text() != self.user_conf.text() or not self.user_password.text():
            self.messages.critical(self, 'Ошибка', 'Введенные пароли не совпадают')
            return
        elif self.db.check_user(self.user_name.text()):
            self.messages.critical(self, 'Ошибка', 'Такой пользователь уже зарегистрирован.')
            return
        else:
            # Генерация хэш пароля, в качестве соли используется логин в верхнем регистре.
            password_bytes = self.user_password.text().encode('utf-8')
            salt = self.user_name.text().upper().encode('utf-8')
            password_hash = hashlib.pbkdf2_hmac('sha512', password_bytes, salt, 10000)
            self.db.add_user(self.user_name.text(), binascii.hexlify(password_hash))
            self.messages.information(self, 'Успех', 'Пользователь зарегистрирован')

            # Рассылка пользователям сообщения о необходимости обновить списки пользователей.
            self.server.service_update_lists()
            self.close()


if __name__ == '__main__':
    app = QApplication([])
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    dial = RegisterUser(None, None)
    app.exec_()
