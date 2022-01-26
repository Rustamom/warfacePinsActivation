import sys
import requests
from lxml import html
import re
import base64
import time
try:
    import browser_cookie3
    browsercookieInstalled = True
except:
    browsercookieInstalled = False
import os.path
import colorama
from colorama import Fore, Style
colorama.init()
# Функции
def rewriteFilePins():
    f = open('pins.txt', 'w')
    for item in pins:
        f.write("%s" % item)
    f.close()
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press ENTER to exit.")
    sys.exit(-1)
def solveCaptcha(captchaGuruKey):
    print('Решаю капчу')
    headerLocation = ''
    cycle_index = 0
    while 'warface' not in headerLocation:
        print('Попытка ' + str(cycle_index))
        r = requests.get('https://ru.warface.com/validate/c/0', headers=headers1, cookies=cookies_dict)
        image = base64.b64encode(r.content)
        with open("captcha.png", "wb") as fh:
            fh.write(base64.decodebytes(image))

        files = {'file': open('captcha.png', 'rb')}
        payload = {'key': captchaGuruKey, 'method': 'post'}
        r = requests.post('http://api.captcha.guru/in.php', files=files, data=payload)
        captchaId = r.text[r.text.find('|') + 1:]
        captchaAnswer = 'CAPCHA_NOT_READY'
        while captchaAnswer == 'CAPCHA_NOT_READY':
            time.sleep(6)
            r = requests.get('http://api.captcha.guru/res.php?key=' + captchaGuruKey + '&action=get&id=' + captchaId)
            captchaAnswer = r.text
        if captchaAnswer == 'ERROR_WRONG_USER_KEY': raise Exception(Fore.RED + "Неверный ключ капчагуру")
        captchaCode = (r.text[r.text.find('|') + 1:])

        r = requests.get('https://ru.warface.com/validate/process.php?captcha_input=' + captchaCode, headers=headers1,
                         cookies=cookies_dict, allow_redirects=False)
        headerLocation = r.headers['Location']
        print(captchaCode)
        cycle_index += 1
    print('Решил капчу')
def checkErrors():
    bad_cookies = tree.xpath('//*[@class="error-wrap"]')
    if bad_cookies:
        rewriteFilePins()
        raise Exception(Fore.RED + "Закрыт сайт или куки устарели. Обнови страницу")

    if r.status_code == 302:
        if yourCaptchaGuruKey == '':
            rewriteFilePins()
            raise Exception(Fore.RED + 'Вылезла капча, но ты не ввел ключ')
        solveCaptcha(yourCaptchaGuruKey)
    else:
        errorText = tree.xpath('//*[@class="pin__error"]/text()')
        global cycle_index
        cycle_index += 1
        if errorText[0] == 'Этот пин-код уже активирован':
            global pin
            print(str(cycle_index) + '.Этот пин-код уже активирован' + ': ' + pin)
            pins.pop(0)
            try:
                myData = pins[0].rstrip()
                pin = myData.split(':')[0]
            except:
                pin = ''
        else:
            rewriteFilePins()
            print(Fore.RED + errorText[0])
            time.sleep(3601)

sys.tracebacklimit = 0
sys.excepthook = show_exception_and_exit



if os.path.exists('captchaguruKey.txt'):
    with open("captchaguruKey.txt", "r") as f:
        print('Взял ключ из файла captchaguruKey.txt')
        yourCaptchaGuruKey = f.read()
else:
    yourCaptchaGuruKey = input(
        'Введите ключ капчагуру\nПосле ввода ключ будет сохранен в файле captchaguruKey.txt\nОставьте поле пустым, если не хотите, чтобы программа решала капчу\n')
    with open("captchaguruKey.txt", "w") as f:
        f.write(yourCaptchaGuruKey)
cookies_dict = {}
while cookies_dict == {}:
    if browsercookieInstalled:
        #browser = 'chrome'
        browser = (input('Введите ваш браузер из списка(chrome, firefox, opera(не GX), edge, другой)\n')).lower()
    else:
        print('Модуль browser_cookie3 не был установлен. Доступен только ручной ввод куки')
        browser = 'другой'
    if browser == 'другой':
        cookies = input('Вставьте куки\n')
        # Установка кук
        try:
            allCookies = re.findall(r'\S+;?', cookies)
            for cook in allCookies:
                nameCookie = re.findall(r'(\S+)=', cook)[0]
                valueCookie = re.findall(r'=(\S+)', cook)[0]
                cookies_dict[nameCookie] = valueCookie
        except:
            print('Неверно вставил куки')
    elif browser == 'opera':
        cookies_dict = browser_cookie3.opera(domain_name='ru.warface.com')
    elif browser == 'chrome':
        cookies_dict = browser_cookie3.chrome(cookie_file=os.path.join(
                    os.getenv('APPDATA', '')) + '\\..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies', domain_name='ru.warface.com')
    elif browser == 'firefox':
        cookies_dict = browser_cookie3.firefox(domain_name='ru.warface.com')
    elif browser == 'edge':
        cookies_dict = browser_cookie3.edge(domain_name='ru.warface.com')
pins = []
yourServer = input('Введите номер сервера\n')
yourServer = int(yourServer)
while (yourServer > 3) or (yourServer < 1):
    yourServer = input('Введите номер сервера\n')
    yourServer = int(yourServer)
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU'
}

# Активация пинов
pins = open('pins.txt').readlines()

if not pins or pins[0] == '\n':
    raise Exception(Fore.RED + 'Нет пинов в файле pins.txt')

allCredits = 0
cycle_index = 0
while pins and pins[0] != '\n':
    myData = pins[0].rstrip()
    pin = myData.split(':')[0]
    countCredits = myData.split(':')[1]

    payload = {'pin': pin}
    r = requests.post("https://ru.warface.com/dynamic/pin/?a=activate", headers=headers1, cookies=cookies_dict,
                      data=payload, allow_redirects=False)
    t = r.text
    tree = html.fromstring(r.content)
    profile_id = tree.xpath('//*[@class="pin__server-item"][' + str(yourServer) + ']/input/@id')
    while not profile_id and pin != '':
        checkErrors()
        r = requests.post("https://ru.warface.com/dynamic/pin/?a=activate", headers=headers1, cookies=cookies_dict,
                          data=payload)
        tree = html.fromstring(r.content)
        profile_id = tree.xpath('//*[@class="pin__server-item"][' + str(yourServer) + ']/input/@id')
    if pin == '':
        continue
    payload = {
        'pin': pin,
        'shard_id': '1',
        'profile_id': profile_id,
        'item': ''
    }
    r = requests.post("https://ru.warface.com/dynamic/pin/?a=submit", headers=headers1, cookies=cookies_dict,
                      data=payload)
    tree = html.fromstring(r.content)
    pinSuccess = tree.xpath('//*[@class="pin__success"]')

    while not pinSuccess:
        checkErrors()
        r = requests.post("https://ru.warface.com/dynamic/pin/?a=submit", headers=headers1, cookies=cookies_dict,
                          data=payload)
        tree = html.fromstring(r.content)
        pinSuccess = tree.xpath('//*[@class="pin__success"]')

    pins.pop(0)
    allCredits = allCredits + int(countCredits)
    cycle_index += 1
    print(str(cycle_index) + '.Всего активировано кредитов: ' + str(allCredits))

f = open('pins.txt', 'w')
for item in pins:
    f.write("%s" % item)
f.close()
print('Закончил активацию пинов')