"""Парсинг."""
from bs4 import BeautifulSoup
import requests
import aiogram.utils.markdown as fmt


class PARSER:
    """Базовый класс парсинга."""

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    multiplier = 2

    def get_soup(self, url: str) -> BeautifulSoup:
        """
        Получить объект BeautifulSoup из ссылки.

        :param url: ссылка
        """
        req = requests.get(url, headers=self.headers)
        return BeautifulSoup(req.text, "lxml")


class HOROSCOPE(PARSER):
    """Парсер гороскопа."""

    def __init__(self):
        """Инициализировать ссылку и получить знаки гороскопа с ссылками."""
        self.url = "https://1001goroskop.ru"
        self.data = self.setup()

    def setup(self) -> dict:
        """Обновить знаки гороскопа с ссылками."""
        soup = self.get_soup(self.url)
        signs = soup.find("ul", class_="zodi_tbl").find_all("a")
        d = {}
        for item in signs:
            text = item.find("strong").text.strip()
            link = self.url + item.get("href")
            d[text] = link
        return d

    def get_signs(self) -> list:
        """Получить список знаков зодиака."""
        return list(self.data.keys())

    def get_data_smart(self, sign: str) -> str:
        """
        Получить прогноз.

        :param sign: знак зодиака
        """
        url = self.data[sign]
        text = self.parse(url)
        text = fmt.hitalic(text)
        text += fmt.hide_link(url)
        return text

    def parse(self, url: str) -> str:
        """
        Получить сырой текст прогноза.

        :param url: ссылка на сайт с нужным знаком зодиака
        """
        soup = self.get_soup(url)
        text = soup.find("table", id="eje_text").find("p").text.strip()
        return text


class NEWS(PARSER):
    """Парсер новостей."""

    def __init__(self):
        """Инициализировать ссылку и счетчик."""
        self.url = "https://lenta.ru/parts/news"
        self.url_part = "https://lenta.ru"
        self.count = None

    def make_zero(self) -> None:
        """Установить счетчик на ноль."""
        self.count = 0

    def get_data_smart(self) -> list:
        """Получить список, содержащий новости."""
        data = self.parse()
        self.count += 1
        if len(data) > (self.count - 1) * self.multiplier:
            cur_data = data[(self.count - 1) * self.multiplier: self.count * self.multiplier]
            text = []
            for title, link in cur_data:
                cur_text = fmt.hlink(title, link)
                text.append(cur_text)
            return text

    def parse(self) -> list:
        """Получить список сырых данных."""
        soup = self.get_soup(self.url)
        many_news = soup.find("div", class_="b-longgrid-column").find_all("div", class_="item news")
        ans = []
        for item in many_news:
            text = item.find("div", class_="titles").find("a").text.strip()
            link = self.url_part + item.find("div", class_="titles").find("a").get("href")
            ans.append([text, link])
        return ans


class WEATHER(PARSER):
    """Парсер погоды."""

    def __init__(self):
        """Инициализировать ссылку и данные."""
        self.url = "https://www.gismeteo.ru"
        self.main_data = {
            "Температура": None,
            "Описание": None,
        }
        self.extra_data = {}

    def get_data_smart(self) -> str:
        """Получить информацию о погоде."""
        self.get_data()
        text = ""
        for key, value in self.main_data.items():
            text += fmt.hbold(fmt.quote_html(key)) + ": " + fmt.hitalic(fmt.quote_html(value))
            text += "\n"
        for key, value in self.extra_data.items():
            text += fmt.hbold(fmt.quote_html(key)) + ": " + fmt.hitalic(fmt.quote_html(value))
            text += "\n"
        text += fmt.hide_link(self.url)
        return text

    def get_data(self) -> None:
        """Записать информацию о погоде в объект класса."""
        base_info, extra_info = self.parse()
        self.main_data["Температура"] = base_info[0]
        self.main_data["Описание"] = base_info[1]
        for i in range(6):
            self.extra_data[extra_info[i][0]] = extra_info[i][1]

    def parse(self) -> tuple:
        """Получить сырую информацию о погоде."""
        soup = self.get_soup(self.url)
        table = soup.find("div", class_="wn_body")

        base_info = self.get_base_info(table)
        table_1_info = self.get_info_1(table)
        table_2_info = self.get_info_2(table)

        return base_info, table_1_info + table_2_info

    def get_base_info(self, soup: BeautifulSoup) -> tuple:
        """Получить температуру и описание."""
        cur_temp = soup.find("div", class_="temperature").find("span", class_="unit_temperature_c").text.strip()
        cur_descr = soup.find("div", class_="_description").find("div", class_="gray").text.strip()
        return cur_temp, cur_descr

    def get_info_1(self, soup: BeautifulSoup) -> list:
        """Получить ощущаемую температуру и скорость ветра."""
        ans = []
        small_table_1 = soup.find("div", class_="_attention").find_all("div", class_="clearfix")

        base_feel = small_table_1[0]
        feel = base_feel.find("div", class_="info_label").text.strip()
        feel_temp = base_feel.find("div", class_="info_value").find("span", class_="unit_temperature_c").text.strip()
        ans.append([feel, feel_temp])

        base_wind = small_table_1[1]
        wind = base_wind.find("div", class_="info_label").text.strip()
        wind_speed = base_wind.find("div", class_="info_value").find("span", class_="unit_wind_m_s").text.strip()
        ans.append([wind, wind_speed])

        return ans

    def get_info_2(self, soup: BeautifulSoup) -> list:
        """Получить давление, влажность, геомагнитную активность, температуру воды."""
        ans = []
        small_table_2 = soup.find("div", class_="opened").find_all("div", class_="clearfix")

        base_pressure = small_table_2[0]
        pressure = base_pressure.find("div", class_="info_label").text.strip()
        pressure_count = base_pressure.find("div", class_="info_value").find(
            "span", class_="unit_pressure_mm_hg_atm").text.strip()
        ans.append([pressure, pressure_count])

        base_humidity = small_table_2[1]
        humidity = base_humidity.find("div", class_="info_label").text.strip()
        humidity_count = base_humidity.find("div", class_="info_value").text.strip()
        ans.append([humidity, humidity_count])

        base_geomagn_act = small_table_2[2]
        geomagn_act = base_geomagn_act.find("div", class_="info_label").find("a").text.strip()
        geomagn_act_count = base_geomagn_act.find("div", class_="info_value").text.strip()
        ans.append([geomagn_act, geomagn_act_count])

        base_water_temp = small_table_2[3]
        water_temp = base_water_temp.find("div", class_="info_label").text.strip()
        water_temp_count = base_water_temp.find("div", class_="info_value").find(
            "span", class_="unit_temperature_c").text.strip()
        ans.append([water_temp, water_temp_count])

        return ans


class AFISHA(PARSER):
    """Парсер афиши."""

    def __init__(self):
        """Инициализировать ссылку и данные."""
        self.options = [
            "Кино", "Театр", "Концерт"
        ]
        self.url = "https://www.afisha.ru"
        self.max_info_count = 1

        self.url_cinema = "https://www.afisha.ru/msk/schedule_cinema"
        self.cinema_count = None
        self.all_cinema_data = []

        self.url_theatre = "https://www.afisha.ru/msk/schedule_theatre"
        self.theatre_count = None
        self.all_theatre_data = []

        self.url_concert = "https://www.afisha.ru/msk/schedule_concert"
        self.concert_count = None
        self.all_concert_data = []

    def setup(self) -> None:
        """Обновить счетчики и данные."""
        self.make_zero()
        self.refresh_data()

    def make_zero(self) -> None:
        """Обнулить счетчики."""
        self.cinema_count = 0
        self.theatre_count = 0
        self.concert_count = 0

    def refresh_data(self) -> None:
        """Обновить данные."""
        self.all_cinema_data = self.parse(self.url_cinema)
        self.all_theatre_data = self.parse(self.url_theatre)
        self.all_concert_data = self.parse(self.url_concert)

    def get_data_smart(self, action: str) -> list:
        """
        Получить афишу.

        :param action: тип афиши (кино, театр, концерт)
        """
        if action == self.options[0]:
            self.cinema_count += 1
            return self.make_correct_text(self.get_data(self.all_cinema_data, self.cinema_count))
        elif action == self.options[1]:
            self.theatre_count += 1
            return self.make_correct_text(self.get_data(self.all_theatre_data, self.theatre_count))
        else:
            self.concert_count += 1
            return self.make_correct_text(self.get_data(self.all_concert_data, self.concert_count))

    def make_correct_text(self, data: list) -> list:
        """
        Получить корректно оформленный список афиш.

        :param data: некорректный список афиш
        """
        text = []
        for title, link, descr in data:
            cur_text = fmt.hbold(title) + "\n" + fmt.hitalic(descr) + fmt.hide_link(link)
            text.append(cur_text)
        return text

    def get_data(self, data: list, count: int) -> list:
        """
        Получить некорректный срез списка афиш.

        :param data: некорректный список афиш
        :param count: счетчик
        """
        if len(data) > (count - 1) * self.multiplier:
            return data[(count - 1) * self.multiplier: count * self.multiplier]

    def parse(self, url: str) -> list:
        """
        Получить некорректный список афиш.

        :param url: ссылка на сайт с афишами.
        """
        all_links = []
        for num in range(1, self.max_info_count + 1):
            cur_url = url + f"/page{num}"
            soup = self.get_soup(cur_url)
            table = soup.find("div", class_="_1Avyn")
            if table:
                all_cards = table.find_all("li", class_="_1gSmu")
                for item in all_cards:
                    try:
                        tmp = item.find("a", class_="_1F19s")
                        title = tmp.text.strip()
                        link = self.url + tmp.get("href")
                        descr = tmp.find_next().text.strip()
                        all_links.append([title, link, descr])
                    except AttributeError:
                        continue
            else:
                break

        return all_links


if __name__ == "__main__":
    pass
