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
        cr_table = "CREATE TABLE recipes\
                    (ID SERIAL,\
                    RECIPE_NAME varchar(255) NOT NULL,\
                    INGREDIENTS text NOT NULL,\
                    LINK varchar(255) NOT NULL,\
                    PRIMARY KEY (ID)\
                    );"
        cursor.execute(cr_table)
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_line(name, ingrs, link):
    try:
        connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host="127.0.0.1",
                port="5432",
                database=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO recipes\
                        (RECIPE_NAME, INGREDIENTS, LINK)\
                        VALUES ('{name}', '{ingrs}', '{link}')")
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
        cursor.execute(f"SELECT * FROM recipes WHERE ingredients = '{ingreds}';")
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
