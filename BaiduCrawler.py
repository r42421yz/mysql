from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from MysqlHelper import MySqlHelper;
import time

options = Options()

options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# 让chrome在“无界面”模式运行，适合服务器环境或爬虫
options.add_argument('--headless')
# 配合无头模式禁用GPU加速，避免某些系统问题
options.add_argument('--disable-gpu')

service = Service(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://top.baidu.com/board?tab=realtime')

time.sleep(3)

# 抓取前10条热搜标题
titles = driver.find_elements(By.CLASS_NAME, 'c-single-text-ellipsis')[:10]
# 抓取前10条热搜热搜指数
hot_indexes = driver.find_elements(By.CLASS_NAME, 'hot-index_1Bl1a')[:10]

# 连接数据库
db_helper = MySqlHelper(host='localhost', user='root', password='password', database='baidu')

print("百度热搜前10:")
for i, t in enumerate(titles, 1):
    title_text = t.text
    index_value = hot_indexes[i-1].text if i-1<len(hot_indexes) else "N/A"

    data = {
        'title' : title_text,
        'hot_index' : index_value,
        'ranking' : i
    }
    db_helper.insert('hot_searches', data)
    print(f"{i}. {title_text} - 热度: {index_value}")

query = 'SELECT * FROM hot_searches'
params  = ()
print(db_helper.query_all(query, params))

db_helper.close()

driver.quit()
