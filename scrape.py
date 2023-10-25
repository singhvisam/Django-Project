from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bsp

# Replace the uri string with your MongoDB deployment's connection string.
uri = "mongodb+srv://samitsinghvi:sam16%40MONGO@cluster0.v5kwwe5.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

# database and collection code goes here
db = client.Jobs
coll = db.python

url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=data+science&txtLocation='
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'}
r = requests.get(url, headers)
html = r.content

print(r.status_code)

soup = bsp(html, 'html.parser')
heading = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")

jobs = []
jobs_without_salary = []
i = 1
for job in heading:
    current_job = {}
    title = job.find('h3', class_="joblist-comp-name").text
    title = title.split('(')
    current_job['title'] = title[0].strip()
    skills = job.find('span', class_="srp-skills")
    current_job['skills'] = skills.text.strip()
    salary = job.find_all('li')[1]
    if salary.find('i').text != '₹':
        current_job['salary'] = 'N.A'
        jobs_without_salary.append(current_job)
        continue
    current_job['salary'] = str(salary.text)
    jobs.append(current_job)
coll.insert_many(jobs)
coll.insert_many(jobs_without_salary)

print(jobs_without_salary)
    
