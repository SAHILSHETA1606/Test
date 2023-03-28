from . import views
from django.urls import path,include
urlpatterns = [
    path('addMedcinefile/',views.Upload_Excel,name='uploadfile' ),
    path('viewMeds/',views.view_medicine ,name='viewMeds'),
    path('addMedcine/',views.addMedicine ,name='addMedicine'),
    
]

