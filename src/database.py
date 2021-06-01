"""Функции для работы с базой данных."""

import psycopg2
from psycopg2 import Error
from recipe_conf import USER, PASSWORD, DATABASE


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
        print("Ошибка при работе с базой данных ", error)
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
        cr_table = "CREATE TABLE recipes \
                    (id SERIAL, \
                    recipe JSONB NOT NULL \
                    );"
        cursor.execute(cr_table)
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_line(recipe: dict) -> None:
    """
    Добавить запись в таблицу.

    :param recipe: словарь, содержащий данные о рецепте
    """
    try:
        connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host="127.0.0.1",
                port="5432",
                database=DATABASE)
        cursor = connection.cursor()
        cur_recipe = f"{recipe}".replace("\"", "*").replace("\'", "\"")
        print(cur_recipe)
        cursor.execute(f'INSERT INTO recipes (recipe) \
                        VALUES (\'{cur_recipe}\');')
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных ", error)
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
        print("Ошибка при работе с базой данных ", error)
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
        print("Ошибка при работе с базой данных ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            return res


if __name__ == "__main__":
    create_table()
