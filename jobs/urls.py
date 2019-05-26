from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("jobs", views.jobindex, name="jobindex"),
    path("jobs/<int:page>", views.jobindex, name="jobindex"),
    path("register", views.register, name="register"),
    path("registered", views.registered, name="registered"),
    path("login", views.login_page, name="login_page"),
    path("loggingIn", views.login_view, name="login_view"),
    path("loggingOut", views.logout_view, name="logout_view"),
    path("jobs/jobresult", views.jobresult, name="jobresult"),
    path("jobs/jobresult/<int:page>", views.jobresult, name="jobresult"),
    path("jobs/jobsearch", views.jobsearch, name="jobsearch"),
    path("jobs/user_map", views.user_map, name="user_map"),
    path("jobs/saved", views.saved, name="saved"),
    path("jobs/delete", views.delete, name="delete"),
    path("zf-connect", views.forum, name="forum"),
    path("subscribe", views.subscribe, name="subscribe"),
]
