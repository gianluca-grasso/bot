import requests
import bs4




class euro:

    session = None
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}

    def __init__(self):
        self.session = requests.Session()

    def find_serie(self, name):
        name = name.replace(" ","+")
        res = self.session.get("https://eurostreaming.pink/?s="+name, headers = self.headers)

        ret = []

        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            results = soup.find("ul", class_="recent-posts")
            lis = results.find_all("li")
            for li in lis:
                name = li.find("a").get("title")
                link = li.find("a").get("href")
                img = li.find("img").get("src")

                ret.append({"name":name, "link":link, "img":img})

        return ret

    def find_episodes(self, link):
        res = self.session.get(link, headers = self.headers)

        ret = []

        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.text, "html.parser")

            results = soup.find("div", class_="su-accordion")

            for result in results.find_all("a"):
                pass
                #ret.append({"s":"", "e":"", })


