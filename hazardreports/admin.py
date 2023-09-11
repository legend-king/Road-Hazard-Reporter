from django.contrib import admin
from .models import HazardReport, HazardCategory
# Register your models here.
admin.site.register(HazardCategory)
admin.site.register(HazardReport)