from . import views
from django.urls import path,include
urlpatterns = [
    path('addSymptomsfile/',views.Upload_Symptoms,name='uploadSymptoms' ),
    path('viewSymptoms/',views.view_Symptoms ,name='viewSymptoms'),
    path('addSymptoms/',views.addSymptoms ,name='addSymptoms'),
]