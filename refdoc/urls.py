from . import views
from django.urls import path,include
urlpatterns = [
    #path('addRefDocfile',views.UploadRefDoc,name='uploadRefDoc' ),
    path('viewRefDoc/',views.view_refDoc ,name='viewRefDoc'),
    path('addRefDoc/<int:i>',views.addRefdoc ,name='addRefdoc'),
    path('ref_doctor_all_groups',views.ref_doctor_all_groups,name='ref_doctor_all_groups'),
    path('ref_doctor_create_group',views.ref_doctor_create_group, name='ref_doctor_create_group'),
    path('ref_doctor_particular_group/<int:i>',views.ref_doctor_particular_group, name='ref_doctor_particular_group'),
    path('searchrefdoc/<int:i>',views.search_ref_doc, name='searchrefdoc'),
    path('print_ref_doctor/<int:i>',views.print_ref_doctor, name='print_ref_doctor'),
    path('deleterefdocgroup/<int:i>',views.delete_ref_doc_group, name='deleterefdocgroup'),
    path('searchrefdocgroup',views.search_ref_doc_group, name='searchrefdocgroup'),
    path('get_doc_names/',views.get_doc_names, name='get_doc_names')
    #path('patient_group',views.patient_group, name='patient_group'),
]