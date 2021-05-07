from bs4 import BeautifulSoup
import requests
import aiogram.utils.markdown as fmt


class PARSER:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    multiplier = 2

    def get_soup(self, url) -> BeautifulSoup:
        req = requests.get(url, headers=self.headers)
        return BeautifulSoup(req.text, "lxml")


class HOROSCOPE(PARSER):
    def __init__(self):
        self.url = "https://1001goroskop.ru"
        self.data = self.setup()

    def setup(self) -> dict:
        soup = self.get_soup(self.url)
        signs = soup.find("ul", class_="zodi_tbl").find_all("a")

        d = {}
        for item in signs:
            text = item.find("strong").text.strip()
            link = self.url + item.get("href")
            d[text] = link
        return d

    def get_signs(self) -> list:
        return list(self.data.keys())

    def get_data_smart(self, sign: str) -> str:
        url = self.data[sign]
        text = self.parse(url)
        text = fmt.hitalic(text)
        text += fmt.hide_link(url)
        return text

    def parse(self, url: str) -> str:
        soup = self.get_soup(url)
        text = soup.find("table", id="eje_text").find("p").text.strip()
        return text


class NEWS(PARSER):
    def __init__(self):
        self.url = "https://lenta.ru/parts/news"
        self.url_part = "https://lenta.ru"
        self.count = None

    def make_zero(self) -> None:
        self.count = 0

    def get_data_smart(self) -> list:
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
        soup = self.get_soup(self.url)
        many_news = soup.find("div", class_="b-longgrid-column").find_all("div", class_="item news")
        ans = []
        for item in many_news:
            text = item.find("div", class_="titles").find("a").text.strip()
            link = self.url_part + item.find("div", class_="titles").find("a").get("href")
            ans.append([text, link])
        return ans


class WEATHER(PARSER):
    def __init__(self):
        self.url = "https://www.gismeteo.ru"
        self.main_data = {
            "Темпуратура": None,
            "Описание": None,
        }
        self.extra_data = {}

    def get_data_smart(self) -> str:
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
        base_info, extra_info = self.parse()
        self.main_data["Темпуратура"] = base_info[0]
        self.main_data["Описание"] = base_info[1]
        for i in range(6):
            self.extra_data[extra_info[i][0]] = extra_info[i][1]

    def parse(self) -> tuple:
        soup = self.get_soup(self.url)
        table = soup.find("div", class_="wn_body")

        base_info = self.get_base_info(table)
        table_1_info = self.get_info_1(table)
        table_2_info = self.get_info_2(table)

        return base_info, table_1_info + table_2_info

    def get_base_info(self, soup: BeautifulSoup) -> tuple:
        cur_temp = soup.find("div", class_="temperature").find("span", class_="unit_temperature_c").text.strip()
        cur_descr = soup.find("div", class_="_description").find("div", class_="gray").text.strip()
        return cur_temp, cur_descr

    def get_info_1(self, soup: BeautifulSoup) -> list:
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
        ans = []
        small_table_2 = soup.find("div", class_="opened").find_all("div", class_="clearfix")

        base_pressure = small_table_2[0]
        pressure = base_pressure.find("div", class_="info_label").text.strip()
        pressure_count = base_pressure.find("div", class_="info_value").find(
            "span",class_="unit_pressure_mm_hg_atm").text.strip()
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
            "span",class_="unit_temperature_c").text.strip()
        ans.append([water_temp, water_temp_count])

        return ans


class AFISHA(PARSER):
    def __init__(self):
        self.options = [
            "Кино", "Театр", "Концерт"
        ]
        self.url = "https://www.afisha.ru"
        self.max_info_count = 1

        self.url_cinema = "https://www.afisha.ru/msk/schedule_cinema"
        self.cinema_count = None
        self.all_cinema_links = []

        self.url_theatre = "https://www.afisha.ru/msk/schedule_theatre"
        self.theatre_count = None
        self.all_theatre_links = []

        self.url_concert = "https://www.afisha.ru/msk/schedule_concert"
        self.concert_count = None
        self.all_concert_links = []

    def setup(self) -> None:
        self.make_zero()
        self.refresh_links()

    def make_zero(self) -> None:
        self.cinema_count = 0
        self.theatre_count = 0
        self.concert_count = 0

    def refresh_links(self) -> None:
        self.all_cinema_links = self.parse(self.url_cinema)
        self.all_theatre_links = self.parse(self.url_theatre)
        self.all_concert_links = self.parse(self.url_concert)

    def get_data_smart(self, action: str) -> list:
        if action == self.options[0]:
            self.cinema_count += 1
            return self.make_correct_text(self.get_data(self.all_cinema_links, self.cinema_count))
        elif action == self.options[1]:
            self.theatre_count += 1
            return self.make_correct_text(self.get_data(self.all_theatre_links, self.theatre_count))
        else:
            self.concert_count += 1
            return self.make_correct_text(self.get_data(self.all_concert_links, self.concert_count))

    def make_correct_text(self, data: list) -> list:
        text = []
        for title, link, descr in data:
            cur_text = fmt.hbold(title) + "\n" + fmt.hitalic(descr) + fmt.hide_link(link)
            text.append(cur_text)
        return text

    def get_data(self, data: list, count: int) -> list:
        if len(data) > (count - 1) * self.multiplier:
            return data[(count - 1) * self.multiplier: count * self.multiplier]

    def parse(self, url: str) -> list:
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
