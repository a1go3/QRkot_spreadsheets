# QRKot 2.0.

## Описание:
QRKot - приложение для Благотворительного фонда поддержки котиков. 
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, 
на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, 
связанные с поддержкой кошачьей популяции.

В новой версии добавлена возможность формировать отчёт в гугл-таблицу. 
В таблицу добавляются закрытые проекты, отсортированные по скорости сбора средств: 
от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

<image src="https://i.postimg.cc/zXpzv26s/sprint2-picture1-1672399951.png">

## Возможности приложения:
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, 
которую планируется собрать.
После того как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; 
когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.
Пожертвования. Каждый пользователь может сделать пожертвование и сопроводить его комментарием. 
Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. 
Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. 
Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. 
При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

При отправке POST запроса на /google/ формируется Google таблица в которой 
отражаются закрытые проекты, отсортированные по скорости сбора средств: 
от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

## Используемые технологии:
- Python 3.11
- Fastapi 0.78.0
- Pydantic 1.10.0
- SQLAlchemy 1.4.36
- Fastapi-users 13.0.0
- Aiogoogle 5.12.0

## Настройка и запуск проекта: 
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/tatarenkov-r-v/QRkot_spreadsheets.git
```

```
cd QRkot_spreadsheets
```

Создать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS:

    ```
    source venv/bin/activate
    ```

* Если у вас Windows:

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Либо при помощи poetry:
```
poetry install
```


Создать в корне проекта файл переменных окружения `.env` со следующими переменными:
```
APP_TITLE=Благотворительный фонд поддержки котиков QRKot.
APP_DESCRIPTION=Фонд собирает пожертвования на различные целевые проекты: обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=ctrhtnysqctrhnt
FIRST_SUPERUSER_EMAIL=superuser@mail.ru
FIRST_SUPERUSER_PASSWORD=superpassword
```

Кроме этого, добавьте в файл `.env` данные своего сервисного аккаунта Google:
```
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
EMAIL= 
```

**При первом запуске проекта автоматически создается пользователь с правами super_user.
Данные этого пользователя указаны в .env файле.**

Применить миграции:
```commandline
alembic upgrade head
```

Запустить проект:

```commandline
uvicorn app.main:app
```


## Работа с API:
***
### Проект будет доступен по адресу: http://127.0.0.1:8000/ 
***
***
### Документация доступна по адресу: http://127.0.0.1:8000/docs
***

В проекте есть коллекция запросов для Postman. В директории postman_collection сохранена коллекция запросов для отладки 
и проверки работы текущей версии проекта QRKot.
Импортируйте коллекцию в Postman и выполняйте запросы.
