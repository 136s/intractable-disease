#!/usr/bin/env python

import numpy as np
import pandas as pd


def intractable_disease_table(
    xlsx_url: str = "https://www.mhlw.go.jp/content/000855403.xlsx",
    num_period_cols: int = 2,
    period_colname: list[str] = ["_", "no", "name"],
) -> pd.Series:
    """Get intractable disease table from xlsx_url.

    Args:
        xlsx_url (str, optional): a url of xlsx file.
            Defaults to "https://www.mhlw.go.jp/content/000855403.xlsx".
        num_period_cols (int, optional): number of periods of columns. Defaults to 2.
        period_colname (list[str], optional): column names of a period.
            Defaults to ["_", "no", "name"].

    Returns:
        pd.Series: a series of intractable disease table.

    Note:
        xlsx_url is from https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000084783.html
    """
    # load xlsx
    colnames = [f"{col}_{i}" for i in range(num_period_cols) for col in period_colname]
    multicol_df = (
        pd.read_excel(xlsx_url, names=colnames).filter(regex="^(?!_)").dropna()
    )
    # split to no and name
    no, name = (
        np.asarray(
            [multicol_df.filter(regex=f"_{i}$").values for i in range(num_period_cols)]
        )
        .reshape(-1, num_period_cols)
        .T
    )
    # make series
    series = pd.Series(name, index=no, name="name").drop("番号")
    series.index.rename("no", inplace=True)
    return series.sort_index()


if __name__ == "__main__":
    intractable_disease = intractable_disease_table()
    intractable_disease.to_csv("intractable_disease.csv", encoding="utf-8-sig")

    import json
    import yaml

    with open("intractable_disease.json", "w", encoding="utf-8") as f:
        json.dump(intractable_disease.to_dict(), f, ensure_ascii=False)

    with open("intractable_disease.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(intractable_disease.to_dict(), f, allow_unicode=True)
