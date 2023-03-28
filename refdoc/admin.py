from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import RefDoc
from .models import Doc_group
# Register your models here.
@admin.register(RefDoc)
class RefDocadmin(ImportExportModelAdmin):
    list_display=('name','details')

admin.site.register(Doc_group)
