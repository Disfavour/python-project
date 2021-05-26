from bs4 import BeautifulSoup
import requests
import re

url = "https://www.povarenok.ru/recipes/"
headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
}

#req = requests.get(url, headers=headers)
#with open("index.html", "w") as file:
#    file.write(req.text)


def parse():
    data = []

    with open("index.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    names = soup.find_all("h2")
    for i in names:
        rec = dict()
        tmp = i.find("a")
        if tmp == None:
            break
        rec["Название блюда"] = tmp.text
        rec["Ссылка на рецепт"] = tmp.get("href")
        data.append(rec)


    ingr = soup.find_all("div", class_=re.compile("ingr_fast"))
   # print(ingr)
    for k, i in enumerate(ingr):
        lst = []
        tmp = i.find_all("span")
        for j in tmp:
            lst.append(j.text)
            #print(j.text)
        data[k]["Ингредиенты"] = lst

    #for i in data:
    #    print(i)
    return data
