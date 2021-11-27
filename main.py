import sys
import requests
from lxml import html
import re
import base64
import time
import browser_cookie3
import os.path
import colorama
from colorama import Fore, Style
colorama.init()
# Функции
sys.tracebacklimit = 0
def solveCaptcha(captchaGuruKey):
    print('Решаю капчу')
    headerLocation = ''
    while 'warface' not in headerLocation:
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
        captchaCode = (r.text[r.text.find('|') + 1:])

        r = requests.get('https://ru.warface.com/validate/process.php?captcha_input=' + captchaCode, headers=headers1,
                         cookies=cookies_dict, allow_redirects=False)
        headerLocation = r.headers['Location']
    print('Решил капчу')

def checkErrors():
    bad_cookies = tree.xpath('//*[@class="error-wrap"]')
    if bad_cookies:
        f = open('pins.txt', 'w')
        for item in pins:
            f.write("%s" % item)
        f.close()
        raise Exception(Fore.RED + "Закрыт сайт или куки устарели. Обнови страницу")

    if r.status_code == 302:
        if yourCaptchaGuruKey == '':
            raise Exception(Fore.RED + 'Вылезла капча, но ты не ввел ключ')
        solveCaptcha(yourCaptchaGuruKey)
    else:
        errorText = tree.xpath('//*[@class="pin__error"]/text()')
        if errorText[0] == 'Этот пин-код уже активирован':
            pins.pop(0)
            myData = pins[0].rstrip()
            pin = re.findall(r'(\w+)', myData)[0]
            print(errorText[0] + ': ' + pin)
        else:
            f = open('pins.txt', 'w')
            for item in pins:
                f.write("%s" % item)
            f.close()
            raise Exception(Fore.RED + errorText[0])


if os.path.exists('captchaguruKey.txt'):
    with open("captchaguruKey.txt", "r") as f:
        print('Взял ключ из файла captchaguruKey.txt')
        yourCaptchaGuruKey = f.read()
else:
    yourCaptchaGuruKey = input(
        'Введите ключ капчагуру\nПосле ввода ключ будет сохранен в файле captchaguruKey.txt\nОставьте поле пустым, если не хотите, чтобы программа решала капчу\n')
    with open("captchaguruKey.txt", "w") as f:
        f.write(yourCaptchaGuruKey)

browser = (input('Введите ваш браузер из списка(chrome, firefox, opera(не GX), edge, другой)\n')).lower()
if browser == 'другой':
    cookies = input('Вставьте куки\n')
    # Установка кук
    cookies_dict = {}
    allCookies = re.findall(r'\S+;?', cookies)
    for cook in allCookies:
        nameCookie = re.findall(r'(\S+)=', cook)[0]
        valueCookie = re.findall(r'=(\S+)', cook)[0]
        cookies_dict[nameCookie] = valueCookie
elif browser == 'opera':
    cookies_dict = browser_cookie3.opera(domain_name='ru.warface.com')
elif browser == 'chrome':
    cookies_dict = browser_cookie3.chrome(domain_name='ru.warface.com')
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
while pins[0] != '':
    myData = pins[0].rstrip()
    pin = re.findall(r'(\w+)', myData)[0]
    countCredits = re.findall(r'\w+\:(\d+)', myData)[0]

    payload = {
        'pin': pin
    }
    r = requests.post("https://ru.warface.com/dynamic/pin/?a=activate", headers=headers1, cookies=cookies_dict,
                      data=payload, allow_redirects=False)
    tree = html.fromstring(r.content)
    profile_id = tree.xpath('//*[@class="pin__server-item"][' + str(yourServer) + ']/input/@id')
    while not profile_id:
        checkErrors()
        r = requests.post("https://ru.warface.com/dynamic/pin/?a=activate", headers=headers1, cookies=cookies_dict,
                          data=payload)
        tree = html.fromstring(r.content)
        profile_id = tree.xpath('//*[@class="pin__server-item"][' + str(yourServer) + ']/input/@id')

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
    print('Всего активировано кредитов: ' + str(allCredits))

f = open('pins.txt', 'w')
for item in pins:
    f.write("%s" % item)
f.close()
print('Закончил активацию пинов')
