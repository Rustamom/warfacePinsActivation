# warfacePinsActivation
<li>Если вылезла какая-либо ошибка откройте сайт варфейса, подождите минуту и запускайте start.bat</li>
<li>После активации 60 пинкодов подряд у вас выскочит ошибка "Мы заметили подозрительную активность на вашем аккаунте и ограничили возможность ввода новых промокодов". Спустя час можно будет активировать снова</li>
<li>Пинкоды для активации должны храниться в файле pins.txt</li>

<h2>Установка python для работы программы</h2>

<p>Для начала вам необходимо скачать python с помощью данной ссылки: https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe</p>
После запуска установщика, проверьте, чтобы стояли все галочки

![image](https://user-images.githubusercontent.com/48911064/137741630-949eca39-fc32-4642-b0b5-189c2d05e258.png)

<h2>Установка самой программы(для неумеющих пользоваться гитхабом)</h2>
<br>

![image](https://user-images.githubusercontent.com/48911064/138222470-b3d3dd74-2f3e-4fac-b50d-0dff5f195c0f.png)

После распаковки архива переходим в папку с программой и запускаем файл <strong>libraries.bat</strong>(Один раз для установки нужных библиотек).<br>
Откройте сайт <strong>ru.warface.com</strong> и подождите секунд 10-20<br>
Запускаем файл <strong>start.bat</strong> для запуска программы и следуем инструкции

<h2>Работа с программой</h2>
После запуска файла start.bat вам будет необходимо ввести:<br>

1. Ввести имя вашего браузера(или куки, если выбрали "другой")
2. Номер сервера(от 1 до 3, сверху вниз) ![image](https://user-images.githubusercontent.com/48911064/137755294-afae7966-47cb-4ced-a254-b0699806a85f.png) 
3. <a href='#captchaguru'>Captchaguru</a> ключ(необязательно) 

Пример моего ввода:
![image](https://user-images.githubusercontent.com/48911064/141651165-c1c8a6d7-f38f-4d6c-9f3c-69e02b60889d.png)



<h2 name='cookie'>Получение cookie</h2>
<h3>Вся информация представлена для браузера google chrome</h3>
<br><br>

Заходим на сайт warface. Открываем инструменты разработчика(обычно ctrl+shift+i)
, переходим во вкладку сеть(network)![image](https://user-images.githubusercontent.com/48911064/137767184-a7a95625-b618-44ee-9cf8-85766db5495c.png)<br> и обновляем страницу. Находим url(в самом верху страницы) 
<br>
![image](https://user-images.githubusercontent.com/48911064/137767648-bec12a09-6a62-4050-a35c-e8f772566a3f.png)
<br>
Переходим во вкладку заголовки(headers)<br>![image](https://user-images.githubusercontent.com/48911064/137769461-7d5242d2-60eb-4496-867a-c687e920be8d.png)<br>
Листаем вниз и находим заголовок запросов 'Cookie' и копируем его: ПКМ-Копировать значение (ctrl+c не работает)<br>
Вставляем его в программу

<h2 name='captchaguru'>Получение captchaguru ключа</h2>
<h3>Данный ключ нужен в случае появления капчи при активации пинкодов</h3>
<br><br>

Для начала необходимо зарегистрироваться на сайте https://captcha.guru/<br> (Буду благодарен, если зарегистрируетесь по реф.ссылке https://captcha.guru/en/regen/?ref=106261)<br>
ПОПОЛНЯЕТЕ БАЛАНС(5 рублей будет достаточно для активации пинкодов на сумму до 3к кредитов)и копируете ключ с главной страницы<br>
![image](https://user-images.githubusercontent.com/48911064/137770696-696f377a-05cf-4269-b949-c4732f03e714.png)
