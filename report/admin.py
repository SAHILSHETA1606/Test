from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Report
# Register your models here.
@admin.register(Report)
class Reportadmin(ImportExportModelAdmin):
    list_display=['report']