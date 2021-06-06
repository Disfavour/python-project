"""Данные по бд."""
import configparser
import os


config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + "/recipe_conf.ini")
config.sections()
USER = config["DATABASE"]["USER"]
PASSWORD = config["DATABASE"]["PASSWORD"]
DATABASE = config["DATABASE"]["DATABASE"]

if __name__ == "__main__":
    pass
