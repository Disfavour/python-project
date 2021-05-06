from bs4 import BeautifulSoup
import requests


class PARSER:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }

    def get_soup(self, url) -> BeautifulSoup:
        req = requests.get(url, headers=self.headers)
        return BeautifulSoup(req.text, "lxml")


headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
url_horoscope = "https://1001goroskop.ru"

url_news = "https://lenta.ru/parts/news"
url_news_part = "https://lenta.ru"

url_weather = "https://www.gismeteo.ru"


def get_soup(url) -> BeautifulSoup:
    req = requests.get(url, headers=headers)
    return BeautifulSoup(req.text, "lxml")


def get_horoscope_signs() -> dict:
    soup = get_soup(url_horoscope)
    signs = soup.find("ul", class_="zodi_tbl").find_all("a")
    d = {}
    for item in signs:
        text = item.find("strong").text.strip()
        link = item.get("href")
        d[text] = link
    return d


def parse_horoscope_sign(url):
    url = url_horoscope + url
    soup = get_soup(url)
    text = soup.find("table", id="eje_text").find("p").text.strip()
    return text


def parse_news():
    soup = get_soup(url_news)
    many_news = soup.find("div", class_="b-longgrid-column").find_all("div", class_="item news")
    d = {}
    for item in many_news:
        text = item.find("div", class_="titles").find("a").text.strip()
        link = item.find("div", class_="titles").find("a").get("href")
        d[text] = link
    return d


def parse_weather():
    soup = get_soup(url_weather)
    d = {}

    table = soup.find("div", class_="wn_body")
    cur_temp = table.find("div", class_="temperature").find("span", class_="unit_temperature_c").text.strip()
    cur_descr = table.find("div", class_="_description").find("div", class_="gray").text.strip()
    info = [cur_temp, cur_descr]

    small_table_1 = table.find("div", class_="_attention").find_all("div", class_="clearfix")

    base_feel = small_table_1[0]
    feel = base_feel.find("div", class_="info_label").text.strip()
    feel_temp = base_feel.find("div", class_="info_value").find("span", class_="unit_temperature_c").text.strip()
    d[feel] = feel_temp

    base_wind = small_table_1[1]
    wind = base_wind.find("div", class_="info_label").text.strip()
    wind_speed = base_wind.find("div", class_="info_value").find("span", class_="unit_wind_m_s").text.strip()
    d[wind] = wind_speed

    small_table_2 = table.find("div", class_="opened").find_all("div", class_="clearfix")

    base_pressure = small_table_2[0]
    pressure = base_pressure.find("div", class_="info_label").text.strip()
    pressure_count = base_pressure.find("div", class_="info_value").find("span", class_="unit_pressure_mm_hg_atm").text.strip()
    d[pressure] = pressure_count

    base_humidity = small_table_2[1]
    humidity = base_humidity.find("div", class_="info_label").text.strip()
    humidity_count = base_humidity.find("div", class_="info_value").text.strip()
    d[humidity] = humidity_count

    base_geomagn_act = small_table_2[2]
    geomagn_act = base_geomagn_act.find("div", class_="info_label").find("a").text.strip()
    geomagn_act_count = base_geomagn_act.find("div", class_="info_value").text.strip()
    d[geomagn_act] = geomagn_act_count

    base_water_temp = small_table_2[3]
    water_temp = base_water_temp.find("div", class_="info_label").text.strip()
    water_temp_count = base_water_temp.find("div", class_="info_value").find("span", class_="unit_temperature_c").text.strip()
    d[water_temp] = water_temp_count

    return info, d


class AFISHA(PARSER):
    def __init__(self):
        #self.url_cinema = "https://www.afisha.ru/msk/schedule_cinema"
        self.url = "https://www.afisha.ru"
        self.multiplyer = 1

        self.cinema_count = 0
        self.all_cinema_links = self.parse_cinema()

        self.theatre_count = 0
        self.all_theatre_links = self.parse_theatre()

        self.concert_count = 0
        self.all_concert_links = self.parse_concert()


    def parse_cinema(self):
        all_links = []
        for num in range(1, 20):
            cur_url = f"https://www.afisha.ru/msk/schedule_cinema/page{num}"
            soup = self.get_soup(cur_url)
            table = soup.find("div", class_="_1Avyn")
            if table:
                all_cards = table.find_all("li", class_="_1gSmu")
                for item in all_cards:
                    all_links.append(self.url + item.find("a", class_="_1F19s").get("href"))
            else:
                break
        return all_links

    def parse_theatre(self):
        all_links = []
        for num in range(1, 20):
            cur_url = f"https://www.afisha.ru/msk/schedule_theatre/page{num}"
            soup = self.get_soup(cur_url)
            table = soup.find("div", class_="_1Avyn")
            if table:
                all_cards = table.find_all("li", class_="_1gSmu")
                for item in all_cards:
                    try:
                        # тут трай, потому что там блок с рекламой
                        all_links.append(self.url + item.find("a", class_="_1F19s").get("href"))
                    except:
                        continue
            else:
                break

        return all_links

    def parse_concert(self):
        all_links = []
        for num in range(1, 20):
            cur_url = f"https://www.afisha.ru/msk/schedule_concert/page{num}"
            soup = self.get_soup(cur_url)
            table = soup.find("div", class_="_1Avyn")
            if table:
                all_cards = table.find_all("li", class_="_1gSmu")
                for item in all_cards:
                    try:
                        # тут трай, потому что там блок с рекламой
                        all_links.append(self.url + item.find("a", class_="_1F19s").get("href"))
                    except:
                        continue
            else:
                break

        return all_links

    def get_links_cinema(self):
        if len(self.all_cinema_links) < 1:
            self.parse_cinema()
        self.cinema_count += 1
        if len(self.all_cinema_links) > (self.cinema_count - 1) * self.multiplyer:
            return self.all_cinema_links[(self.cinema_count - 1) * self.multiplyer: self.cinema_count * self.multiplyer]

    def get_links_theatre(self):
        if len(self.all_theatre_links) < 1:
            self.parse_cinema()
        self.theatre_count += 1
        if len(self.all_theatre_links) > (self.theatre_count - 1) * self.multiplyer:
            return self.all_theatre_links[(self.theatre_count - 1) * self.multiplyer: self.theatre_count * self.multiplyer]

    def get_links_concert(self):
        if len(self.all_concert_links) < 1:
            self.parse_cinema()
        self.concert_count += 1
        if len(self.all_concert_links) > (self.concert_count - 1) * self.multiplyer:
            return self.all_concert_links[(self.concert_count - 1) * self.multiplyer: self.concert_count * self.multiplyer]


if __name__ == "__main__":
    pass
