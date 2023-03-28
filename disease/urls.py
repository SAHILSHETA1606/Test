from . import views
from django.urls import path,include
urlpatterns = [
    path('addDiseasefile/',views.Upload_Disease,name='uploaddisease' ),
    path('viewDisease/',views.view_Disease ,name='viewDisease'),
    path('addDisease/',views.addDisease ,name='addDisease'),
]