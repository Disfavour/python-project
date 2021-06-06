"""Функции для работы с базой данных."""

import psycopg2
from psycopg2 import Error

import recipes_parsing
from recipe_conf import USER, PASSWORD, DATABASE
import os, gettext

gettext.install("telbot", os.path.dirname(__file__))

ERROR_MESSAGE = _("Ошибка при работе с базой данных ")


def create_base() -> None:
    """Создать базу данных."""
    try:
        con = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432")
        cursor = con.cursor()
        sql_cr_db = "create database postgres_db"
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
        for i in ("recipes", "reminders"):
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
        print("cur_line: ", cur_line)
        if t_name == "recipes":
            cursor.execute(f'INSERT INTO {t_name} (recipe) \
                            VALUES (\'{cur_line}\');')
        elif t_name == "reminders":
            print(line.values())
            cursor.execute(f'INSERT INTO {t_name} (name, date, time, type) \
                                        VALUES (%s,%s,%s,%s);', tuple(line.values()))
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_line(table_name: str) -> None:
    """
    Извлечь запись из таблицы.

    :param table_name: название заполняемой таблицы
    """
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host="127.0.0.1",
            port="5432",
            database=DATABASE)
        cursor = connection.cursor()
        if table_name == "reminders":
            cursor.execute('SELECT reminder from reminders;')
        connection.commit()
        return cursor.fetchone()
    except (Exception, Error) as error:
        print(ERROR_MESSAGE, error)
    finally:
        if connection:
            cursor.close()
            connection.close()


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


if __name__ == "__main__":
    create_table()
