#default libraries
import http.cookiejar
import sys, configparser, json, os.path
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime, timedelta
from threading import Thread
from PIL import Image
from io import BytesIO
import traceback
import base64
import math

#downloaded libraries
try:
    import browser_cookie3
    browsercookieInstalled = True
except:
    browsercookieInstalled = False
from jsonpath_ng.ext import parse
from PyQt5 import QtWidgets, QtTest
from PyQt5.QtCore import QTimer
import faulthandler, requests
import design
import js2py


class breakLoop(Exception): pass


class MainApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        global jsonProfileData
        self.setupUi(self)
        sys.excepthook = self.showExceptionAndExit
        self.pinsFilePath = ''
        self.jsonProfileData = ''
        self.pins = []
        self.uid = 0
        self.limitActivationsMessageBox = QtWidgets.QMessageBox()
        self.limitActivationsMessageBox.setWindowTitle('Error')
        self.groupBoxManuallyCookie.setEnabled(True)
        self.submitCookie.setEnabled(True)
        self.cbxBrowsers.setCurrentText('Моего браузера нету')
        self.btnDialog.clicked.connect(self.browseFolder)
        self.cbxBrowsers.currentTextChanged.connect(self.browserChanged)
        self.submitCookie.clicked.connect(self.parseCookie)
        self.btnStart.clicked.connect(lambda: Thread(target=self.pinsActivation()))

        if browsercookieInstalled == False:
            QtWidgets.QMessageBox.about(self, 'Error', 'Не смог загрузить модуль кук, доступен только ввод куки вручную')
            self.groupBox_3.setEnabled(False)

        if os.path.exists('profileInfo.ini') == False:
            config['DEFAULT'] = {'lastTimeBan': datetime(1970, 1, 1).strftime('%d.%m.%Y %H:%M:%S'),
                                 'lastIndexPin': 0,
                                 'captchaGuruKey': '',
                                 'uid': self.uid
                                 }
            with open('profileInfo.ini', 'w') as configfile:
                config.write(configfile)



    def closeEvent(self, event):
        if self.pins != [] and self.pinsFilePath != '':
            rewriteFilePins(self.pins, self.pinsFilePath)


    def browseFolder(self):
        Tk().withdraw()
        filePath = askopenfilename(filetypes=[('Normal text file', '.txt')])
        if filePath != '':
            self.label.setText(filePath)
            if os.stat(filePath).st_size == 0:
                QtWidgets.QMessageBox.about(self, 'Error', 'Нет пинкодов в файле')
        self.pinsFilePath = filePath
        return filePath


    def browserChanged(self):
        global cookies_dict
        self.cbxNicknames.clear()
        browser = self.cbxBrowsers.currentText().lower()
        try:
            if browser == 'моего браузера нету':
                self.groupBoxManuallyCookie.setEnabled(True)
                self.submitCookie.setEnabled(True)
                return
            elif browser == 'operagx':
                cookies_dict = browser_cookie3.opera(cookie_file=os.path.join(
                    os.getenv('APPDATA', '')) + '\\..\\Roaming\\Opera Software\\Opera GX Stable\\Cookies',
                                                     key_file=os.path.join(
                    os.getenv('APPDATA', '')) + '\\..\\Roaming\\Opera Software\\Opera GX Stable\\Local State',
                                                     domain_name='warface.com')
            elif browser == 'яндекс':
                cookies_dict = browser_cookie3.opera(cookie_file=os.path.join(
                    os.getenv('APPDATA', '')) + '\\..\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies',
                                                     key_file=os.path.join(
                    os.getenv('APPDATA', '')) + '\\..\\Local\\Yandex\\YandexBrowser\\User Data\\Local State',
                                                     domain_name='warface.com')
            elif browser == 'opera':
                cookies_dict = browser_cookie3.opera(domain_name='warface.com')
            elif browser == 'chrome':
                cookies_dict = browser_cookie3.chrome(cookie_file=os.path.join(
                    os.getenv('APPDATA', '')) + '\\..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies', domain_name='warface.com')
            elif browser == 'firefox':
                cookies_dict = browser_cookie3.firefox(domain_name='warface.com')
            elif browser == 'edge':
                cookies_dict = browser_cookie3.edge(domain_name='warface.com')
        except browser_cookie3.BrowserCookieError:
            QtWidgets.QMessageBox.about(self, 'Error', 'Не смог загрузить куки из данного браузера. Проверь, верно ли выбран браузер')
            cookies_dict = {}
            return
        self.groupBoxManuallyCookie.setEnabled(False)
        self.submitCookie.setEnabled(False)
        if cookies_dict.__len__() == 0 and browser != 'моего браузера нету':
            QtWidgets.QMessageBox.about(self, 'Error', 'Не нашел куки варфейса')
            cookies_dict = {}
            self.cbxNicknames.clear()
            return
        self.setupNicknames()


    def parseCookie(self):
        global cookies_dict
        cookiesTxt = self.tbxCookies.toPlainText()
        try:
            cookies_dict = (dict(i.split('=', 1) for i in cookiesTxt.split('; ')))
        except:
            pass
        if cookies_dict.__len__() == 0:
            QtWidgets.QMessageBox.about(self, 'Error', 'Неверно вставил куки')
            cookies_dict = {}
            return
        self.setupNicknames()


    def setupNicknames(self):
        nicknames = []
        self.uid = self.updateSession()
        if self.uid != 0:
            r = requests.get("https://ru.warface.com/dynamic/profile/?a=profile_json",
                             headers=headers, cookies=cookies_dict, allow_redirects=False)
            if r.status_code == 302:
                QtWidgets.QMessageBox.about(self, 'Error', 'Вылезла капча, реши в браузере')
            jsonProfileData = json.loads(r.text)
            self.jsonProfileData = jsonProfileData

            for i in jsonProfileData['chars']:
                nicknames.append(jsonProfileData['chars'][i]['name'])
        if nicknames == []:
            QtWidgets.QMessageBox.about(self, 'Error', 'Не смог получить ники')
            return
        for item in nicknames:
            self.cbxNicknames.addItem(item)


    def checkErrors(self, r, pin):
        global cycle_index
        jsonData = json.loads(r.text)

        if 'reload' in jsonData:
            QtWidgets.QMessageBox.about(self, 'Error', 'Проблема с куками. Попробуй обновить страницу варфейса')
            raise Exception('Cookie error')

        messageError = parse('$.error.message').find(jsonData)[0].value
        if messageError == 'Этот пин-код уже активирован':
            self.listLogs.addItem(f'{str(cycle_index)}. Этот пин-код уже активирован: {pin}')
            self.pins.pop(0)
        elif messageError == 'Вы ввели некорректный пин-код':
            self.listLogs.addItem(f'{str(cycle_index)}. Неверный пин-код: {pin}')
            self.pins.pop(0)
        else:
            rewriteFilePins(self.pins, self.pinsFilePath)
            timeNow = datetime.now()
            lastTimeBan = timeNow.strftime('%d.%m.%Y %H:%M:%S')
            timeUnban = (timeNow + timedelta(hours=1)).strftime('%d.%m.%Y %H:%M:%S')
            QTimer.singleShot(3000, lambda: self.limitActivationsMessageBox.done(0))
            self.limitActivationsMessageBox.setText( f'Мы заметили подозрительную активность на вашем аккаунте и ограничили возможность ввода новых промокодов.'
                                        f'\nВремя блокировки: {lastTimeBan}'
                                        f'\nВ {timeUnban} программа начнет активировать пинкоды снова')
            self.limitActivationsMessageBox.exec_()

            config['DEFAULT'] = {'lastTimeBan': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                                 'lastIndexPin': 0,
                                 'captchaGuruKey': '',
                                 'uid': self.uid
                                 }
            with open('profileInfo.ini', 'w') as configfile:
                config.write(configfile)
            QtTest.QTest.qWait(3600 * 1000)
            self.updateSession()
            raise breakLoop
        cycle_index += 1


    def pinsActivation(self):
        if self.cbxNicknames.currentText() == '':
            QtWidgets.QMessageBox.about(self, 'Error', 'Ты не выбрал никнейм')
            return
        if self.label.text() == 'Выберите файл с пинкодами':
            QtWidgets.QMessageBox.about(self, 'Error', 'Выбери файл с пинкодами')
            return


        config.read('profileInfo.ini')
        if (self.uid == config['DEFAULT']['uid']):
            lastTimeBan = datetime.strptime(config['DEFAULT']['lastTimeBan'], '%d.%m.%Y %H:%M:%S')
            timeNow = datetime.now()
            if (timeNow - lastTimeBan).total_seconds() < 3600:
                QTimer.singleShot(3000, lambda: self.limitActivationsMessageBox.done(0))
                self.limitActivationsMessageBox.setText(
                    f'Мы заметили подозрительную активность на вашем аккаунте и ограничили возможность ввода новых промокодов.'
                    f'\nВремя блокировки: {lastTimeBan}'
                    f'\nВ {lastTimeBan + timedelta(hours=1)} программа начнет активировать пинкоды снова')
                self.limitActivationsMessageBox.exec_()
                timeSleepToUnban = 3605 - (timeNow - lastTimeBan).total_seconds()
                self.groupBox.setEnabled(False)
                self.groupBox_2.setEnabled(False)
                self.groupBox_3.setEnabled(False)
                QtTest.QTest.qWait(int(timeSleepToUnban) * 1000)
                self.groupBox.setEnabled(True)
                self.groupBox_2.setEnabled(True)
                self.groupBox_3.setEnabled(True)
                self.updateSession()
        currentNickname = self.cbxNicknames.currentText()
        jsonpathExpression = parse(f"$.chars[?(@.name=='{currentNickname}')].charId")
        profile_id = jsonpathExpression.find(self.jsonProfileData)[0].value

        allCredits = 0
        cycle_index = 0
        with open(self.pinsFilePath) as filePins:
            self.pins = filePins.readlines()
        [pin for pin in self.pins if pin]
        if self.pins.__len__() == 0:
            QtWidgets.QMessageBox.about(self, 'Error', 'Нет пинкодов в файле')
            return

        try:
            while self.pins.__len__() > 0:
                activateSuccess, pinSuccess = False, False
                while not pinSuccess and self.pins.__len__() > 0:
                    myData = self.pins[0].rstrip()
                    try:
                        pin, countCredits = myData.split(':')
                    except:
                        QtWidgets.QMessageBox.about(self, 'Error', f'Пинкод {myData} не подходящего формата(или не купленные у меня). Закончил активацию')
                        return

                    payload = {'pin': pin}
                    r = requests.post("https://ru.warface.com/dynamic/pin/?a=check_pin", headers=headers,
                                      cookies=cookies_dict,
                                      data=payload, allow_redirects=False)
                    try:
                        json_data = json.loads(r.text)
                        pinSuccess = parse('$.success').find(json_data)[0].value
                    except:
                        pinSuccess = False
                    if pinSuccess: break
                    self.checkErrors(r, pin)
                    app.processEvents()
                while not activateSuccess and self.pins.__len__() > 0:
                    payload = {
                        'pin': pin,
                        'shard_id': '1',
                        'profile_id': profile_id,
                    }
                    r = requests.post("https://ru.warface.com/dynamic/pin/?a=activate_pin", headers=headers,
                                      cookies=cookies_dict,
                                      data=payload, allow_redirects=False)
                    try:
                        json_data = json.loads(r.text)
                        activateSuccess = parse('$.success').find(json_data)[0].value
                    except:
                        activateSuccess = False
                    if activateSuccess: break
                    self.checkErrors(r, pin)
                    app.processEvents()
                if self.pins.__len__() > 0:
                    self.pins.pop(0)
                    allCredits = allCredits + int(countCredits)
                    cycle_index += 1
                    self.listLogs.addItem(f'{str(cycle_index)}. Всего активировано валюты: {str(allCredits)}')
                    app.processEvents()
            rewriteFilePins(self.pins, self.pinsFilePath)
            QtWidgets.QMessageBox.about(self, 'Text', 'Закончил активацию пинкодов')
            self.listLogs.addItem('Закончил активацию пинкодов')
        except breakLoop:
            self.pinsActivation()


    def updateSession(self):
        def part1(base64data):
            dataImage = base64data
            im = Image.open(BytesIO(base64.b64decode(dataImage)))
            h = 0
            for i in range(31, -1, -1):
                c = im.convert('RGB').getpixel((i, 0))
                h *= 2
                if 0 < c[0]: h += 1
            return h

        def part2(n):
            t = math.floor(math.sqrt(n))
            g = 0
            for i in range(3, t, 2):
                g = g + 1
                if n % i == 0:
                    t = math.floor(n / i + i)
                    break
            return t

        print('Обновляю куки')
        r = requests.get("https://ru.warface.com/n.js",
                         headers=headers, cookies=cookies_dict, allow_redirects=False)
        jsfuckT = r.text.split('var t=')[1].split(';')[0]
        cookieN_js_t = r.text.split('n_js_t=')[1].split(';')[0]
        imageData = r.text.split('base64,')[1].split('\'')[0]
        cookieN_js_d = part1(imageData)

        js = 'function abc() {return' + jsfuckT + '} abc()'
        result = js2py.eval_js(js)
        a = part2(int(result))
        cookieN_js_d = str(cookieN_js_d ^ a)

        if type(cookies_dict) is http.cookiejar.CookieJar:
            cookie_obj1 = requests.cookies.create_cookie(domain="ru.warface.com", name="n_js_d", value=cookieN_js_d, secure=True)
            cookie_obj2 = requests.cookies.create_cookie(domain="ru.warface.com", name="n_js_t", value=cookieN_js_t, secure=True)
            cookies_dict.set_cookie(cookie_obj1)
            cookies_dict.set_cookie(cookie_obj2)
        else:
            cookies_dict['n_js_d'] = cookieN_js_d
            cookies_dict['n_js_t'] = cookieN_js_t
        r = requests.get("https://ru.warface.com/dynamic/auth/?a=checkuser", headers=headers, cookies=cookies_dict,
                         allow_redirects=False)
        userInfo = json.loads(r.text)
        if (userInfo['status'] == 0):
            QtWidgets.QMessageBox.about(self, 'Error', 'Ты не вошел в аккаунт')
            return 0

        return json.loads(r.text)['user']['uid']


    def showExceptionAndExit(self, exc_type, exc_value, exc_traceback):
        if self.pins != [] and self.pinsFilePath != '':
            rewriteFilePins(self.pins, self.pinsFilePath)
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        QtWidgets.QMessageBox.about(self, 'Error', f'Ошибка {tb}')
        sys.exit(-1)


def rewriteFilePins(pins, filePath):
    with open(filePath, 'w') as f:
        for item in pins:
            f.write("%s" % item)


sys.tracebacklimit = 0

cookies_dict = {}
cycle_index = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU',
    'Referer': 'https://ru.warface.com/pin/activate'
}
config = configparser.ConfigParser()


def main():
    global app
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    faulthandler.enable()
    main()
