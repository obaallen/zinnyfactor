from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import user_job_map, user_detail, company
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

import base64
import requests

global level
global cat
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('https://zinnyfactor.com')
    else:
        posts = []
        # API call to get all current posts
        res = requests.get("http://www.zinnyfactor.com/wp-json/wp/v2/posts")
        if res.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")

        post_results = res.json()
        counter = 0

        for post_result in post_results:
            if counter == 3:
                break

            dt = datetime.strptime(post_result["date"], "%Y-%m-%dT%H:%M:%S")
            date = dt.strftime("%B %d, %Y")
            imagelink = post_result["_links"]["wp:featuredmedia"][0]["href"]
            res = requests.get(imagelink)
            imageurl = res.json()
            post = {
                "title": post_result["title"]["rendered"],
                "snippet": post_result["excerpt"]["rendered"],
                "image": imageurl["guid"]["rendered"],
                "date": date,
                "link": post_result["link"]
            }
            posts.append(post)
            counter += 1

        context = {
            "posts": posts
        }

        return render(request, "home/index.html", context)

def forum(request):
    # if not request.user.is_authenticated:
    #     return redirect('https://zinnyfactor.com')
    # else:
        # current_user = request.user
        # fullname = current_user.get_full_name()
        # details = user_detail.objects.get(user=current_user)
        # img_url = details.img_url
        # tagline = details.job_title + " at " + details.company.company_name
        # print (fullname)
        # context = {
        #     "fullname": fullname,
        #     "tagline": tagline,
        #     "img_url": img_url
        # }

        # return render(request, "zf-connect/forum.html", context)
        return render(request, "comingsoon/index.html")

def subscribe(request):
    email = request.POST.get('email', False)
    print(email)
    body = {
            "email_address": email,
            "status": "subscribed"
            }
    #
    # auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    # token_type, _, credentials = auth_header.partition(' ')
    #
    # expected = base64.b64encode(b'zinnyify:52fe88e70e42cee9cce82aa967306f34-us14').decode()
    #
    # if token_type != 'Basic' or credentials != expected:
    #     return HttpResponse(status=401)


    # API call to get all current posts
    res = requests.post("https://us14.api.mailchimp.com/3.0/lists/cc295c5a74/members/", auth=('zinnyify','52fe88e70e42cee9cce82aa967306f34-us14'), data=body)
    if res.status_code != 200:
        print(res.content)
        raise Exception("ERROR: API request unsuccessful.")

    return render(request, "comingsoon/thankyou.html")

def jobindex(request, page=0):
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

def saved(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    current_user = request.user
    maps = user_job_map.objects.filter(user=current_user).values('job_id')
    jobs = []

    print(maps)
    for map in maps:
        id = str(map["job_id"])
        url = "https://www.themuse.com/api/public/jobs/"+id
        # API call to get all current jobs
        res = requests.get(url,
                           params={"api_key": "eccc1f3fd28b1b61ce03bccc0befbcc8cef1e52ca9f241b5ef10209eee7fab03"})
        if res.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")

        job_result = res.json()
        job = {
            "ext_id": id,
            "title": job_result["name"],
            "company": job_result["company"]["name"],
            "location": job_result["locations"][0]["name"],
            "apply": job_result["refs"]["landing_page"]
        }
        jobs.append(job)

    context = {
        "jobs": jobs
    }
    return render(request, "jobs/saved.html", context)

@csrf_exempt
def user_map(request):
    job_id = request.POST["job_id"]
    current_user = request.user

    map = user_job_map.objects.all().filter(job_id=job_id, user=current_user)
    print(map)
    if not map:
        p = user_job_map(job_id=job_id, user=current_user)
        p.save()
    return HttpResponse('')

@csrf_exempt
def delete(request):
    job_id = request.POST["job_id"]
    current_user = request.user
    user_job_map.objects.filter(job_id=job_id, user=current_user).delete()
    return HttpResponse('')

def register(request):
    return render(request, "registration/register.html")

def registered(request):
    username = request.POST.get("username", False)
    password = request.POST.get("password", False)
    first_name = request.POST.get("first_name", False)
    last_name = request.POST.get("last_name", False)
    email = request.POST.get("email", False)
    jobtitle = request.POST.get("job_title", False)
    company = request.POST.get("company", False)
    years = request.POST.get("years", False)
    city = request.POST.get("city", False)
    province = request.POST.get("province", False)

    if not username or not password or not email:
        raise Http404("Something went wrong. Please go back and fill out your username, password and email")

    #register the user
    user = User.objects.create_user(username=username,
                                     email=email,
                                     password=password,
                                     first_name=first_name,
                                     last_name=last_name)

    detail = user_detail(jobtitle=jobtitle,
                         company=company,
                         experience_years=years,
                         city=city,
                         province=province,
                         user=user)
    detail.save()
    login(request, user)
    return redirect('index')

def login_page(request):
    return render(request, "registration/login.html")

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        raise Http404("user does not exist")
        return redirect('login_page')

def logout_view(request):
    logout(request)
    return redirect('login_page')
