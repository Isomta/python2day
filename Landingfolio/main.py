import requests
from bs4 import BeautifulSoup
import json


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Sec-Fetch-Site': 'same-site',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru',
    'Sec-Fetch-Mode': 'cors',
    'Host': 's3.landingfolio.com',
    'Origin': 'https://www.landingfolio.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Connection': 'keep-alive',
    'Referer': 'https://www.landingfolio.com/',
    'Sec-Fetch-Dest': 'empty',
}

params = {
    'category': 'landing-page',
    'page': '1',
    'sortBy': 'free-first',
}


def main():
    page = 0
    total_list = []
    while True:
        page += 1
        print(f"[+] page number {page}")
        params.update({"page": page})
        response = requests.get(
            'https://s3.landingfolio.com/inspiration', params=params, headers=headers)
        res = response.json()
        if res == []:
            break
        for item in res:
            print(f"      [+] {item.get('title')}")
            images = []
            prefix = "https://landingfoliocom.imgix.net/"
            for i in item.get("screenshots"):
                images.append(f"{prefix}{i.get('images').get('desktop')}")
            total_list.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "images": images
            })
    with open("Landingfolio/data/index.json", "w") as file:
        json.dump(total_list, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
