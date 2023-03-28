from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('',views.statistic, name='home'),
     path('patients',views.main_patient, name='main_patient'),
     path('addpatient',views.addpatient, name='addpatient'),
     path('deletepatient/<int:i>',views.delete_patient,name='deletepatient'),
     path('patient_details',views.patient_details, name='patient_details'),
     path('settle_account/<int:pid>',views.settle_account, name='settle_account'),
     path('viewdetail/<int:i>',views.viewdetail, name='viewdetail'),
     path('editpatientdetail/<int:i>',views.editpatientdetail, name='editpatientdetail'),
     path('addpatient_health_details/<int:i>',views.addpatient_health_details, name='addpatient_health_details'),
     path('edit_add_patient_health_detail/<int:i>/<int:k>',views.edit_add_patient_health_detail, name='edit_add_patient_health_detail'),
     path('patient_health_details/<int:i>',views.patient_health_details, name='patient_health_details'),
     path('editpatient_health_detail/<int:i>/<int:k>',views.editpatient_health_detail, name='editpatient_health_detail'),
     path('visit_summary',views.visit_summary, name='visit_summary'),
     path('particular_person_summary/<int:i>',views.particular_person_summary, name='particular_person_summary'),
     path('summary/<int:i>/<int:j>',views.summary, name='summary'),
     path('patient_group',views.patient_group, name='patient_group'),
     path('all_group',views.all_group, name='all_group'),
     path('deletegroup/<int:i>',views.delete_group, name='deletegroup'),
     path('create_group',views.create_group, name='create_group'),
     path('particular_group/<int:i>',views.particular_group, name='particular_group'),
     path('addpatient_health_details/<str:fname>/<str:lname>',views.addpatient_health_details, name='addpatient_health_details'),
     path('statistic',views.statistic,name='statistic'),
     path('searchPatient',views.search_patient,name='searchPatient'),
     path('searchPatientGroup',views.search_patient_Group,name='searchPatientGroup'),
     path('searchPatientSummary',views.search_patient_summary,name='searchPatientSummary'),
     path('today_patient',views.today_patient,name='today_patient')
     #path('print_prescription/<int:pid>',views.print_prescription,name='print_prescription'),
     


]