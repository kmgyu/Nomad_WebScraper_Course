from playwright.sync_api import sync_playwright
import time

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

# page.goto("https://google.com")
page.goto("https://www.wanted.co.kr/jobsfeed")

time.sleep(2)

page.click("button.Aside_searchButton__Xhqq3")
# same code down here
# page.locator("button.Aside_searchButton__Xhqq").click()

time.sleep(2)

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
# you can get by label, id... etc

page.keyboard.down("Enter")
# press key enter
time.sleep(4)

page.click("a#search_tab_position")
time.sleep(4)

for i in range(5):
    page.keyboard.down("End")
    # scrolling down
    time.sleep(0.5)

# return whole html
content = page.content()

p.stop()