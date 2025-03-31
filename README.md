## Yatube API

REST API для социальной сети Yatube

## Функциональность

- Аутентификация через JWT
- Добавление и изменение публикаций
- Оставление комментариев к записям
- Возможность подписываться на авторов
- Сообщества для объединения публикаций
- Функции поиска и постраничного вывода

## Технологический стек

- Python 3.9
- SQLite3
- Django 3.2
- Django REST Framework 3.12

## Запуск проекта

* Клонировать репозиторий и перейти в него в командной строке:

        git clone git@github.com:Calorific/api_final_yatube.git
        cd api_final_yatube

* Cоздать и активировать виртуальное окружение:

        python3 -m venv venv
        source venv/Scripts/activate

* Установить зависимости из файла requirements.txt:

        python -m pip install --upgrade pip
        pip install -r requirements.txt

* Выполнить миграции:

        python manage.py migrate
        
* Запустить проект:

        python manage.py runserver

* Перейти на локальный сервер:

        http://127.0.0.1:8000/

