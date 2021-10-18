import requests
from lxml import html
import re
import base64
import time

pins = []
#cookies = input('Вставьте куки\n')
cookies = 'n_js_t=1634561477; n_js_d=2795837954; has_js=1; __atssc=google;1; PHPSESSID=oms6gv1d6g449avf6ufv4ock3q; _gcl_au=1.1.648345722.1634561479; mrcurrentpath=/; tmr_lvid=5c3e829bb3c4cc822012acca129a5216; tmr_lvidTS=1634561479055; _gid=GA1.2.27564497.1634561479; _ym_uid=1634561479628512142; _ym_d=1634561479; _ym_isad=2; _fbp=fb.1.1634561479765.1842899077; _ym_visorc=w; mgrt=372c3fccc5a9727c8f1a313e585400b12fd21d3f37363830; __atuvc=2|42; __atuvs=616d6dc6ccc2b043001; userId=728821799; mrreferer=https://ru.warface.com/; _ga_LF5DZQ3NEX=GS1.1.1634561478.1.1.1634561543.59; mr1lad=616d6e0735e90f65-21_824-21_824-; _ga=GA1.2.1915755414.1634561479; __utma=239333376.1915755414.1634561479.1634561544.1634561544.1;'
yourServer = input('Введите номер сервера\n')
yourServer = int(yourServer)
#yourCaptchaGuruKey = input('Введите ключ капчагуру\n')
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language':'ru-RU'
}

#Установка кук
cookies_dict = {}
allCookies = re.findall(r'\S+;?', cookies)
for cook in allCookies:
    nameCookie = re.findall(r'(\S+)=', cook)[0]
    valueCookie = re.findall(r'=(\S+)', cook)[0]
    cookies_dict[nameCookie] = valueCookie

#Функции
def solveCaptcha(captchaGuruKey):
    headerLocation = ''
    while 'warface' not in headerLocation:
        r = requests.get('https://ru.warface.com/validate/c/0', headers=headers1, cookies=cookies_dict)
        image = base64.b64encode(r.content)
        with open("captcha.png", "wb") as fh:
            fh.write(base64.decodebytes(image))

        files = {'file': open('captcha.png', 'rb')}
        payload = {'key': captchaGuruKey, 'method': 'post'}
        r = requests.post('http://api.captcha.guru/in.php', files=files, data=payload)
        captchaId = r.text[r.text.find('|')+1:]
        captchaAnswer = 'CAPCHA_NOT_READY'
        while captchaAnswer == 'CAPCHA_NOT_READY':
            time.sleep(6)
            r = requests.get('http://api.captcha.guru/res.php?key=' + captchaGuruKey + '&action=get&id=' + captchaId)
            captchaAnswer = r.text
        captchaCode = (r.text[r.text.find('|')+1:])

        r = requests.get('https://ru.warface.com/validate/process.php?captcha_input=' + captchaCode, headers=headers1, cookies=cookies_dict, allow_redirects=False)
        headerLocation = r.headers['Location']
    print('Решил капчу')

def checkErrors():
    bad_cookies = tree.xpath('//*[@class="error-wrap"]')
    if bad_cookies:
        f = open('pins.txt', 'w')
        for item in pins:
            f.write("%s" % item)
        f.close()
        raise Exception("Закрыт сайт или куки устарели")

    savedContent = r.text
    if 'redirect' in savedContent:
        solveCaptcha('f705fdfb650afa20c06adc55f7744dd6')
    else:
        errorText = tree.xpath('//*[@class="pin__error"]/text()')
        f = open('pins.txt', 'w')
        for item in pins:
            f.write("%s" % item)
        f.close()
        raise Exception(errorText)

#Активация пинов
pins=open('pins.txt').readlines()

allCredits = 0
while pins[0] != '':
    myData = pins[0].rstrip()
    pin = re.findall(r'(\w+)', myData)[0]
    countCredits = re.findall(r'\w+\:(\d+)', myData)[0]

    payload = {
        'pin': pin
    }
    r = requests.post("https://ru.warface.com/dynamic/pin/?a=activate", headers=headers1, cookies=cookies_dict, data=payload)
    tree = html.fromstring(r.content)
    profile_id = tree.xpath('//*[@class="pin__server-item"][' + str(yourServer) + ']/input/@id')
    while not profile_id:
        checkErrors()
        r = requests.post("https://ru.warface.com/dynamic/pin/?a=activate", headers=headers1, cookies=cookies_dict, data=payload)
        tree = html.fromstring(r.content)
        profile_id = tree.xpath('//*[@class="pin__server-item"][' + str(yourServer) + ']/input/@id')

    payload = {
        'pin': pin,
        'shard_id':'1',
        'profile_id':profile_id,
        'item':''
    }
    r = requests.post("https://ru.warface.com/dynamic/pin/?a=submit", headers=headers1, cookies=cookies_dict, data=payload)
    tree = html.fromstring(r.content)
    pinSuccess = tree.xpath('//*[@class="pin__success"]')

    while not pinSuccess:
        checkErrors()
        r = requests.post("https://ru.warface.com/dynamic/pin/?a=submit", headers=headers1, cookies=cookies_dict, data=payload)
        tree = html.fromstring(r.content)
        pinSuccess = tree.xpath('//*[@class="pin__success"]')

    pins.pop(0)
    allCredits = allCredits + int(countCredits)
    print('Всего активировано кредитов: ' + str(allCredits))

f = open('pins.txt', 'w')
for item in pins:
    f.write("%s" % item)
f.close()