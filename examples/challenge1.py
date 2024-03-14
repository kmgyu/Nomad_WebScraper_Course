from requests import get
from bs4 import BeautifulSoup
import requests


class Scrape:
  # 돚거돚거
  def __init__(self, title, company, location, tip, url):
    self.title = title
    self.company = company
    self.location = location
    self.tip = tip
    self.url = url

    if "*" not in self.tip:
      self.tip = "None"

  def printing(self):
    print("<Title>\n->", self.title)
    print("<Company>\n->", self.company)
    print("<Location>\n->", self.location)
    print("<Tooltip>\n->", self.tip)
    print("<URL>\n->", self.url)
    print(20 * '-')


def GetPage(tag):
  response = requests.get(
      f"https://remoteok.com/remote-{tag}-jobs",
      headers={
          "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      })
  soup = BeautifulSoup(response.text, "html.parser")
  jobs = soup.find("table", id="jobsboard").find_all("tr", class_="job")

  jobs_list = []

  # expart informations
  for job in jobs:
    title = job.find("h2", itemprop="title").text.replace("\n", "")
    company = job.find("h3", itemprop="name").text.replace("\n", "")

    locations = [
        location.text
        for location in job.find_all("div", class_="location")[:-1]
        if "tip" not in location.get("class", [])
    ]

    # for checking div only from td
    tip_div = job.find("td",
                       class_="company position company_and_position").find(
                           "div", class_="location tooltip")
    tip = tip_div.text if tip_div else "None"

    link = job.find("a")["href"]
    url = f"https://remoteok.com{link}"

    # Create a Scrape object with default location
    job_data = Scrape(title, company, locations or ["Unknown"], tip, url)
    jobs_list.append(job_data)  # Append the Scrape object to the jobs_list

  return jobs_list


# keywords
keywords = ["flutter", "python", "golang"]

# define lists
jobs_flutter = []
jobs_python = []
jobs_golang = []

for keyword in keywords:
  if keyword == "flutter":
    jobs_flutter = GetPage(keyword)
  elif keyword == "python":
    jobs_python = GetPage(keyword)
  elif keyword == "golang":
    jobs_golang = GetPage(keyword)

# print information we want
print(20 * "==")
print("Jobs related to Flutter\n")
for job in jobs_flutter:
  job.printing()
print("\n" + 20 * "==")
print("\nJobs related to Python\n")
for job in jobs_python:
  job.printing()
print("\n" + 20 * "==")
print("\nJobs related to Golang\n")
for job in jobs_golang:
  job.printing()

print("\n" + 20 * "==")
