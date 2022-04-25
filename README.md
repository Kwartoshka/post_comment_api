### Инструкция по запуску
Для проверки задачи необходимы следующие шаги:
1. Клонировать проект <br>
`git clone https://github.com/Kwartoshka/post_comment_api.git`
2. Установить зависимости (команда выполняется в корне проекта [где расположен файл manage.py])<br>
`pip install -r requirements.txt`
3. Для поднятия БД запустить Docker-compose (необходим установленный Docker-compose) 
(команда выполняется в корне проекта [где расположен файл manage.py]):<br/>
`sudo docker-compose up -d`
5. Выполнить миграции (команда выполняется в корне проекта [где расположен файл manage.py]):<br>
`python manage.py migrate`
6. Запустить проект (команда выполняется в корне проекта [где расположен файл manage.py]):<br>
`python manage.py runserver`
#### Документация к API расположена по адресу:
`http://127.0.0.1:8000`