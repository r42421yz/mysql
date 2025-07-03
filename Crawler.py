import requests;
from bs4 import BeautifulSoup;
from MysqlHelper import MySqlHelper;

# 发送请求
url = "https://top.baidu.com/board?tab=realtime"
headers = {
    'User-Agent' :  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 获取相应
response = requests.get(url, headers=headers)
if response.status_code == 200:
    print("Request succeed")

# 解析数据
soup = BeautifulSoup(response.content, "html.parser")
titles = soup.find_all("div", class_="c-single-text-ellipsis")[:10]
hot_indexes = soup.find_all("div", class_="hot-index_1Bl1a")[:10]
ranking = soup.find_all("div", class_ = "index_1Ew5p")[:10]

# 连接数据库
db_helper = MySqlHelper(host='localhost', user='root', password='password', database='baidu')
print("百度热搜前10:")
for i in range(0, 10):
    rank = 0
    if(ranking[i].text.strip()):
        rank = int(ranking[i].text.strip())

    title = titles[i].text
    hot_index = hot_indexes[i].text

    data = {
        'title' : title,
        'hot_index' : hot_index,
        'ranking' : rank
    }
    db_helper.insert('hot_searches', data)
    print(f"{rank}. {title} - 热度: {hot_index}")

query = 'SELECT * FROM hot_searches'
params  = ()
print(db_helper.query_all(query, params))

db_helper.close()
