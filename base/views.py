from django.shortcuts import render
from django.http import HttpResponse

from pymongo import MongoClient
client = MongoClient('mongodb+srv://samitsinghvi:sam16%40MONGO@cluster0.v5kwwe5.mongodb.net/')
db = client['Jobs']
coll = db.python

cursor = coll.find({})

jobs = []
for i in cursor:
    salary = i['salary']
    salary = salary.split()
    print(salary)
    jobs.append(i)
    print(i['title'])


# print(jobs)

def home(request):
    context = {'jobs' : jobs}
    return render(request, 'base/home.html', context)

def room(request):
    return render(request, 'base/room.html')
title = None

def edit_job(request):
    title = request.POST['title']
    context = {'title' : title}
    return render(request, 'base/edit_job.html', context)
    

def edit_in_mongo(request):
    skills = request.POST['skills']
    salary = request.POST['salary']
    title_query = request.POST['title']

    for job in jobs:
        if job['title'] == title_query:
            job['skills'] = skills
            job['salary'] = salary
    print(title_query)
    myQuery = {'title' : title_query}
    newValues = {'$set' : {'skills' : skills, 'salary' : salary}}
    coll.update_one(myQuery, newValues)
    return render(request, 'base/deleted.html')

# def search_job(request):
#     if request.method == "POST":
#         searched = request.POST['searched']
#         print("#### HEY I HAVE VALUE OF SEARCHED = " + str(searched))
#         return render(request, 'base/search.html', {'searched' : searched})
#     else: 
#         return render(request, 'base/search.html', {})
    
def search_job(request):
    print(request.POST)
    if request.method == "POST":
        searched = request.POST['searched']
        context = {'jobs' : jobs, 'searched': searched}
        return render(request, 'base/search.html',context)
    else:
        return render(request, 'base/search.html', {})


from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

def delete_job(request, title):
    try:
        doc = {
            'title': title
        }
        result = coll.delete_one(doc)

        if result.deleted_count == 0:
            raise Http404("Job not found")
        else:
            for job in jobs:
                if job['title'] == title:
                    jobs.remove(job)
                    break
            # Redirect to the home page (you can use the URL name or path)
            return render(request, 'base/deleted.html') # Replace 'home' with your actual URL name
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
