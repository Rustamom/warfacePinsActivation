# warfacePinsActivation

<li>Пинкоды для активации должны храниться в файле pins.txt</li>
<li>Сайт ru.warface.com должен быть открыт, пока работает программа</li>

<h2>Установка программы</h2>

<p>Для начала вам необходимо скачать python с помощью данной ссылки: https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe</p>
После запуска установщика, проверьте, чтобы стояли все галочки

![image](https://user-images.githubusercontent.com/48911064/137741630-949eca39-fc32-4642-b0b5-189c2d05e258.png)

После установки переходим в папку с программой и вводим в адресную строку "cmd"
![image](https://user-images.githubusercontent.com/48911064/137742862-b611020c-6264-4731-b5f5-590b1d1446ba.png)

Прописываем туда следующие команды:
1. pip install requests (установка нужных библиотек)
2. pip install lxml (установка нужных библиотек)
3. python main.py (Запуск программы)

<h2>Работа с программой</h2>
После ввода команды "python main.py" вам будет необходимо ввести:

1. <a href='#cookie'>Cookie-файлы</a>
2. Номер сервера(от 1 до 3, сверху вниз) ![image](https://user-images.githubusercontent.com/48911064/137755294-afae7966-47cb-4ced-a254-b0699806a85f.png) 
3. <a href='#captchaguru'>Captchaguru</a> ключ


<h2 name='cookie'>Получение cookie-файлов</h2>
<h3>Вся информация представлена для браузера google chrome</h3>
<br><br>

 Заходим в режим инкогнито в браузере и авторизуемся на сайте warface. Открываем инструменты разработчика(обычно ctrl+shift+i)
, переходим во вкладку сеть(network)![image](https://user-images.githubusercontent.com/48911064/137767184-a7a95625-b618-44ee-9cf8-85766db5495c.png)<br> и обновляем страницу. Находим url(в самом верху страницы) 
<br>
![image](https://user-images.githubusercontent.com/48911064/137767648-bec12a09-6a62-4050-a35c-e8f772566a3f.png)
<br>
Переходим во вкладку заголовки(headers)<br>![image](https://user-images.githubusercontent.com/48911064/137769461-7d5242d2-60eb-4496-867a-c687e920be8d.png)<br>
находим заголовок запросов 'Cookie' и копируем его(ПКМ-Копировать значение)<br>
Вставляем его в программу

<h2 name='captchaguru'>Получение captchaguru ключа</h2>
<h3>Данный ключ нужен в случае появления капчи при активации пинкодов</h3>
<br><br>

Для начала необходимо зарегистрироваться на сайте https://captcha.guru/<br> (Буду благодарен, если зарегистрируетесь по реф.ссылке https://captcha.guru/en/regen/?ref=106261)<br>
ПОПОЛНЯЕТЕ БАЛАНС(5 рублей будет достаточно для активации пинкодов на сумму до 3к кредитов)и копируете ключ с главной страницы<br>
![image](https://user-images.githubusercontent.com/48911064/137770696-696f377a-05cf-4269-b949-c4732f03e714.png)

<h2>Особенности активации пинов</h2>
<li>После активации 60 пинкодов подряд у вас выскочит ошибка "Подозрительная активность, поэтому мы ограничили вам возможность активации пинкодов". Спустя час можно будет активировать снова</li>
<li>"Закрыт сайт или куки устарели" - значит вы закрыли сайт варфейса или вам надо заного получить другие куки</li>

С любыми другими ошибками я на стадии тестирования не встречался
