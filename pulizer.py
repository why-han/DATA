import requests
from bs4 import BeautifulSoup

# 目标 URL
url = "https://en.wikipedia.org/wiki/Pulitzer_Prize_for_Fiction"

# 发送请求，避免被屏蔽
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# 解析 HTML
soup = BeautifulSoup(response.text, "lxml")

# 找到获奖者信息的表格
table = soup.find("table", {"class": "wikitable sortable"})

# 获取表格主体部分（<tbody>）
tbody = table.find("tbody")

# 遍历表格的每一行（<tr>）
for row in tbody.find_all("tr")[1:]:  
    cells = row.find_all(["td", "th"])  # 获取每一列
    if len(cells) < 3:  # 过滤掉无效行
        continue
    year = cells[0].get_text(strip=True)  # 第 1 列：年份
    winner = cells[2].find("a").get_text(strip=True) if cells[2].find("a") else cells[2].get_text(strip=True)  # 获奖者
    work = cells[3].get_text(strip=True)  # 作品
    print(f"年份: {year}, 获奖者: {winner}, 作品: {work}")

