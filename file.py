

def save_to_file(file_name, jobs):
    file = open(f"db/{file_name}.csv", "w", encoding="utf-8")
    file.write("Title,Company,Reward,URL\n")
    
    for job in jobs:
        file.write(
            f"{job['title']},{job['company_name']},{job['reward']},{job['link']}\n"
        )
    file.close()