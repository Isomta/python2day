import requests
from bs4 import BeautifulSoup
import lxml
import json

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
}
url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}"


def get_soup(url, flag=0) -> BeautifulSoup:
    response = requests.get(url=url, headers=headers).text
    if flag == 1:
        with open(f"data/index{url.split('=')[-1]}.html", "w") as file:
            file.write(response)
    return BeautifulSoup(response, 'lxml')


def get_pagination(soup) -> int:
    return int(soup.find("div", class_="pagination-numbers__right").find_all("a")[-1].text)


def get_data(cart):
    new_price = int(
        cart.find("span", class_="price-val").find("span").text.replace(" ", ""))

    old_price = int(e.text.replace(" ", "")) if (e := cart.find(
        "span", class_="price-old")) is not None else new_price
    if old_price - new_price > 1:
        prefix = "https://www.labirint.ru"
        print(cart.find("span", class_="product-title").text)
        return {
            "name": cart.find("span", class_="product-title").text,
            "link": f"{prefix}{cart.find('a', class_='product-title-link').get('href')}",
            "product-author": e.text.replace("\n", "").strip() if (e := cart.find("div", class_="product-author")) is not None else "Нет автора",
            "author-link": f"{prefix}{e}).find('a').get('href')" if e is not None else "Нет ссылки",
            "new-price": new_price,
            "old-price": old_price,
            "product-pubhouse": cart.find("div", class_="product-pubhouse").text.replace("\n", "").strip(),
            "product-pubhouse-link": f"{prefix}{cart.find('a', class_='product-pubhouse__pubhouse').get('href')}",
            "discount": int((old_price - new_price) / old_price * 100),
        }


def get_carts(soup):
    carts = soup.find_all("div", class_="genres-carousel__container products-row")[1].find_all("div",
                                                                                               class_="genres-carousel__item")
    return carts


def get_pages(num) -> str:
    pages = []
    for page in range(1, num + 1):
        pages.append(get_soup(url=url.format(page=page), flag=1))
    return pages


def main():
    soup = get_soup(url=url.format(page=1))
    num = get_pagination(soup)
    pages = get_pages(num)
    data = []
    for page in pages:
        for cart in get_carts(page):
            data.append(get_data(cart))
    with open("data/data.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
