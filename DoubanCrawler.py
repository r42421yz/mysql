import requests;
from bs4 import BeautifulSoup;
from MysqlHelper import MySqlHelper;

class DoubanMovieCrawler:
    def __init__(self, db_helper, base_url="https://movie.douban.com/top250", headers=None):
        self.db_helper = db_helper
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0'
        }

    def crawler(self):
        for start in range(0, 100, 25):
            url = f"{self.base_url}?start={start}"
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Request failed at start={start}")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            self.parse_and_store(soup)

    def parse_and_store(self, soup):
        for item in soup.find_all("div", class_="info"):
            data = self.extract_movie_data(item)
            self.print_movie(data)
            self.db_helper.insert('movies', data)

    def extract_movie_data(self, item):
        hd = item.find("div", class_="hd")
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
        year = parts[0] if len(parts) > 0 else ""
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
        return data
    
    def print_movie(self, data):
        print(f"标题：{data['title']}")
        print(f"导演：{data['director']}")
        print(f"主演：{data['actors']}")
        print(f"年份：{data['year']}")
        print(f"国家：{data['country']}")
        print(f"类型：{data['genres']}")
        print(f"评分：{data['rating']}")
        print(f"评价人数：{data['votes']}")
        print("-------------------------")

if __name__ == "__main__":
    db_helper = MySqlHelper(host='localhost', user='root', password='password', database='douban')
    crawler = DoubanMovieCrawler(db_helper = db_helper)
    crawler.crawler()
    db_helper.close()
