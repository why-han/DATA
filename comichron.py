import requests
from bs4 import BeautifulSoup
import re
import pandas as pd  # 用于存储表格数据

# 目标 URL
url = "https://comichron.com/yearlycomicssales.html"

# 设置请求头，模拟真实浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
}

# 发送请求
response = requests.get(url, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
    # 解析 HTML 内容
    soup = BeautifulSoup(response.text, "lxml")

    # 直接查找目标 <div> 标签
    target_divs = soup.find_all("div", style="text-align:center;")

    # 遍历所有符合条件的 <div> 标签
    links = []
    years = []  # 存储年份信息
    for target_div in target_divs:
        # 查找所有 <a> 标签
        for a_tag in target_div.find_all("a"):
            href = a_tag.get("href")
            if href and not href.startswith("http"):
                href = "https://comichron.com" + href
                # 使用正则表达式提取年份
                year_match = re.search(r'/(\d{4})\.html$', href)
                if year_match:
                    year = int(year_match.group(1))
                    # 检查年份范围
                    if 1984 <= year <= 2022:
                        links.append(href)
                        years.append(year)  # 记录对应的年份
                        
    # 输出符合条件的链接
    print("\n符合条件的链接：")
    for link in links:
        print(link)
    print("\n总共找到链接数:", len(links))

    # --- 新增部分：提取每个链接中的表格数据 ---
    all_tables = []  # 用于存储所有表格数据

    for i, link in enumerate(links):  # 使用索引 i 关联年份
        print(f"\n正在处理链接：{link}")
        try:
            # 打开链接
            page_response = requests.get(link, headers=headers)
            # 检查请求是否成功
            if page_response.status_code == 200:
                # 解析 HTML 内容
                page_soup = BeautifulSoup(page_response.text, "lxml")
                # 找到 <tbody> 标签
                tbody = page_soup.find("tbody")
                if tbody:
                    # 遍历每一行 <tr>
                    table_data = []
                    rows = tbody.find_all("tr")
                    for row in rows:
                        # 提取每一列 <td>
                        cols = row.find_all("td")
                        cols = [col.get_text(strip=True) for col in cols]
                        # 忽略空行
                        if len(cols) > 0:
                            table_data.append(cols)

                    # 将当前页面的表格数据存储为 DataFrame
                    df = pd.DataFrame(table_data)

                    # **新增：给表格增加 "年份" 列**
                    df.insert(0, "年份", years[i])  # 在第 0 列插入年份
                    
                    # 存储表格
                    all_tables.append(df)  
                    print(f"已成功提取表格数据，共 {len(table_data)} 行。")
                else:
                    print("未找到 <tbody> 标签，跳过此页面。")
            else:
                print(f"请求失败，状态码：{page_response.status_code}")
        except Exception as e:
            print(f"请求或解析失败，错误信息：{e}")

    # 将所有表格数据合并并保存为 Excel 文件
    if all_tables:
        combined_df = pd.concat(all_tables, ignore_index=True)
        combined_df.to_excel('E:\coding\PYTHONE_OUTPUT\COMICHRONE\comichron_tables_with_year.xlsx', index=False)
        print("\n所有表格数据已保存为 comichron_tables_with_year.xlsx 文件。")
    else:
        print("\n未找到任何表格数据。")

else:
    print("请求失败，状态码：", response.status_code)
