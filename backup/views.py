from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
# Create your views here.
from script import backup
import time
# import schedule
def excelreport(request):
    backup()
    messages.success(request,'Backup done')
    return redirect('/')
  
# schedule.every(2).minutes.do(backup)
# while True:
#     schedule.run_pending()
#     time.sleep(1)