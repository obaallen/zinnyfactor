from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page>", views.index, name="jobindex"),
    path("jobresult", views.jobresult, name="jobresult"),
    path("jobresult/<int:page>", views.jobresult, name="jobresult"),
    path("jobsearch", views.jobsearch, name="jobsearch"),
]
