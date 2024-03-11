import requests
import bs4

# refactor this or... idk
base = "https://weworkremotely.com"
url = base + "/categories/remote-full-stack-programming-jobs"

response = requests.get(url)

soup = bs4.BeautifulSoup(response.content, "html.parser")


jobs = soup.find("section",
                 class_ = "jobs").find_all("li")[1:-1]
# it returns bs4.element.ResultSet

all_jobs = [] # the name... refactor this. i don't like it

for job in jobs:
    title = job.find("span", class_= "title")
    region = job.find("span", class_= "region")
    company, position, _ = job.find_all("span", class_= "company")
    
    job_url = job.find("div", class_ = "tooltip--flag-logo").next_sibling
    if job_url: # if not None
        job_url = job_url["href"]
    
    # append job info
    all_jobs.append({"title" : title.text,
                     "region" : region.text,
                     "company" : company.text,
                     "position" : position.text,
                     "url" : base + job_url,
                     })
    
print(all_jobs[0])


