from importlib import import_module
from django.shortcuts import redirect,render
from .models import Disease
from .resource import DiseaseResource
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def Upload_Disease(request):
    if request.method=='POST':
        dis_resource=DiseaseResource()
        dataset=Dataset()
        new_disease=request.FILES['mydisease']

        if not new_disease.name.endswith('xlsx'):
            messages.info(request,'wrong format valid xlsx')
            return render(request,'upload_disease.html')

        imported_data=dataset.load(new_disease.read(),format='xlsx')
        for data in imported_data:
            value=Disease(data[0],data[1])
            if not Disease.objects.filter(disease=data[1]).exists():
                t1=Disease.objects.filter(disease=data[1])
                print(t1)
                value.save()
            else:
                continue
    return render(request,'home/uploadexternalfiles.html')

def view_Disease(request):
    disease=Disease.objects.all()
    print(disease)
    return render(request,'view_disease.html',{'disease':disease})

def addDisease(request):
    if request.method == 'POST':
        new_disease=request.POST['disease']
       
        d=Disease(disease=new_disease)
        d.save()
    return redirect('uploadfile')
