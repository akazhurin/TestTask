# Test task

1. Клонировать проект в локальный репозиторий:
-  git clone https://github.com/akazhurin/TestTask
2. Создание виртуального окружения Python:
-  python -m venv venv
-  .\venv\Scripts\activate
2. Установить необходимые библиотеки из списка requirements:
-  pip install -r .\requirements.txt
3. Развернуть docker контейнер:
-  docker-compose -f .\docker-compose.yml up
4. Создать базу данных и провести миграции:
-  flask db init
-  flask db migrate
-  flask db upgrade
5. Заполнить базу данных данными из csv файлов:   
-  flask script boostrap-db
6. Запустить приложение:   
-  flask run
