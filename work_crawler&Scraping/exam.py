import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://finance.naver.com/sise/sise_market_sum.naver?&sosok=0&page="

all_data = []

for page in range(1 , 2):  
    url = base_url.format(page)
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.select_one("table.type_2")
    rows = table.select("tbody tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 12:
            continue
        
        
        name = cols[1].text.strip()
        current_price = cols[2].text.strip().replace(',', '')
        market_cap = cols[6].text.strip().replace(',', '')
        per = cols[10].text.strip()
        roe = cols[11].text.strip()

        all_data.append({
            "종목명": name,
            "현재가": current_price,
            "시가총액": market_cap,
            "PER": per,
            "ROE": roe
        })


df = pd.DataFrame(all_data)
df.to_csv("kospi_top50.csv", index=False, encoding='utf-8-sig')

print("✅ CSV 저장 완료")