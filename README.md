# classBot

Telegram Bot To Manage The Class, you will be able to add students to your bot and the bot will be able to sends notifies
to students subscriber  and each student can get the exam info , homeworks and zoom links and pdf files you will upload it by admin. 

# How To Run The Project

## First Step :

install all requirements using terminal

```bash
pip install -r requirements.txt
```

## Second Step :

- Go to [bot.py](./modules/bot.py) and add your Telegram Token:


```python
from telebot import TeleBot, types


class BOT:
    __API = "PUT YOUR TOKEN HERE"
    bot = TeleBot(__API)
```

## Third Step :

- Go To [db.py](./modules/db.py) and add your database information

```python
import psycopg2
import time


class DB:

    # this method connect with database
    def connect(self):
        self.__con = psycopg2.connect(
            host="your host",
            database='your database', 
            user='your user',
            password='your password', port=5432)
        self.__cur = self.__con.cursor()
```

## Note :

I am using postgresql in this project
and all table I create it in [tables](./modules/tables)

## Forth Step :

Go to [main.py](main.py) and run the file 😁😎

