"""Функции для работы с базой данных."""
import datetime

import gettext
import os

import psycopg2
from psycopg2 import Error, extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import recipes_parsing
from read_db_conf import USER, PASSWORD, DATABASE

gettext.install("telbot", os.path.dirname(__file__))

ERROR_MESSAGE = _("Ошибка при работе с базой данных ")


def create_base() -> None:
    """Создать базу данных."""
    try:
        con = psycopg2.connect(
            dbname="postgres",
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432")
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        sql_cr_db = "CREATE DATABASE exp_db;"
        cursor.execute(sql_cr_db)
        con.commit()
    except (Exception, Error) as error:
        print(ERROR_MESSAGE, error)
    finally:
        if con:
            cursor.close()
            con.close()


def create_table() -> None:
    """Создать таблицу в базе данных."""
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432",
            database=DATABASE)
        cursor = connection.cursor()
        for i in ("recipes", "reminders", "shopping_lists"):
            cursor.execute(f'select exists(SELECT * FROM information_schema.tables \
                        WHERE lower(table_name) = lower(\'{i}\'));')
            exist = cursor.fetchone()
            if not exist[0]:
                if i == "recipes":
                    cr_table = "CREATE TABLE recipes \
                                (id SERIAL, \
                                recipe JSONB NOT NULL \
                                );"
                if i == "reminders":
                    cr_table = "CREATE TABLE reminders \
                                (id SERIAL, \
                                name varchar(255), \
                                date varchar(255), \
                                time varchar(255), \
                                type varchar(255) NOT NULL \
                                );"
                if i == "shopping_lists":
                    cr_table = "CREATE TABLE shopping_lists \
                                (id SERIAL, \
                                shopping_list JSONB NOT NULL \
                                );"
                print("created", i, "table")
                cursor.execute(cr_table)
                connection.commit()
            if i == "recipes":
                cursor.execute('SELECT COUNT(*) AS RowCnt FROM recipes;')
                if not cursor.fetchone()[0]:
                    recipes_parsing.parse()
    except (Exception, Error) as error:
        print(ERROR_MESSAGE, error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_line(line: dict, t_name: str) -> None:
    """
    Добавить запись в таблицу.

    :param line: словарь, содержащий добавляемые данные
    :param t_name: название заполняемой таблицы
    """
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432",
            database=DATABASE)
        cursor = connection.cursor()
        cur_line = f"{line}".replace("\"", "*").replace("\'", "\"")
        if t_name == "recipes":

            cursor.execute(f'INSERT INTO {t_name} (recipe) \
                            VALUES (\'{cur_line}\');')
        elif t_name == "reminders":
            cursor.execute(f'INSERT INTO {t_name} (name, date, time, type) \
                                        VALUES (%s,%s,%s,%s);', tuple(line.values()))
        elif t_name == "shopping_lists":
            cursor.execute(f'INSERT INTO {t_name} (shopping_list) \
                            VALUES (\'{cur_line}\');')
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_line_notif(line_data: str):
    """
    Извлечь запись из таблицы.

    :param line_data: запрашиваемая строка
    """
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432",
            database=DATABASE)
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        date_time = datetime.datetime.now()
        hour = '0' + str(date_time.hour) if date_time.hour < 10 else date_time.hour
        minute = '0' + str(date_time.minute) if date_time.minute < 10 else date_time.minute
        day = '0' + str(date_time.day) if date_time.day < 10 else date_time.day
        month = '0' + str(date_time.month) if date_time.month < 10 else date_time.month
        if line_data in ("Мобильная Связь", "Подписки", "ЖКХ"):
            cursor.execute(f'SELECT * from reminders WHERE date = \'{day}\' and ' +
                           f'time = \'{hour}:{minute}\' and type=\'{line_data}\';')
        elif line_data == "Планер":
            cursor.execute(f'SELECT * from reminders WHERE date = \'{date_time.date}\' ' +
                           f'and time = \'{hour}:{minute}\' and type=\'{line_data}\';')
        elif line_data == "День Рождения":
            cursor.execute(f'SELECT * from reminders WHERE date = \'{day}.{month}\' ' +
                           f'and time = \'{hour}:{minute}\' and type=\'{line_data}\';')
        elif line_data == "Приём Лекарств":
            cursor.execute('SELECT * from reminders WHERE ' +
                           f'time = \'{hour}:{minute}\' and type=\'{line_data}\';')
        connection.commit()
    except (Exception, Error) as error:
        print(ERROR_MESSAGE, error)
    finally:
        res = cursor.fetchall()
        if connection:
            cursor.close()
            connection.close()
        return res


def delete_table_data(t_name: str):
    """
    Добавить запись в таблицу.

    :param t_name: название заполняемой таблицы
    """
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432",
            database=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM {t_name};')
        connection.commit()
        cursor.execute(f'SELECT COUNT(*) AS RowCnt FROM {t_name};')
        empty = cursor.fetchone()[0]
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
        return empty


def fetch_by_id(id: int) -> list:
    """
    Получить рецепт по id.

    :param id: идентификатор
    """
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432",
            database=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM recipes WHERE id = {id};")
        res = cursor.fetchall()
    except (Exception, Error) as error:
        print(ERROR_MESSAGE, error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            return res
        return None


def fetch_by_ingreds(ingreds: list) -> list:
    """
    Найти все рецепты с ингредиентами из полученного списка.

    :param ingreds: список ингредиентов
    """
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432",
            database=DATABASE)
        cursor = connection.cursor()
        search = ""
        for ingr in ingreds:
            search += f"recipe -> 'ingrs' ? '{ingr}'"
            if ingr != ingreds[-1]:
                search += " AND "
        cursor.execute(f"SELECT * FROM recipes WHERE {search};")
        res = cursor.fetchall()
    except (Exception, Error) as error:
        print(ERROR_MESSAGE, error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            return res


def take_all() -> list:
    """
    Получить все записи из таблицы списков покупок.

    :param id: идентификатор
    """
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432",
            database=DATABASE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM shopping_lists")
        res = cursor.fetchall()
    except (Exception, Error) as error:
        print(ERROR_MESSAGE, error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            return res
        return None


if __name__ == "__main__":
    create_table()
