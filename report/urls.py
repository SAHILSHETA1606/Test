from . import views
from django.urls import path,include
urlpatterns = [
    path('addReportfile/',views.upload_report,name='uploadreport' ),
    path('viewReport/',views.view_report ,name='viewreport'),
    path('addReport/',views.addreport ,name='addreport'),
]