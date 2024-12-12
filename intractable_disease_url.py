#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


CHROME_OPTION = Options()
CHROME_OPTION.add_argument("--headless")

INDEX_URL = "https://www.nanbyou.or.jp/entry/5346"


def intractable_disease_urls() -> dict[int, str]:
    """Get the URL for each disease from the intractable disease list.

    Returns:
        dict[int, str]: a dictionary of the URL for each disease.
    """
    with webdriver.Chrome(options=CHROME_OPTION) as driver:
        driver.get(INDEX_URL)

        # get the url of the list for each of the 50 diseases
        disease_50_urls = [
            ele.get_attribute("href")
            for ele in driver.find_elements(By.XPATH, "//table[@class='serchList'][1]/tbody/tr/td/a")
        ]

        # get the URL for each disease
        disease_urls: dict[int, str] = {}
        for block_url in disease_50_urls:
            driver.get(block_url)
            driver.implicitly_wait(10)
            for no_ele, url_ele in zip(
                driver.find_elements(By.XPATH, "//tr[@class='txt-cntr']/td[1]"),
                driver.find_elements(By.XPATH, "//td[@class='btn-pnk']/div/a"),
            ):
                disease_urls[int(no_ele.text)] = url_ele.get_attribute("href")

    return disease_urls


if __name__ == "__main__":
    disease_urls = intractable_disease_urls()

    import json
    import yaml
    import pandas as pd

    pd.Series(disease_urls, name="name").to_csv("intractable_disease_url.csv", encoding="utf-8-sig")

    with open("intractable_disease_url.json", "w", encoding="utf-8") as f:
        json.dump(disease_urls, f, ensure_ascii=False)

    with open("intractable_disease_url.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(disease_urls, f, allow_unicode=True)
