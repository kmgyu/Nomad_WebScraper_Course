from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

# 환경 변수
user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"

class PageExtractor:
    
    def __init__(self, keyword, base="https://www.wanted.co.kr", search_query="/search?query="):
        self.base = base
        self.search_query = search_query
        self.keyword = keyword
        
        self.p = sync_playwright().start()
        self.jobs_db = []

        # headless True
        self.browser = self.p.chromium.launch()

        self.page = self.browser.new_page(user_agent=user_agent)

        self.page.goto(base + search_query + keyword)

    def action_wanted(self):
        # 원티드 페이지에서 적용됨
        self.page.click("a#search_tab_position")
        time.sleep(0.1)

        for _ in range(5):
            self.page.keyboard.down("End")
            # scrolling down
            time.sleep(0.1)
        
    
    def extract(self):
        # 원티드아니면 다른거 써야됨.
        # 사이트가 다르면 class가 다를 것이므로... 원티드 아니면 작동 안 할것..
        self.action_wanted()
        self.content = self.page.content()
        self.p.stop()

        soup = BeautifulSoup(self.content, "html.parser")
        
        jobs = soup.find_all("div", class_="JobCard_container__FqChn")

        for job in jobs:
            link = f"{self.base}{job.find('a')['href']}"
            title = job.find("strong", class_ = "JobCard_title__ddkwM").text
            company_name = job.find("span", class_ = "JobCard_companyName__vZMqJ").text
            reward = job.find("span", class_="JobCard_reward__sdyHn").text
            job_info = {
                "title":title,
                "company_name":company_name,
                "reward":reward,
                "link":link,
            }
            self.jobs_db.append(job_info)
        
        return self.jobs_db
        # self.file = open(f"db/{self.keyword}.csv", mode="w", encoding="utf-8", newline="")
        # self.writer = csv.writer(self.file)
        # self.writer.writerow(
        #     ["Title",
        #     "Company",
        #     "Reward", 
        #     "link"])

        # for job in self.jobs_db:
        #     self.writer.writerow(job.values())
        # self.file.close()


# 자원관리 예제를 위해 with문도 시도해볼것.