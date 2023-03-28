from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Disease
# Register your models here.
@admin.register(Disease)
class Diseaseadmin(ImportExportModelAdmin):
    list_display=['disease']