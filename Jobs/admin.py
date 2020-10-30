from django.contrib import admin
from Jobs.models import JobCategory,UserJob, JobMaterial

# Register your models here.

admin.site.register(JobCategory)
admin.site.register(UserJob)
admin.site.register(JobMaterial)