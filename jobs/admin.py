from django.contrib import admin
from .models import user_job_map, company, user_detail

# Register your models here.

admin.site.register(user_job_map)
admin.site.register(company)
admin.site.register(user_detail)
