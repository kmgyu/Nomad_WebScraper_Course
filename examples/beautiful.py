import requests
import bs4

def scrape_page(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("section",
                    class_ = "jobs").find_all("li")[1:-1]
    # type: bs4.element.ResultSet
    
    # all jobs in this page

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


def get_page_length(url):
    # it returns page length
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    page_length = len(soup.find("div", class_ = "pagination").find_all("span", class_="page"))
    
    return page_length
    

all_jobs = [] # the name... refactor this. i don't like it

# refactor this or... idk
# base url is we work remotely website
base = "https://weworkremotely.com"
target_url = base + "/categories/remote-full-stack-programming-jobs"
target_url2 = base + "/remote-full-time-jobs"
pagination = "?page="

page_length = get_page_length(target_url2)

for i in range(1, page_length+1):
    page_url = f'{target_url+pagination}{i}'
    scrape_page(page_url)

print(all_jobs[1])