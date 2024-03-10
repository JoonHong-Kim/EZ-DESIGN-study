from collections.abc import Iterable, Iterator
import requests
from bs4 import BeautifulSoup
import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Clothes:
    def __init__(self, name: str, brand: str, price: str) -> None:
        self.name = name
        self.brand = brand
        self.price = price


class WebIterator(Iterator):
    def __init__(
        self, collections: "HTMLCollection", selectors: dict[str, str]
    ) -> None:
        self._collections = collections
        self._index = 0
        self._selectors = selectors

    def __next__(self) -> list[Clothes]:
        try:
            item = self._parser(self._collections[self._index])
            if not item:
                raise StopIteration
            self._index += 1
        except IndexError:
            raise StopIteration
        return item

    def _parser(self, item):
        names = item.select(self._selectors["name"])
        brands = item.select(self._selectors["brand"])
        prices = item.select(self._selectors["price"])
        return [
            Clothes(
                name=name.text.strip(),
                brand=brand.text.strip(),
                price=price.text.strip().split("\n")[-1].strip(),
            )
            for name, brand, price in zip(names, brands, prices)
        ]


class HTMLCollection(Iterable):
    def __init__(
        self,
        collection: list[str],
        selectors: dict[str, str],
    ) -> None:
        self._collection = collection
        self._selectors = selectors

    def __getitem__(self, index: int):
        return self._collection[index]

    def __iter__(self) -> WebIterator:
        return WebIterator(self._collection, self._selectors)

    def add_item(self, item: str):
        self._collection.append(item)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-M", "--mall", type=str, required=True, default="musinsa")
    parser.add_argument("-C", "--category", type=str, required=True, default="003004")
    parser.add_argument("-P", "--page", type=int, default=1)
    args = parser.parse_args()

    if args.mall == "musinsa":
        musinsa_selector = {
            "name": "div.li_inner > div.article_info > p.list_info > a",
            "brand": "div.li_inner > div.article_info > p.item_title > a",
            "price": "div.li_inner > div.article_info > p.price",
        }
        MusinsaCollection = HTMLCollection([], musinsa_selector)

        for page in range(1, args.page + 1):
            url = f"https://www.musinsa.com/categories/item/{args.category}?d_cat_cd={args.category}&brand=&list_kind=small&sort=pop_category&sub_sort=&page={page}"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            MusinsaCollection.add_item(soup)
        clothes_list = []
        for clothes in MusinsaCollection:
            clothes_list.extend(clothes)
            if len(clothes_list) > 1000:
                clothes_list = clothes_list[:1000]
                break

    elif args.mall == "wconcept":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        wconcept_selector = {
            "name": ".text.detail",
            "brand": ".text.title",
            "price": ".final-price",
        }
        WconceptSelector = HTMLCollection([], wconcept_selector)

        for page in range(1, args.page + 1):
            url = f"https://display.wconcept.co.kr/category/women/{args.category}?page={page}"
            driver.get(url)
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "like")))
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            WconceptSelector.add_item(soup)
        clothes_list = []
        for clothes in WconceptSelector:
            clothes_list.extend(clothes)
            if len(clothes_list) > 100:
                clothes_list = clothes_list[:100]
                break
    else:
        raise ValueError("Invalid mall")

    df = pd.DataFrame(
        [[clothes.name, clothes.brand, clothes.price] for clothes in clothes_list],
        columns=["name", "brand", "price"],
    )
    df.to_csv(f"{args.mall}_{args.category}.csv", index=False)
