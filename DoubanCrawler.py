import requests;
from bs4 import BeautifulSoup;
from MysqlHelper import MySqlHelper;

headers = {
    'User-Agent' :  'Mozilla/5.0'
}


db_helper = MySqlHelper(host='localhost', user='root', password='password', database='douban')
for start in range(0, 100, 25):

    url = f"https://movie.douban.com/top250?start={start}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Request failed at start={start}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")

    for item in soup.find_all("div", class_="info"):

        hd = item.find("div", class_="hd")
        link = hd.find("a")["href"]
        spans = hd.find_all("span", class_="title")
        title_main = spans[0].text.strip() if spans else ""

        bd = item.find("div", class_="bd")
        p_tags = bd.find_all("p")

        info_lines = p_tags[0].get_text(strip=True, separator="\n").split("\n")
        line1 = info_lines[0]  # 导演/主演
        line2 = info_lines[1]  # 年份/国家/类型

        director = ""
        actors = ""
        if "导演" in line1:
            parts = line1.split("主演:")
            director = parts[0].replace("导演:", "").strip()
            if len(parts) > 1:
                actors = parts[1].strip()

        parts = [x.strip() for x in line2.split("/")]
        year = parts[0]
        country = parts[1] if len(parts) > 1 else ""
        genres = parts[2] if len(parts) > 2 else ""

        # 评分
        rating_tag = bd.find("span", class_="rating_num")
        rating = rating_tag.text.strip() if rating_tag else ""

        # 评价人数
        vote_tag = rating_tag.find_next_sibling("span").find_next_sibling("span")
        votes = ""
        if vote_tag:
            votes = "".join(filter(str.isdigit, vote_tag.text.strip()))

        print(f"标题：{title_main}")
        print(f"导演：{director}")
        print(f"主演：{actors}")
        print(f"年份：{year}")
        print(f"国家：{country}")
        print(f"类型：{genres}")
        print(f"评分：{rating}")
        print(f"评价人数：{votes}")
        print("-------------------------")

        data = {
            'title' : title_main,
            'year' : year,
            'rating' : rating,
            'votes' : votes,
            'genres' : genres,
            'country' : country,
            'director' : director,
            'actors' : actors
        }

        db_helper.insert('movies', data)


db_helper.close()
