from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from django.core.paginator import Paginator
import math, random
from django.db.models import Q
from .models import patient_detail
from .models import patient_health_detail
from .models import Patient_group
from .models import Account
from medicine.models import Medicine
from refdoc.models import RefDoc
from refdoc.models import Doc_group
from symptoms.models import Symptoms
from disease.models import Disease
from json import dumps
import datetime
import json as simplejson
import json
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Sum
from django.db.models.functions import TruncMonth,TruncYear
from django.db.models.functions import ExtractMonth
from django.db.models.functions import ExtractYear
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def home(request):

    
    return render(request,'home/index.html')


def main_patient(request):
    patient=patient_detail.objects.all().order_by('-id')
    print(patient)
    paginator=Paginator(patient, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'home/patients.html',{'patient':patient,'page_obj':page_obj})

def addpatient(request):
    return render(request,'home/addpatient.html')

def patient_details(request):

    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        note = request.POST['note']
        age = request.POST['age']
        weight = request.POST['weight']
        contact = request.POST['contact']
        address = request.POST['address']
        rperson = request.POST['rperson']
        gender = request.POST['gender']

        user = patient_detail( fname = fname,lname = lname,note = note,age = age, weight =  weight,contact = contact,address = address , rperson = rperson)
        user.save()

        return redirect('/patients')
    else:
        return redirect('/')


def viewdetail(request,i):
    #here i is patient id
    patient  = patient_detail.objects.get(id=i)
    return render(request,'home/particular_patient_detail.html',{'patient':patient})

def editpatientdetail(request,i):
        if request.method=="POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            note = request.POST['note']
            age = request.POST['age']
            weight = request.POST['weight']
            contact = request.POST['contact']
            address = request.POST['address']
            rperson = request.POST['rperson']

            a=patient_detail.objects.get(id = i)
            a.fname = fname
            a.lname = lname
            a.note = note
            a.age = age
            a.weight = weight
            a.contact = contact
            a.address = address
            a.rperson = rperson
            a.save()
            patient  = patient_detail.objects.get(id=i)
            return render(request,'home/particular_patient_detail.html',{'patient':patient})
        else:
            patient  = patient_detail.objects.get(id=i)
            return render(request,'home/particular_patient_edit_detail.html',{'patient':patient})


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def addpatient_health_details(request,i):
    #i is pid
    patient_health = patient_detail.objects.get(id=i)
    medi=Medicine.objects.all()
    symp=Symptoms.objects.all()
    dies=Disease.objects.all()
    docgroup=Doc_group.objects.all()
    last_five_visit_summary = patient_health_detail.objects.filter(patient_id=i).order_by('-id')[:5]
    last_five_visit_summary_details=[]
   
    for p in last_five_visit_summary:
        jsonDec = json.decoder.JSONDecoder()
        prescription = jsonDec.decode(p.prescription)
        medicine_outside = jsonDec.decode(p.medicine_outside)
        note = jsonDec.decode(p.note)
        note_outside = jsonDec.decode(p.note_outside)
        m_time = jsonDec.decode(p.m_time)
        time_outside = jsonDec.decode(p.time_outside)
        schd_time = jsonDec.decode(p.schd_time)
        schd_outside = jsonDec.decode(p.schd_outside)
        countt = jsonDec.decode(p.countt)
        count_outside = jsonDec.decode(p.count_outside)
       
        print('-------this are medicines data def addpatient health details-------')
        print(prescription)

        
        last_five_visit_summary_details.append({"id":p.id,"date":p.date,"diagnosis": p.diagnostic,"symptoms":p.symptoms,'prescription':prescription,'medicine_outside':medicine_outside,'note':note,'note_outside':note_outside,'m_time':m_time,'time_outside':time_outside,'schd_time':schd_time,'schd_outside':schd_outside,'countt':countt,'count_outside':count_outside})
    
    
    
    # print("------------------this is patient--------------")
    # print(last_five_visit_summary)
    # print("------------------this is individual--------------")
    listnum = [1,2,3,4,5]
    last_five_visit_summary_details1=[]
    last_five_visit_prescription_details=[]
    # for i in last_five_visit_summary:
    #     print(i.id)
    #     print(i.date)
    #     print(i.prescription)
    #     print(i.diagnostic)
    #     print(i.symptoms)
    



    for p,n in zip(last_five_visit_summary_details,listnum):

        last_five_visit_summary_details1.append({"p":p,"n":n})   
    
    return render(request,'home/addpatient_health.html',{'patient':patient_health,'pid':patient_health.id,'medi':medi,'symp':symp,'dies':dies,'docgroup':docgroup,'last_five_visit_summary_details':last_five_visit_summary_details1})

                                                        
def patient_health_details(request,i):
    # i is pid
    if request.method=="POST":
        t1=patient_detail.objects.get(id=i)
        fname=t1.fname
        lname=t1.lname
        symptoms = request.POST.getlist('symptoms')
        diagnostic = request.POST.getlist('diagnostic')
        note = request.POST.getlist('note')
        prescription = request.POST.getlist('prescription')
        timee = request.POST.getlist('time')
        schd_time = request.POST.getlist('schdtime')
        countt = request.POST.getlist('countt')
        printpres = request.POST.getlist('printpres')
        report = request.POST['report']
        fees = request.POST['fees']
        paid = request.POST['paid']
        
        print('-------this are medicines data def patient health details-------')
        print(printpres)

        
        schd_time.pop(0)
        countt.pop(0)
        timee.pop(0)
        note.pop(0)

        print('-------this are medicines data 1 def patient health details-------')
        print(prescription) 
        print(schd_time) 
        print(timee)
        print(note)
        print(countt) 
        

        #------------------------------logic for seprating scdh time----------
        medicine_outside = []
        medcine_temp =[]
        schd_outside =[]
        time_outside =[] 
        note_outside =[]
        count_outside =[]  
            
        for l in printpres:# for converting to string
            a=json.loads(l)
            medicine_outside.append(a[2])
            time_outside.append(a[3])
            note_outside.append(a[0])
            count_outside.append(a[1])
            schd_outside.append(a[4])

        
        for j in medicine_outside: #for removing medicine from precription
            if j in prescription:
                prescription.remove(j)

        for j in time_outside: #for removing medicine from precription
            if j in timee:
                timee.remove(j)

        for j in note_outside: #for removing medicine from precription
            if j in note:
                note.remove(j)

        for j in count_outside: #for removing medicine from precription
            if j in countt:
                countt.remove(j)

        for j in schd_outside: #for removing medicine from precription
            if j in schd_time:
                schd_time.remove(j)
        

        print('-------this are medicines out data def patient health details-------')
        print(medicine_outside)
        print(schd_outside) 
        print(time_outside)
        print(note_outside)
        print(count_outside)  
                
        # schd_outside.pop(0)
        # count_outside.pop(0)
        # time_outside.pop(0)
        # note_outside.pop(0)


        


        try:           #---------for ref doc
            refdoc = request.POST['refdoc']
        except MultiValueDictKeyError:
            refdoc = ''
            
        date = datetime.date.today()
        time=datetime.datetime.now().time()
        paid_og=paid

        #--------------------calculation of settleing account when extra or lee money is added-------------------

        patient_all_visit_acc=patient_health_detail.objects.filter(patient_id=i)

        fees1=int(fees)
        paid1=int(paid)
        j=0
        for j in patient_all_visit_acc:

            if fees1 > paid1:

                if j.paid > j.fees:
                
                    print('this is >')
                    a = fees1-paid1
                    b=j.paid-j.fees
                    c=a-b
                   #if c>=0:
                    print('-this is b-')
                    print(b)
                    j.paid=j.paid-b
                    print(paid1)
                    paid1 = paid1+b
                    print(paid1)
                    paid = paid1
                    
                    
                    b=patient_health_detail.objects.get(id=j.id)
                    b.paid=j.paid
                    b.left_from_doc=b.paid-b.fees
                    b.save()

            elif fees1 < paid1:
                
                if j.paid < j.fees :
                    print('this is <')
                    a= paid1 - fees1
                    b=j.fees-j.paid
                    print('-----------')
                    print(a)
                    print(b)
                    if a>=b:
                        
                        if a>b:
                            j.paid=j.paid+b
                            #a=a-b
                            print('this is a>b')
                            print(a)
                    
                            paid1=paid1-b
                            paid=paid1
                        elif a==b:
                            print('this is a==b')
                            print(a)
                            j.paid=j.paid+b
                            paid1=paid1-a
                            paid=paid1


                    elif a<b:
                        
                        print('this is a<b')
                        j.paid=j.paid+a
                        print(j.paid)
                        paid1=paid1-a
                        print(paid1)
                        paid=paid1
                   

                    b=patient_health_detail.objects.get(id=j.id)
                    b.paid=j.paid
                    b.left_from_patient=b.fees-b.paid
                    b.save()

               
        p1=patient_detail.objects.get(id=i)
        user = patient_health_detail(patient_id=p1,fname = fname,lname = lname,report=report,refdoc=refdoc,date=date,time=time,fees=fees,paid=paid,paid_original=paid_og)
        
        
        listIWantToStore1 = prescription
        user.prescription = json.dumps(listIWantToStore1)

        listIWantToStore2 = note
        user.note = json.dumps(listIWantToStore2)

        listIWantToStore3 = timee
        user.m_time = json.dumps(listIWantToStore3)

        listIWantToStore4 = countt
        user.countt = json.dumps(listIWantToStore4)

        listIWantToStore5 = symptoms
        user.symptoms = json.dumps(listIWantToStore5)

        listIWantToStore6 = diagnostic
        user.diagnostic = json.dumps(listIWantToStore6)

        listIWantToStore7 = schd_time
        user.schd_time = json.dumps(listIWantToStore7)




        listIWantToStore8 = medicine_outside
        user.medicine_outside = json.dumps(listIWantToStore8)

        listIWantToStore9 = schd_outside
        user.schd_outside = json.dumps(listIWantToStore9)

        listIWantToStore10 = time_outside
        user.time_outside = json.dumps(listIWantToStore10)

        listIWantToStore11 = note_outside
        user.note_outside = json.dumps(listIWantToStore11)

        listIWantToStore12 = count_outside
        user.count_outside = json.dumps(listIWantToStore12)

        user.save()
        patient = patient_detail.objects.all()

        
        return redirect(reverse('addpatient_health_details', kwargs={'i':i}))
        #return render(request,'home/index.html')#'home.html',{'patient':patient})


def editpatient_health_detail(request,i,k):
    # i is pid # k is visit no
    print(i)
    if request.method=="POST":
        t1=patient_detail.objects.get(id=i)
        fname=t1.fname
        lname=t1.lname
        symptoms = request.POST.getlist('symptoms')
        diagnostic = request.POST.getlist('diagnostic')
        note = request.POST.getlist('note')
        prescription = request.POST.getlist('prescription')
        m_time = request.POST.getlist('time')
        schd_time = request.POST.getlist('schdtime')
        countt = request.POST.getlist('countt')
        printpres = request.POST.getlist('printpres')
        report = request.POST['report']
        fees = request.POST['fees']
        paid = request.POST['paid']

        print('-------this are medicines data-------')
        print(printpres)
        #------------------------------logic for seprating scdh time----------
        medicine_outside = []
        schd_outside =[]
        time_outside =[] 
        note_outside =[]
        count_outside =[]  
            
        for l in printpres:# for converting to string
            a=json.loads(l)
            
            medicine_outside.append(a[2])
            time_outside.append(a[3])
            note_outside.append(a[0])
            count_outside.append(a[1])
            schd_outside.append(a[4])

        
        for j in medicine_outside: #for removing medicine from precription
            if j in prescription:
                prescription.remove(j)

        for j in time_outside: #for removing medicine from precription
            if j in m_time:
                m_time.remove(j)

        for j in note_outside: #for removing medicine from precription
            if j in note:
                note.remove(j)

        for j in count_outside: #for removing medicine from precription
            if j in countt:
                countt.remove(j)

        for j in schd_outside: #for removing medicine from precription
            if j in schd_time:
                schd_time.remove(j)
        

        print('------- edit patient detILAS def this are medicines outside data-------')
        print(medicine_outside)
        print(schd_outside) 
        print(time_outside)
        print(note_outside)
        print(count_outside)  
                

        try:           #---------for ref doc
            refdoc = request.POST['refdoc']
        except MultiValueDictKeyError:
            refdoc = ''
            
        date = datetime.date.today()
        time=datetime.datetime.now().time()
        paid_og=paid

        print('------- edit patient detILAS def this are medicines data-------')
        print(note)
        print(prescription)
        print(m_time)
        print(countt)
        print(schd_time)
        # print('-----------------')
        # print(printpres)
        #--------------------calculation of settleing account when extra or lee money is added-------------------

        patient_all_visit_acc=patient_health_detail.objects.filter(patient_id=i)

        fees1=int(fees)
        paid1=int(paid)
        
        for j in patient_all_visit_acc:
            if fees1 > paid1:
                if j.paid > j.fees:
                    print('this is >')
                    a = fees1-paid1
                    b=j.paid-j.fees
                    c=a-b
                    #if c>=0:
                    print('-this is b-')
                    print(b)
                    j.paid=j.paid-b
                    print(paid1)
                    paid1 = paid1+b
                    print(paid1)
                    paid = paid1
                    
                    
                    b=patient_health_detail.objects.get(id=j.id)
                    b.paid=j.paid
                    b.left_from_doc=b.paid-b.fees
                    b.save()

            elif fees1 < paid1:
                if j.paid < j.fees :
                    print('this is <')
                    a= paid1 - fees1
                    b=j.fees-j.paid
                    print('-----------')
                    print(a)
                    print(b)
                    if a>=b:
                        
                        if a>b:
                            j.paid=j.paid+b
                            #a=a-b
                            print('this is a>b')
                            print(a)
                    
                            paid1=paid1-b
                            paid=paid1
                        elif a==b:
                            print('this is a==b')
                            print(a)
                            j.paid=j.paid+b
                            paid1=paid1-a
                            paid=paid1

                    elif a<b:
                        print('this is a<b')
                        j.paid=j.paid+a
                        print(j.paid)
                        paid1=paid1-a
                        print(paid1)
                        paid=paid1

                    b=patient_health_detail.objects.get(id=j.id)
                    b.paid=j.paid
                    b.left_from_patient=b.fees-b.paid
                    b.save()
                    
        patient_detail_object = patient_detail.objects.get(id=i)
        patient_health_detail_object = patient_health_detail.objects.get(id=k)

        patient_health_detail_object.patient_id = patient_detail_object
        patient_health_detail_object.fname =fname
        patient_health_detail_object.lname = lname
        patient_health_detail_object.report = report
        patient_health_detail_object.refdoc = refdoc
        patient_health_detail_object.date = date
        patient_health_detail_object.time = time
        patient_health_detail_object.fees = fees
        patient_health_detail_object.paid = paid
        patient_health_detail_object.paid_original = paid_og

        
        listIWantToStore1 = prescription
        patient_health_detail_object.prescription = json.dumps(listIWantToStore1)

        listIWantToStore2 = note
        patient_health_detail_object.note = json.dumps(listIWantToStore2)

        listIWantToStore3 = m_time
        patient_health_detail_object.m_time = json.dumps(listIWantToStore3)

        listIWantToStore4 = countt
        patient_health_detail_object.countt = json.dumps(listIWantToStore4)

        listIWantToStore5 = symptoms
        patient_health_detail_object.symptoms = json.dumps(listIWantToStore5)

        listIWantToStore6 = diagnostic
        patient_health_detail_object.diagnostic = json.dumps(listIWantToStore6)

        listIWantToStore7 = schd_time
        patient_health_detail_object.schd_time = json.dumps(listIWantToStore7)

        listIWantToStore8 = medicine_outside
        patient_health_detail_object.medicine_outside = json.dumps(listIWantToStore8)

        listIWantToStore9 = schd_outside
        patient_health_detail_object.schd_outside = json.dumps(listIWantToStore9)

        listIWantToStore10 = time_outside
        patient_health_detail_object.time_outside = json.dumps(listIWantToStore10)

        listIWantToStore11 = note_outside
        patient_health_detail_object.note_outside = json.dumps(listIWantToStore11)

        listIWantToStore12 = count_outside
        patient_health_detail_object.count_outside = json.dumps(listIWantToStore12)

        patient_health_detail_object.save()
        return redirect(reverse('addpatient_health_details', kwargs={'i':i}))


def edit_add_patient_health_detail(request,i,k):
    patient = patient_detail.objects.get(id=i)
    medi=Medicine.objects.all()
    symp=Symptoms.objects.all()
    dies=Disease.objects.all()
    docgroup=Doc_group.objects.all()
    patient_health = patient_health_detail.objects.get(id=k)

    prescription_total =[]
    note_total = []
    time_total = []
    schd_time_total = []
    count_total = []

    jsonDec = json.decoder.JSONDecoder()
    symptoms = jsonDec.decode(patient_health.symptoms)
    jsonDec = json.decoder.JSONDecoder()
    diagnosis = jsonDec.decode(patient_health.diagnostic)

    prescription  = jsonDec.decode(patient_health.prescription)
    note  = jsonDec.decode(patient_health.note)
    m_time  = jsonDec.decode(patient_health.m_time)
    schd_time  = jsonDec.decode(patient_health.schd_time)
    countt  = jsonDec.decode(patient_health.countt)

    medicine_outside  = jsonDec.decode(patient_health.medicine_outside)
    schd_outside  = jsonDec.decode(patient_health.schd_outside)
    time_outside  = jsonDec.decode(patient_health.time_outside)
    note_outside  = jsonDec.decode(patient_health.note_outside)
    count_outside  = jsonDec.decode(patient_health.count_outside)

    prescription_total=prescription+medicine_outside
    note_total=note+note_outside
    time_total=m_time+time_outside
    schd_time_total=schd_time+schd_outside
    count_total=countt+count_outside

    note_total.pop(0)
    time_total.pop(0)
    schd_time_total.pop(0)
    count_total.pop(0)

    fees=patient_health.fees
    paid=patient_health.paid
    investigate=patient_health.report
    
    prescription_listJSON = json.dumps(prescription_total)
    note_listJSON = json.dumps(note_total)
    time_listJSON = json.dumps(time_total)
    schd_time_listJSON = json.dumps(schd_time_total)
    count_listJSON = json.dumps(count_total)
    

    return render(request,'home/edit_patient_healthdetails.html',{'patient':patient,'pid':i,'vid':k,'medi':medi,'symp':symp,'dies':dies,'docgroup':docgroup,'symptoms':symptoms,'diagnosis':diagnosis,'fees':fees,'paid':paid,'investigate':investigate,'prescription':prescription_listJSON,'note':note_listJSON,'time':time_listJSON,'schd_time':schd_time_listJSON,'count':count_listJSON})

def calclulation(i,j,pid):
    if i == j:
        Account.objects.filter(patient_id = pid).update(tleft_from_patient=0,tleft_from_doc=0)
        return 0
    elif i > j:
        c=i-j
        Account.objects.filter(patient_id = pid).update(tleft_from_patient=c,tleft_from_doc=0)
        return c
    elif j > i:
        c=j-i
        Account.objects.filter(patient_id = pid).update(tleft_from_doc=c,tleft_from_patient=0)
        return c

def summary1(i,j):
    s=patient_health_detail.objects.get(id=i)
    #j is patient id and  i is visit no
    g=patient_health_detail.objects.get(id=i)
    

    pid=j
    p1=patient_detail.objects.get(id=pid)
    paid=s.paid
    fees=s.fees
    d=patient_health_detail.objects.filter(patient_id=pid)
    Total_FEES=0
    Total_PAID=0
    for g in d:
     Total_FEES=Total_FEES+g.fees
     Total_PAID=Total_PAID+g.paid
    
    try:
     t=Account.objects.get(patient_id=pid)
     if t != None:
      Account.objects.filter(patient_id = pid).update(tfees=Total_FEES,tpaid=Total_PAID)
      t=Account.objects.get(patient_id=pid)
    except:
     
     Account(patient_id=p1,tfees=Total_FEES,tpaid=Total_PAID).save()
     t=Account.objects.get(patient_id=pid)

    if fees == paid:
        calclulation(Total_FEES,Total_PAID,pid)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        pleft=0
        dleft=0
        patient_health_detail.objects.filter(id=i).update(left_from_patient=pleft,left_from_doc=dleft)
        return 0

    elif paid < fees:
        calclulation(Total_FEES,Total_PAID,pid)
        pleft=fees-paid
        patient_health_detail.objects.filter(id=i).update(left_from_patient=pleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        
        return 0
    elif paid > fees:
        calclulation(Total_FEES,Total_PAID,pid)
        dleft=paid-fees
        patient_health_detail.objects.filter(id=i).update(left_from_doc=dleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        
        return 0


def visit_summary(request):
    patient = patient_detail.objects.all().order_by('-id')
    patient1 = patient_detail.objects.all()
    paginator=Paginator(patient, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    for i in patient1:
        particular_patient = patient_health_detail.objects.filter(patient_id=i.id)
        for j in particular_patient:
            summary1(j.id, i.id)


        get_total_acc_patient = Account.objects.all().order_by('-patient_id')

        patient_summary =[]
    for p,n in zip(patient,get_total_acc_patient):
        patient_summary.append({"p":p,"n":n})
    return render(request,'home/visit_summary.html',{'page_obj':page_obj,'patient_summary':patient_summary})
    

def particular_person_summary(request,i):
    visit=patient_health_detail.objects.filter(patient_id=i).all().order_by('-id')
    patient_info = patient_detail.objects.get(id=i)

    #print("-------------------------------------------------")
    #print(visit.patient_visit)
    #print("-------------------------------------------------")
    s={'patient':visit,'id':i,'patient_info':patient_info}
    return render(request,'home/particular_patient.html',s)
    

    
def summary(request,i,j):
    s=patient_health_detail.objects.get(id=i)
    #j is patient id and  i is visit no
    g=patient_health_detail.objects.get(id=i)

    jsonDec = json.decoder.JSONDecoder()
    prescription = jsonDec.decode(g.prescription)
    note = jsonDec.decode(g.note)
    m_time = jsonDec.decode(g.m_time)
    countt = jsonDec.decode(g.countt)
    schd_time = jsonDec.decode(g.schd_time)

    jsonDec = json.decoder.JSONDecoder()
    medicine_outside = jsonDec.decode(g.medicine_outside)
    note_outside = jsonDec.decode(g.note_outside)
    time_outside = jsonDec.decode(g.time_outside)
    count_outside = jsonDec.decode(g.count_outside)
    schd_outside = jsonDec.decode(g.schd_outside)

    print(prescription)
    print(note)
    print(m_time)
    print(countt)
    print(schd_time)
    
    prescription_details = []
    prescription_details_outside = []

    print(medicine_outside)
    print(note_outside)
    print(time_outside)
    print(count_outside)
    print(schd_outside)

    for p,n,t,c,st in zip(prescription,note,m_time,countt,schd_time):
        prescription_details.append({"p":p,"n":n,"t":t,"c":c,"st":st})
    print('-----------------------this is prescription details--------------')
    print(prescription_details)

    for op,on,ot,oc,ost in zip(medicine_outside,note_outside,time_outside,count_outside,schd_outside):
        prescription_details_outside.append({"op":op,"on":on,"ot":ot,"oc":oc,"ost":ost})

    pid=j
    p1=patient_detail.objects.get(id=pid)
    paid=s.paid
    fees=s.fees
    d=patient_health_detail.objects.filter(patient_id=pid)
    Total_FEES=0
    Total_PAID=0
    for g in d:
     Total_FEES=Total_FEES+g.fees
     Total_PAID=Total_PAID+g.paid
    
    try:
     t=Account.objects.get(patient_id=pid)
     if t != None:
      Account.objects.filter(patient_id = pid).update(tfees=Total_FEES,tpaid=Total_PAID)
      t=Account.objects.get(patient_id=pid)
    except:
     
     Account(patient_id=p1,tfees=Total_FEES,tpaid=Total_PAID).save()
     t=Account.objects.get(patient_id=pid)

    if fees == paid:
        calclulation(Total_FEES,Total_PAID,pid)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        summary={'s':s,'t':t,'gender':p1.gender,'prescription_details':prescription_details,'prescription_details_outside':prescription_details_outside}
        return render(request,'home/summary.html',summary)
    elif paid < fees:
        calclulation(Total_FEES,Total_PAID,pid)
        pleft=fees-paid
        patient_health_detail.objects.filter(id=i).update(left_from_patient=pleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        summary={'s':s,'t':t,'prescription_details':prescription_details,'prescription_details_outside':prescription_details_outside}
        return render(request,'home/summary.html',summary)
    elif paid > fees:
        calclulation(Total_FEES,Total_PAID,pid)
        dleft=paid-fees
        patient_health_detail.objects.filter(id=i).update(left_from_doc=dleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        summary={'s':s,'t':t,'prescription_details':prescription_details,'prescription_details_outside':prescription_details_outside}
        return render(request,'home/summary.html',summary)



def patient_group(request): 
    
    p = patient_detail.objects.all()
    return render(request,'home/patient_group.html',{'patient':p})

def create_group(request): 
    if request.method=="POST":
        mem = request.POST.getlist('mselect')
        mem_sep = []
        for i in mem:
         mem_sep.append(i.split(":"))


        print("-------------------------------------------------")
        print(mem)
        print(mem_sep)
        print(mem_sep[0][0])
        print("-------------------------------------------------")

        gname = request.POST['gname']
        user=Patient_group(gname=gname)
        listIWantToStore = mem_sep
        user.member = json.dumps(listIWantToStore)
        user.save()
        g = Patient_group.objects.all()
        s={'group':g}
        return redirect('/all_group')
        
    else:
         p = patient_detail.objects.all()
         s={'patient':p}
         return render(request,'home/patient_group.html',s)
        
def all_group(request): 
    g = Patient_group.objects.all().order_by('id')
    paginator=Paginator(g, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)    
    
    return render(request,'home/all_group.html',{'group':g,'page_obj':page_obj})


def particular_group(request,i):
    #here i is gid
    g=Patient_group.objects.get(id=i)
    jsonDec = json.decoder.JSONDecoder()
    gList = jsonDec.decode(g.member)
    mem_sep = []
    mem_sep1 = []
    
    for i in gList:
        #print("this is i")
        #print(i[0])#pid is patient id
        pid = i[0]
        advance_summ=patient_health_detail.objects.filter(patient_id=pid)
        for j in advance_summ:
            #print("this is j")
            #print(j.id)
            summary1(j.id, pid )#j.id is visit no
    
    for j in gList:
        mem_sep.append({"id":j[0],"name":j[1]})
        
    print("-------------------------------------------------")
    #print(mem_sep)
    print(mem_sep[0]["id"])
    print("-------------------------------------------------")
    Total_Group_paid=0
    Total_Group_fees=0
    Total_Group_from_patient=0
    Total_Group_from_doc=0
    
    dleft_account = []
    pleft_account = []
    #print("-------------------------------------------------")
    for i in gList:
        #print(i[0])#pid is patient id
        pid = i[0]
        #print(pid)
        #print("-------------------------------------------------")
        
        #print(i[0])#pid is patient id
        pid = i[0]
        #print(pid)
    #print("-------------------------------------------------")
        o = Account.objects.get(patient_id=pid)
        o1 = patient_detail.objects.get(id=pid)
        print(o.tfees)
        print(o1)
   
        Total_Group_paid=Total_Group_paid+o.tpaid
        Total_Group_fees=Total_Group_fees+o.tfees
        Total_Group_from_patient=Total_Group_from_patient+o.tleft_from_patient
        Total_Group_from_doc=Total_Group_from_doc+o.tleft_from_doc

        if o.tleft_from_patient != 0:
            pleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':o.tleft_from_patient})
            mem_sep1.append({"id":i[0],"name":i[1],"pleft":o.tleft_from_patient,"dleft":0})
        else:
            #pleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':0})

            if o.tleft_from_doc != 0:
                dleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':o.tleft_from_doc}) 
                mem_sep1.append({"id":i[0],"name":i[1],"pleft":0,"dleft":o.tleft_from_doc})
            else:
                dleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':0}) 
                mem_sep1.append({"id":i[0],"name":i[1],"pleft":0,"dleft":o.tleft_from_doc})
    
    print("-------------------------------------------------")
        
    p = patient_detail.objects.all()
    s={'list':mem_sep,'list1':mem_sep1,'patient':p,'tpaid':Total_Group_fees,'tfees':Total_Group_paid,'tfrom_patient':Total_Group_from_patient,'tfrom_doc':Total_Group_from_doc,'list_pleft':pleft_account,'list_dleft':dleft_account}
    return render(request,'home/particular_group.html',s)
        
        #    return render(request,'home/pageadddata.html')



def statistic(request):
   
    try:
        patient = patient_detail.objects.all()
        total_patient=0
        current_month_patient=0
        current_month_revenue=0
        today_patient=0
        today_revenue=0
        daily_patient_list =[]
        daily_revenue_list =[]
        date_list=[]
        temp=[]

        
        #-------------calulate total patient----------------
        for i in patient:
            total_patient=total_patient+1
        #---------------------calculate current month patient revenue---------
        total_patient_month=0
        date = datetime.date.today()
        last_date=date.day
        end_date = datetime.date.today()    
        start_date = end_date - datetime.timedelta(last_date)       
        monthly_id=patient_health_detail.objects.filter(date__range=[start_date,end_date])

        for i in monthly_id:
        #print(i.id)
        #print(i.fees)
            current_month_patient=current_month_patient+1
            current_month_revenue=current_month_revenue+i.fees
            temp.append(str(i.date.day))
        
        for i in temp:
            if i not in date_list:
                date_list.append(i)

    #--------------------current_month_new_patient -------------------------
        current_month_new_patient=0  
        current_month_new_patient_list=[]
        monthly_id=patient_health_detail.objects.filter(date__range=[start_date,end_date]).only('patient_id')

        for i in monthly_id:
            if i.patient_id.id not in current_month_new_patient_list:
                current_month_new_patient_list.append(i.patient_id.id)
                current_month_new_patient=current_month_new_patient+1
            else:
                continue
        #print(current_month_new_patient_list)
            

    #--------------------calculate today patient and revenue--------------------------
        today_patient_object=patient_health_detail.objects.filter(date=date)
        for i in today_patient_object:
            today_patient=today_patient+1
            today_revenue=today_revenue+i.fees
        
    #-------------------------------------------calculate daily revenue and patient-----------------------------
        date_temp=0
        for i in monthly_id:
            daily_patient=0
            daily_revenue=0
            
            if date_temp == i.date: # to ignore same date as there are many enrty on one day
                continue
            else:
                date_temp=i.date
                particular_date_object=patient_health_detail.objects.filter(date=i.date)

                for j in particular_date_object:
                    daily_patient=daily_patient+1
                    daily_revenue=daily_revenue+j.fees

                daily_patient_list.append({"date":i.date.day,"patient":daily_patient})
                daily_revenue_list.append({"date":i.date.day,"revenue":daily_revenue})
                
                daily_patient_list1=[]
                daily_revenue_list1=[]
                k=0
                j=0
                for i in range(1, 32, 1):
                    
                    if daily_patient_list[k]["date"] == i:
                        a=daily_patient_list[k]["patient"]
                        daily_patient_list1.append(a)
                        k=k+1
                        if k>=len(daily_patient_list):
                            break
                    else:
                        daily_patient_list1.append(0)
                
                k=0
                j=0
                for i in range(1, 32, 1):
                    if j>=len(daily_revenue_list):
                        break
                    if daily_revenue_list[j]["date"] == i:
                        b=daily_revenue_list[j]["revenue"]
                        daily_revenue_list1.append(b)
                        j=j+1
                        
                    else:
                        daily_revenue_list1.append(0)
                        


                    # print('--this is daily patient---')
                    # print(daily_patient_list1)
                    # print(daily_revenue_list1)
                    # print('--this is daily patient abc---')
                    # print(daily_patient_list)
                    # print(daily_revenue_list)

                daily_patient_list_data = {'daily_patient_list':daily_patient_list1}      
                daily_revenue_list_data =  {'daily_revenue_list':daily_revenue_list1}    
                daily_patient_listJSON = dumps(daily_patient_list_data)
                daily_revenue_listJSON = dumps(daily_revenue_list_data)

    #-----------------------------------------------calculate monthly revenue and patient-------------------------------
        monthly_revenue_list=patient_health_detail.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_revenue=Sum('fees')).order_by('month').annotate(extract_month=ExtractMonth('month')).annotate(extract_year=ExtractYear('month'))
        monthly_patient_list=patient_health_detail.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_patient=Count('id')).order_by('month').annotate(extract_month=ExtractMonth('month')).annotate(extract_year=ExtractYear('month'))
        # print("---------------this is j------------------")
        # for j in monthly_revenue_list:
        #      print(j)
        # print("---------------this is j------------------")
        # for j in monthly_patient_list:
        #     print(j["extract_year"])

        monthly_patient_list2=[]
        monthly_revenue_list2=[]

        date1=datetime.date.today()
        year1=date1.year
        

        for j in monthly_patient_list:
            if j["extract_year"] == year1:
                monthly_patient_list2.append({'month':j["extract_month"],'patient':j["total_patient"],'year':j["extract_year"]})
        j=0
        for j in monthly_revenue_list:
            if j["extract_year"] == year1:
                monthly_revenue_list2.append({'month':j["extract_month"],'revenue':j["total_revenue"],'year':j["extract_year"]})

        # print("---------------this is lentgh------------------")
        # print(len(monthly_revenue_list2))
        # print("---------------this is ------------------")
        # print(monthly_patient_list2)
        # print(monthly_revenue_list2)

        monthly_patient_list1=[]
        monthly_revenue_list1=[]

        k=0
       
        for i in range(1, 13, 1):
            if k>=len(monthly_patient_list2):
                
                break 
            if monthly_patient_list2[k]["month"] == i:
                a=monthly_patient_list2[k]["patient"]
                monthly_patient_list1.append(a)
                k=k+1
            else:
                monthly_patient_list1.append(0)
           

        # print("---------------this is list1 ------------------")
        # print(monthly_patient_list1)
        k=0
        for i in range(1, 13, 1):
            if k>=len(monthly_revenue_list2):
                    break        
            if monthly_revenue_list2[k]["month"] == i:
                a=monthly_revenue_list2[k]["revenue"]
                monthly_revenue_list1.append(a)
                k=k+1
            else:
                monthly_revenue_list1.append(0)

        monthly_patient_list_data = {'monthly_patient_list':monthly_patient_list1}      
        monthly_revenue_list_data =  {'monthly_revenue_list':monthly_revenue_list1}    
        monthly_patient_listJSON = dumps(monthly_patient_list_data)
        monthly_revenue_listJSON = dumps(monthly_revenue_list_data)



        #-------------------------------calculate yearly data---------------------------------------
        date2=datetime.date.today()
        year2=date.year

        yearly_revenue_list=patient_health_detail.objects.annotate(year=TruncYear('date')).values('year').annotate(total_revenue=Sum('fees')).order_by('year').annotate(extract_month=ExtractMonth('year')).annotate(extract_year=ExtractYear('year'))
        yearly_patient_list=patient_health_detail.objects.annotate(year=TruncYear('date')).values('year').annotate(total_patient=Count('id')).order_by('year').annotate(extract_month=ExtractMonth('year')).annotate(extract_year=ExtractYear('year'))

        # print("---------------this is yearly_revenue_list------------------")
        # for j in yearly_revenue_list:
        #      print(j)
        # print("---------------this is yearly_patient_lis------------------")
        # for j in yearly_patient_list:
        #     print(j)

        yearly_patient_list2=[]
        yearly_revenue_list2=[]


        for j in yearly_patient_list:
           
            yearly_patient_list2.append({'patient':j["total_patient"],'year':j["extract_year"]})
        j=0
        for j in yearly_revenue_list:
            
            yearly_revenue_list2.append({'revenue':j["total_revenue"],'year':j["extract_year"]})

        # print("---------------this is lentgh------------------")
        # print(len(yearly_revenue_list2))
        # print("---------------this is yearly_patient_list yearly_revenue_list------------------")
        # print(yearly_patient_list2)
        # print(yearly_revenue_list2)

        yearly_patient_list1=[]
        yearly_revenue_list1=[]

        k=0

        for i in range(2, 10, 1):
            #print(i)
            if k>=len(yearly_patient_list2):
                
                break 
            if yearly_patient_list2[k]["year"] == (2020+i):
              
                a=yearly_patient_list2[k]["patient"]
                yearly_patient_list1.append(a)
                k=k+1
            else:
                yearly_patient_list1.append(0)
           

        #print("---------------this is list year ------------------")
        #print(yearly_patient_list1)
        k=0
        for i in range(2,10, 1):
            if k>=len(yearly_revenue_list2):
                    break        
            if yearly_revenue_list2[k]["year"] == (2020+i):
                a=yearly_revenue_list2[k]["revenue"]
                yearly_revenue_list1.append(a)
                k=k+1
            else:
                yearly_revenue_list1.append(0)

        # print("---------------this is list year 12------------------")
        # print(yearly_revenue_list1)

        yearly_patient_list_data = {'yearly_patient_list':yearly_patient_list1}      
        yearly_revenue_list_data =  {'yearly_revenue_list':yearly_revenue_list1}    
        yearly_patient_listJSON = dumps(yearly_patient_list_data)
        yearly_revenue_listJSON = dumps(yearly_revenue_list_data)

        
    
        # print("---------------------------------")
        # print(current_month_patient)
        # print(current_month_revenue)
        # print(total_patient)  
        # print(today_patient)  
        # print(today_revenue)
        # print("-------------daily patient og--------------------")
        # print(daily_patient_list)#done
        # print(daily_revenue_list)#done
        # print("-------------daily patient--------------------")
        # print(daily_patient_list1)#done
        # print(daily_revenue_list1)#done
        # print("---------------------------------")
        # print('--this is monthly patient---')
        # print(monthly_patient_list1)
        # print(monthly_revenue_list1)
        # print('--this is monthly patient og---')
        # print(monthly_patient_list)
        # print(monthly_revenue_list)
        # print('--this is yearly patient---')
        # print(yearly_patient_list1)
        # print(yearly_revenue_list1)
        # print(end_date) 
        # print(start_date) 
        # print(date_list)


        
        data_for_statistics={'yearly_patient_list':yearly_patient_listJSON ,'yearly_revenue_list':yearly_revenue_listJSON ,'daily_patient_list': daily_patient_listJSON,'daily_revenue_list':daily_revenue_listJSON,'monthly_patient_list':monthly_patient_listJSON,'monthly_revenue_list':monthly_revenue_listJSON,'today_patient':today_patient,'today_revenue':today_revenue,'total_patient':total_patient,'current_month_new_patient':current_month_new_patient}
        return render(request,'home/index.html', data_for_statistics)

    except:
        today_patient=0
        today_revenue=0
        total_patient=0
        daily_patient_list1=[]
        daily_revenue_list1=[]
        monthly_patient_list1=[]
        monthly_revenue_list1=[]
        daily_patient_list_data = {'daily_patient_list':daily_patient_list1}      
        daily_revenue_list_data =  {'daily_revenue_list':daily_revenue_list1}    
        daily_patient_listJSON = dumps(daily_patient_list_data)
        daily_revenue_listJSON = dumps(daily_revenue_list_data)

        monthly_patient_list_data = {'monthly_patient_list':monthly_patient_list1}      
        monthly_revenue_list_data =  {'monthly_revenue_list':monthly_revenue_list1}    
        monthly_patient_listJSON = dumps(monthly_patient_list_data)
        monthly_revenue_listJSON = dumps(monthly_revenue_list_data)


        data_for_statistics={'daily_patient_list': daily_patient_listJSON,'daily_revenue_list':daily_revenue_listJSON,'monthly_patient_list':monthly_patient_listJSON,'monthly_revenue_list':monthly_revenue_listJSON,'today_patient':today_patient,'today_revenue':today_revenue,'total_patient':total_patient}
        return render(request,'home/index.html', data_for_statistics)
def settle_account(request,pid):
    #pid is pid
    o=patient_detail.objects.get(id=pid)
    advance_summ=patient_health_detail.objects.filter(patient_id=pid)

    for j in advance_summ:
          
            summary1(j.id,pid)

    if request.method=="POST":
        new_pamount = request.POST['new_pamount']
        new_damount = request.POST['new_damount']

        new_pamount1=int(new_pamount)
        new_damount1=int(new_damount)

        if new_damount1 and new_pamount1 > 0:
            return render(request,'home/page-500.html')

        if new_damount1 != 0:
            patient_all_visit_acc=patient_health_detail.objects.filter(patient_id=pid)

            for i in patient_all_visit_acc:
                if i.fees == i.paid:
                    pass

                elif i.left_from_doc != 0:

                    a =i.paid-i.fees
                    print('this is a')
                    print(a)

                    if new_damount1 >= a:
                        print('>=')
                        new_damount1=new_damount1-a
                        i.paid=i.paid-a
                        b=patient_health_detail.objects.get(id=i.id)
                        b.paid=i.paid
                        b.save()

                    elif new_damount1==0:
                        print('=')
                        pass

                    elif new_damount1 < a:
                       print('<=')
                       c = a-new_damount1
                       print('this is c')
                       print(c)
                       

                       #new_damount1=new_damount1-c
                       i.paid=i.paid-new_damount1
                       b=patient_health_detail.objects.get(id=i.id)
                       b.paid=i.paid
                       b.save()
                       new_damount1=0

        else:
           
            patient_all_visit_acc=patient_health_detail.objects.filter(patient_id=pid)

            for i in patient_all_visit_acc:
                if i.fees == i.paid:
                    pass

                elif i.left_from_patient != 0:

                    a =i.fees-i.paid
                    print('this is a')
                    print(a)

                    if new_pamount1 >= a:
                        print('>=')
                        new_pamount1=new_pamount1-a
                        i.paid=i.paid+a
                        b=patient_health_detail.objects.get(id=i.id)
                        b.paid=i.paid
                        b.save()
                    elif new_pamount1==0:
                        print('=')
                        pass
                    elif new_pamount1 < a:
                       print('<=')
                       c = a-new_pamount1
                       print('this is c')
                       print(c)
                       #new_pamount1=new_pamount1-c
                       i.paid=i.paid+new_pamount1
                       b=patient_health_detail.objects.get(id=i.id)
                       b.paid=i.paid
                       b.save()
                       new_pamount1=0


        advance_summ=patient_health_detail.objects.filter(patient_id=pid)
        for j in advance_summ:
          
            summary1(j.id,pid)
                 
             
        patient_account = Account.objects.get(patient_id=pid)

        return render(request,'home/particular_patient_settle_account.html',{'patient_account':patient_account,'patient':o})
    else:
        patient_account = Account.objects.get(patient_id=pid)
        
        return render(request,'home/particular_patient_settle_account.html',{'patient_account':patient_account,'patient':o})
        
def ref_doctor(request):

    if request.method == 'POST':
        doc_list = []
        query = request.POST['search1']
        name = RefDoc.objects.all().filter((Q(name__icontains = query)))
        print(name)
        for i in name:
            doc_list.append({'name':i.name,'details':i.details})
            print(i.id)
            print(i.details)
        return render(request,'home/ref_doc.html',{'doc_list':doc_list})
    else:
         return render(request,'home/ref_doc.html')


def search_patient(request):
    if request.method=='POST':
            query=request.POST['search']
            lookups=Q(fname__icontains=query)|Q(lname__icontains=query)|Q(contact__icontains=query)
            results=patient_detail.objects.filter(lookups).distinct()
            print(results)
            if len(results)== 0:
                    return render(request,"home/patients.html",{'error':'NOT FOUND'})
            context={'page_obj':results}
            template_name='home/patients.html'
            return render(request,template_name,context)

        # else:
        #     return redirect('main_patient')
    else:
        return render(request, 'home/patients.html')


def search_patient_summary(request):
    if request.method=='POST':
            query=request.POST['search']
            lookups=Q(fname__icontains=query)|Q(lname__icontains=query)|Q(contact__icontains=query) #__iexact can be also used
            results=patient_detail.objects.filter(lookups).distinct()
            print(results)
            if len(results)== 0:
                    return render(request,"home/visit_summary.html",{'error':'NOT FOUND'})
            context={'page_obj':results}
            template_name='home/visit_summary.html'
            return render(request,template_name,context)
    
    else:
        return render(request, 'home/visit_summary.html')

def search_patient_Group(request):

    if request.method=='POST':
            query=request.POST['search']
            lookups=Q(gname__icontains=query)
            results=Patient_group.objects.filter(lookups).distinct()
            print(results)
            if len(results)== 0:
                    return render(request,"home/all_group.html",{'error':'NOT FOUND'})
            context={'page_obj':results}
            template_name='home/all_group.html'
            return render(request,template_name,context)
    
    else:
        return render(request, 'home/all_group.html')

def search_patient_Today(request):

    if request.method=='POST':
            date = datetime.date.today()
           
            query=request.POST['search']
            lookups=Q(fname__icontains=query)|Q(lname__icontains=query)
            results=patient_health_detail.objects.filter(lookups).distinct().filter(date=date)
            print(results)
            if len(results)== 0:
                    return render(request,"home/all_group.html",{'error':'NOT FOUND'})
            context={'page_obj':results}
            template_name='home/today_patient.html'
            return render(request,template_name,context)
    
    else:
        return render(request, 'home/today_patient.html')



    
def delete_patient(request,i):
    patient=patient_detail.objects.get(id=i)
    print('================================')
    print('deleting')
    print(patient)
    patient.delete()
    print('===================================')
    return redirect('main_patient')

def delete_group(request,i):
    grp=Patient_group.objects.get(id=i)
    print(grp)
    grp.delete()
    return redirect('all_group')
def today_patient(request):
    date = datetime.date.today()
    today_patient_object=patient_health_detail.objects.filter(date=date)
    for i in today_patient_object:
        print(i.patient_id.id)
    context={'page_obj':today_patient_object}
    template_name='home/today_patient.html'
    return render(request,template_name,context)







master-1
#master




