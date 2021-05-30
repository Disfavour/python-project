import psycopg2
from psycopg2 import Error
from recipe_conf import USER, PASSWORD, DATABASE


def create_base():
    try:
        con = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host="127.0.0.1",
                port="5432")
        cursor = con.cursor()
        sql_cr_db = "create database postgres_db"
        cursor.execute(sql_cr_db)
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных ", error)
    finally:
        if con:
            cursor.close()
            con.close()


def create_table():
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


def add_line(recipe):
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


def fetch_by_id(id):
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


def fetch_by_ingreds(ingreds):
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
        return None



if __name__ == "__main__":
    pass
    create_table()
