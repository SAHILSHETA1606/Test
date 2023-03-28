from importlib import import_module
from django.shortcuts import render,redirect
from .models import Symptoms
from .resource import SymptomsResource
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def Upload_Symptoms(request):
    if request.method=='POST':
        dis_resource=SymptomsResource()
        dataset=Dataset()
        new_symptoms=request.FILES['mysymptoms']

        if not new_symptoms.name.endswith('xlsx'):
            messages.info(request,'wrong format valid xlsx')
            return render(request,'upload_symptoms.html')

        imported_data=dataset.load(new_symptoms.read(),format='xlsx')
        for data in imported_data:
            value=Symptoms(data[0],data[1])
            if not Symptoms.objects.filter(symptoms=data[1]).exists():
                value.save()
            else:
                continue
    return render(request,'home/uploadexternalfiles.html')

def view_Symptoms(request):
    symptoms=Symptoms.objects.all()
    print(symptoms)
    return render(request,'view_symptoms.html',{'symptoms':symptoms})

def addSymptoms(request):
    if request.method == 'POST':
        new_symptoms=request.POST['symptoms']
        
        d=Symptoms(symptoms=new_symptoms)
        d.save()
    return redirect('uploadfile')
