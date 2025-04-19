"""Generate a list of intractable disease groups and their corresponding disease numbers."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


CHROME_OPTION = Options()
CHROME_OPTION.add_argument("--headless")

GROUP_URLS = {
    "神経・筋疾患": "https://www.nanbyou.or.jp/entry/5347/#01",
    "代謝疾患": "https://www.nanbyou.or.jp/entry/5479/#02",
    "染色体・遺伝子異常": "https://www.nanbyou.or.jp/entry/5491/#03",
    "免疫疾患": "https://www.nanbyou.or.jp/entry/5481/#04",
    "循環器疾患": "https://www.nanbyou.or.jp/entry/5482/#05",
    "消化器疾患": "https://www.nanbyou.or.jp/entry/5490/#06",
    "内分泌疾患": "https://www.nanbyou.or.jp/entry/5486/#07",
    "血液疾患": "https://www.nanbyou.or.jp/entry/5483/#08",
    "腎・泌尿器疾患": "https://www.nanbyou.or.jp/entry/5484/#09",
    "呼吸器疾患": "https://www.nanbyou.or.jp/entry/5487/#10",
    "皮膚・結合組織疾患": "https://www.nanbyou.or.jp/entry/5480/#11",
    "骨・関節疾患": "https://www.nanbyou.or.jp/entry/5485/#12",
    "聴覚・平衡機能疾患": "https://www.nanbyou.or.jp/entry/5489/#13",
    "視覚疾患": "https://www.nanbyou.or.jp/entry/5488/#14",
}


def intractable_disease_groups() -> dict[str, list[int]]:
    """Obtain the disease number for each disease group from https://www.nanbyou.or.jp/.

    Returns:
        dict[str, list[int]]: Dictionary of disease group names and disease numbers.
    """
    with webdriver.Chrome(options=CHROME_OPTION) as driver:
        disease_nos: dict[str, list[int]] = {}
        for group_name, group_url in GROUP_URLS.items():
            disease_nos[group_name] = []
            driver.get(group_url)
            driver.implicitly_wait(3)
            for ele in driver.find_elements(By.XPATH, "//tr[@class='txt-cntr']/td[@rowspan]"):
                disease_nos[group_name].append(int(ele.text))

    return disease_nos


if __name__ == "__main__":
    disease_nos = intractable_disease_groups()

    import pandas as pd
    import json
    import yaml

    pd.Series(disease_nos, name="no").to_frame().rename_axis("group").reset_index().explode("no").set_index(
        "no"
    ).sort_index().to_csv("intractable_disease_groups.csv", encoding="utf-8-sig")

    with open("intractable_disease_groups.json", "w", encoding="utf-8") as f:
        json.dump(disease_nos, f, ensure_ascii=False)

    with open("intractable_disease_groups.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(disease_nos, f, allow_unicode=True)
