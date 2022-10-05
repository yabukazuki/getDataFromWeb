# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests as req

import pandas as pd
import re
from tqdm import tqdm
import traceback

from time import sleep
import warnings
warnings.simplefilter("ignore")

# カード一覧表示ページの URL
url = "https://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&set=[%22Adventures+in+the+Forgotten+Realms%22]&sort=cn+"

# [必須]サーバー負荷対策
sleep(1)
# ページ情報の取得
response=req.get(url, verify=False)
response.encoding=response.apparent_encoding
soup=BeautifulSoup(response.text, "html.parser")

info=soup.find_all("a")
count3 = 0
# 各カードデータの表示ページの URL に含まれる各カード固有の文字列を格納
uniques = []

# 各カードデータ表示ページの URL の取得
for data in info:
  unique = re.findall(r"multiverseid=\d+", data.get("href"))
  if len(unique) != 0 and count3%3 == 0:
    uniques.append(unique)
  count3 += 1


# 各表示ページのURLの共通部分
s="https://gatherer.wizards.com/Pages/Card/Details.aspx?"

# 各取得データを格納
CardName = []
Type = []
Text =[]

for unique in tqdm(uniques):
  try :
    # 取得元となる Web ページの URL 
    url = s + unique[0]

    # 　[必須]サーバー負荷対策
    sleep(1)
    # ページ情報の取得
    response = req.get(url, verify=False)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")

    datas = soup.find_all("div", class_="row")

    for data in datas:
      label = data.find("div", class_="label").get_text().strip()
      value = data.find("div",class_="value").get_text().strip()

      if label == "Card Name:":
        CardName.append(value)
        continue
      if label == "Types:":
        Type.append(value)
        continue
      if label == "Card Text:":
        Text.append(value)
        continue

  except :
    print(url)
    print(traceback.format_exc())


df = pd.DataFrame()
df["CardName"] = CardName
df["Type"] = Type
df["Text"] = Text

print(df.head())

df.to_csv("datasetCard.csv", index = False)


#  Created by yabukazuki on 2022/10/2<br>
#  Copyright © 2022 yabukazuki All rights reserved.