from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class user_job_map(models.Model):
    job_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class company(models.Model):
    company_name = models.CharField(max_length=50)

class user_detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50)
    company = models.ForeignKey(company, on_delete=models.CASCADE)
    experience_years = models.FloatField()
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    img_url = models.CharField(max_length=150, default="{% static 'zf-connect/images/avatar.svg' %}")
