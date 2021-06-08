import unittest
from recipes import form_answer
from database import delete_table_data
from parsing import NEWS, AFISHA, HOROSCOPE, WEATHER


class TestBot(unittest.TestCase):

    def test_form_answer(self):
        rec1 = {"name": "Булочки с изюмом",
                "ingrs": ["Мука", "Яйцо куриное", "Изюм"],
                "link": "http://recipe"}
        ans1 = '<b>Булочки с изюмом</b>\nИнгредиенты:\n 1) Мука\n' + \
               '2) Яйцо куриное\n3) Изюм\n\n<a href="http://recipe">Булочки с изюмом</a>'
        self.assertEqual(form_answer(rec1), ans1)
        rec2 = {"name": "Омлет",
                "ingrs": ["Яйцо куриное", "Соль", "Молоко"],
                "link": "http://recipe"}
        ans2 = '<b>Омлет</b>\nИнгредиенты:\n 1) Яйцо куриное\n2) Соль\n' + \
               '3) Молоко\n\n<a href="http://recipe">Омлет</a>'
        self.assertEqual(form_answer(rec2), ans2)
        with self.assertRaises(KeyError):
            form_answer(dict())

    # def test_empty_delete_reminders(self):
    #     self.assertEqual(delete_table_data("reminders"), 0)

    def test_parsing_horoscope(self):
        obj = HOROSCOPE()
        self.assertEqual(obj.url, "https://1001goroskop.ru")

    def test_parsing_horoscope_1(self):
        obj = HOROSCOPE()
        self.assertEqual(type(obj.get_signs()), type([1, 2]))

    def test_parsing_news(self):
        obj = NEWS()
        self.assertEqual(obj.count, None)

    def test_parsing_news_1(self):
        obj = NEWS()
        obj.count = 5
        obj.make_zero()
        self.assertEqual(obj.count, 0)

    def test_parsing_news_2(self):
        obj = NEWS()
        self.assertEqual(obj.url, "https://lenta.ru/parts/news")

    def test_parsing_news_3(self):
        obj = NEWS()
        self.assertEqual(obj.url_part, "https://lenta.ru")

    def test_parsing_news_4(self):
        obj = NEWS()
        self.assertEqual(type(obj.parse()), type([1, 2]))

    def test_parsing_weather(self):
        obj = WEATHER()
        self.assertEqual(type(obj.extra_data), type({}))

    def test_parsing_weather_1(self):
        obj = WEATHER()
        self.assertEqual(obj.url, "https://www.gismeteo.ru")

    def test_parsing_weather_2(self):
        obj = WEATHER()
        self.assertEqual(type(obj.main_data), type({}))

    def test_parsing_afisha(self):
        obj = AFISHA()
        self.assertEqual(obj.cinema_count, None)

    def test_parsing_afisha_1(self):
        obj = AFISHA()
        obj.cinema_count = 1
        obj.make_zero()
        self.assertEqual(obj.cinema_count, 0)

    def test_parsing_afisha_2(self):
        obj = AFISHA()
        obj.theatre_count = 2
        obj.make_zero()
        self.assertEqual(obj.theatre_count, 0)

    def test_parsing_afisha_3(self):
        obj = AFISHA()
        obj.concert_count = 3
        obj.make_zero()
        self.assertEqual(obj.concert_count, 0)

    def test_parsing_afisha_4(self):
        obj = AFISHA()
        obj.cinema_count = 1
        obj.theatre_count = 2
        obj.make_zero()
        self.assertEqual(obj.cinema_count, 0)
        self.assertEqual(obj.theatre_count, 0)

    def test_parsing_afisha_5(self):
        obj = AFISHA()
        obj.cinema_count = 1
        obj.concert_count = 3
        obj.make_zero()
        self.assertEqual(obj.cinema_count, 0)
        self.assertEqual(obj.concert_count, 0)

    def test_parsing_afisha_6(self):
        obj = AFISHA()
        obj.theatre_count = 2
        obj.concert_count = 3
        obj.make_zero()
        self.assertEqual(obj.theatre_count, 0)
        self.assertEqual(obj.concert_count, 0)

    def test_parsing_afisha_total(self):
        obj = AFISHA()
        obj.cinema_count = 1
        obj.theatre_count = 2
        obj.concert_count = 3
        obj.make_zero()
        self.assertEqual(obj.cinema_count, 0)
        self.assertEqual(obj.theatre_count, 0)
        self.assertEqual(obj.concert_count, 0)

