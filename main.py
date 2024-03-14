from flask import Flask, render_template, request, redirect, send_file
from extractor.extractor import PageExtractor
from file import save_to_file

app = Flask("JobScrapper")

# fake db
db = {}

@app.route("/")
def home():
    return render_template("home.html", name="nico")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    
    if keyword in db:
        jobs = db[keyword]
    else:
        jobs = PageExtractor(keyword=keyword).extract()
        db[keyword] = jobs
        save_to_file(keyword, jobs)
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    try:
        keyword = request.args.get("keyword")
        if not keyword:
            raise Exception()
        jobs = db[keyword]
        if not jobs:
            raise Exception()
        return send_file(f"db/{keyword}.csv", as_attachment=True)
    except:
        return redirect("/")


app.run()

