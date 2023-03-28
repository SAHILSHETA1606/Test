from importlib import import_module
from django.shortcuts import redirect,render
from .models import Report
from .resource import ReportResource
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def upload_report(request):
    if request.method=='POST':
        upload_report_resource=ReportResource()
        dataset=Dataset()
        new_report=request.FILES['myreport']

        if not new_report.name.endswith('xlsx'):
            messages.info(request,'wrong format valid xlsx')
            return render(request,'home/uploadexternalfiles.html')

        imported_data=dataset.load(new_report.read(),format='xlsx')
        for data in imported_data:
            value=Report(data[0],data[1])
            if not Report.objects.filter(report=data[1]).exists():
                t1=Report.objects.filter(report=data[1])
                print(t1)
                value.save()
            else:
                continue
    return render(request,'home/uploadexternalfiles.html')

def view_report(request):
    report=Report.objects.all()
    print(report)
    return render(request,'view_report.html',{'report':report})

def addreport(request):
    if request.method == 'POST':
        new_report=request.POST['report']
       
        d=Report(report=new_report)
        d.save()
    return redirect('uploadfile')
