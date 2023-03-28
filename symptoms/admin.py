from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Symptoms
# Register your models here.
@admin.register(Symptoms)
class Symptomsadmin(ImportExportModelAdmin):
    list_display=['symptoms']