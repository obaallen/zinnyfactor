from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

import base64
import requests

global level
global cat
# Create your views here.
def index(request, page=0):
    jobs = []
    # API call to get all current jobs
    res = requests.get("https://www.themuse.com/api/public/jobs",
                       params={"page": page,"location": "Toronto, Canada", "api_key": "eccc1f3fd28b1b61ce03bccc0befbcc8cef1e52ca9f241b5ef10209eee7fab03"})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    data = res.json()
    job_results = data["results"]
    previous_page = data["page"] - 1
    page_number = data["page"] + 1
    last_page = data["page_count"] + 1

    if previous_page < 0:
        previous_page = 0

    for job_result in job_results:
        job = {
            "ext_id": job_result["id"],
            "title": job_result["name"],
            "company": job_result["company"]["name"],
            "location": job_result["locations"][0]["name"],
            "apply": job_result["refs"]["landing_page"]
        }
        jobs.append(job)

    context = {
        "jobs": jobs,
        "page": page_number,
        "previous_page": previous_page,
        "last_page": last_page,
        "link": "jobindex"
    }
    return render(request, "jobs/index.html", context)

def jobresult(request, page=0):
    joblevel = request.POST.get('joblevel', False)
    category = request.POST.get('category', False)

    if joblevel is None and category is None and (level or cat):
        joblevel = level
        category = cat
    elif joblevel or category:
        level = joblevel
        cat = category


    jobs = []
    # API call to get all current jobs
    res = requests.get("https://www.themuse.com/api/public/jobs",
                       params={"page": page, "location": "Toronto, Canada", "category": category, "level": joblevel, "api_key": "eccc1f3fd28b1b61ce03bccc0befbcc8cef1e52ca9f241b5ef10209eee7fab03"})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    data = res.json()
    job_results = data["results"]
    previous_page = data["page"] - 1
    page_number = data["page"] + 1
    last_page = data["page_count"] + 1

    if previous_page < 0:
        previous_page = 0

    for job_result in job_results:
        job = {
            "ext_id": job_result["id"],
            "title": job_result["name"],
            "company": job_result["company"]["name"],
            "location": job_result["locations"][0]["name"],
            "apply": job_result["refs"]["landing_page"]
        }
        jobs.append(job)

    context = {
        "jobs": jobs,
        "page": page_number,
        "previous_page": previous_page,
        "last_page": last_page,
        "link": "jobresult"
    }
    return render(request, "jobs/index.html", context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def jobsearch(request):
    q = request.POST.get('query', False)
    l = request.POST.get('city', False)
    country = request.POST.get('country', False)

    if country is False:
        country = 'canada'
        l = ''
    print(q)
    if q is False:
        q = ''

    pub_id = 'adcf451f'
    format = 'json'
    userip = get_client_ip(request)
    useragent = request.META['HTTP_USER_AGENT']

    print (l)
    print (country)
    print(useragent)
    print(userip)
    jobs = []
    # API call to get all current jobs
    res = requests.get("https://neuvoo.com/services/api-new/search",
                       params={"ip": userip, "useragent": useragent, "country": country, "contenttype": "organic", "publisher": pub_id, "k": q, "l": l, "format": format})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    data = res.json()
    print (data)
    if data["results"] is None:
        job = {
            "title": "No Jobs Found"
        }
        jobs.append(job)
    else:
        job_results = data["results"]

        for job_result in job_results:
            job = {
                "ext_id": job_result["jobkey"],
                "title": job_result["jobtitle"],
                "company": job_result["company"],
                "location": job_result["formattedLocation"],
                "apply": job_result["url"],
                "snippet": job_result["description"]
            }
            jobs.append(job)

    context = {
        "jobs": jobs
    }
    return render(request, "jobs/results.html", context)
