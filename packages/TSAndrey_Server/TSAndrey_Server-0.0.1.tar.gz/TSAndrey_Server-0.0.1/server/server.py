import os
import logging
import threading

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from conf.decos import log
from server.server_db import ServerDB
from server.main_window import MyWindow
from server.messanger import MessangerClass
from conf.variables import *
from conf.utils import *

server_log = logging.getLogger('server_log')

new_connect = False
con_flag = threading.Lock()


@log
def get_args():
    '''Парсер аргументов коммаднной строки'''
    args = sys.argv
    try:
        if '-p' in args:
            l_port = int(args[args.index('-p') + 1])
        else:
            l_port = DEFAULT_PORT
    except:
        pass
    try:
        if '-a' in args:
            l_addr = int(args[args.index('-a') + 1])
        else:
            l_addr = ''
    except IndexError:
        server_log.critical('Попытка запуска сервера с некорректным адресом ip')
        exit(1)
    return l_addr, l_port


def start():
    """Основная функция модуля server"""
    # Загрузка аргументов коммандной строки
    l_addr, l_port = get_args()
    config = dict()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Имя файла базы данных сервера
    file_name = 'server_db.db3'

    # Чтение настроек сервера из server.ini, если строки пустые, то настройки принимаются по умолчанию.
    # Принятые настройки записываются в файл server.ini.
    with open('server.ini', 'r') as f:
        f_read = f.readlines()
        for i in f_read:
            if '=' in i:
                line = i.split('=')
                config[line[0]] = line[1]
    if 'db_path' not in config.keys() or config['db_path'] == '' or config['db_path'] == '\n':
        config['db_path'] = os.path.join(dir_path, 'server')
    if 'db_file' not in config.keys() or config['db_file'] == '' or config['db_file'] == '\n':
        config['db_file'] = file_name
    if 'default_port' not in config.keys() or config['default_port'] == '' or config['default_port'] == '\n':
        config['default_port'] = str(l_port)
    if 'default_ip' not in config.keys() or config['default_ip'] == '' or config['default_ip'] == '\n':
        config['default_ip'] = l_addr
    for i in config.items():
        if i[1][-1:] == '\n':
            config[i[0]] = i[1][:-1]
    with open(os.path.join(dir_path, 'server.ini'), 'w') as f:
        f.write('SETTINGS\n')
        for i in config.keys():
            f.write(f'{i}={config[i]}\n')

    db_path = os.path.join(config['db_path'], config['db_file'])
    l_addr = config['default_ip']
    l_port = int(config['default_port'])

    # Инициализация базы данных
    db = ServerDB(db_path)

    # Создание экземпляря класса - сервера и его запуск.
    server = MessangerClass(l_addr, l_port, db)
    server.daemon = True
    server.start()

    # Создаем графическое окружение для сервера
    server_app = QApplication(sys.argv)
    server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    mainwindow = MyWindow(db, server, config)

    # Запуск GUI
    server_app.exec_()

    # При закрытии окон остановка обработчика сообщений.
    server.runner = False


if __name__ == '__main__':
    start()
