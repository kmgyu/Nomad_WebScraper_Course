from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv

p = sync_playwright().start()
base = "https://www.wanted.co.kr"
jobs_db = []

browser = p.chromium.launch(headless=False)

page = browser.new_page()

# page.goto("https://google.com")
page.goto("https://www.wanted.co.kr/jobsfeed")

time.sleep(1)

page.click("button.Aside_searchButton__Xhqq3")
# same code down here
# page.locator("button.Aside_searchButton__Xhqq").click()

time.sleep(1)

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
# you can get by label, id... etc

page.keyboard.down("Enter")
# press key enter
time.sleep(1)

page.click("a#search_tab_position")
time.sleep(1)

for i in range(5):
    page.keyboard.down("End")
    # scrolling down
    time.sleep(0.5)

# return whole html
content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__FqChn")

for job in jobs:
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"
    title = job.find("strong", class_ = "JobCard_title__ddkwM").text
    company_name = job.find("span", class_ = "JobCard_companyName__vZMqJ").text
    # location = job.find("span", )
    reward = job.find("span", class_="JobCard_reward__sdyHn").text
    job_info = {
        "title":title,
        "company_name":company_name,
        "reward":reward,
        "link":link,
    }
    jobs_db.append(job_info)



file = open("jobs.csv", mode="w", encoding="utf-8", newline="")
writer = csv.writer(file)
writer.writerow(
    ["Title",
     "Company",
     "Location", 
     "Reward"])

for job in jobs_db:
    writer.writerow(job.values())
file.close()

