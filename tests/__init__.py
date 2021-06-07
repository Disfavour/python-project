import unittest
from src.recipes import form_answer


class TestBot(unittest.TestCase):

    def test_form_answer(self):
        rec1 = {"name": "Булочки с изюмом",
                "ingrs": ["Мука", "Яйцо куриное", "Изюм"],
                "link": "http://recipe"}
        ans1 = '<b>Булочки с изюмом</b>\nИнгредиенты:\n 1) Мука\n' +\
            '2) Яйцо куриное\n3) Изюм\n\n<a href="http://recipe">Булочки с изюмом</a>'
        self.assertEqual(form_answer(rec1), ans1)
        rec2 = {"name": "Омлет",
                "ingrs": ["Яйцо куриное", "Соль", "Молоко"],
                "link": "http://recipe"}
        ans2 = '<b>Омлет</b>\nИнгредиенты:\n 1) Яйцо куриное\n2) Соль\n'+\
                '3) Молоко\n\n<a href="http://recipe">Омлет</a>'
        self.assertEqual(form_answer(rec2), ans2)
        with self.assertRaises(KeyError):
            form_answer(dict())
