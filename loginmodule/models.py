from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
# Create your models here.

class patient_detail(models.Model):
    patient_id=models.AutoField
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    note = models.TextField(max_length=40,null=True)
    age = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    contact = models.IntegerField(null=True)
    address  = models.CharField(max_length=50,null=True)
    rperson = models.CharField(max_length=20,null=True)
    gender = models.CharField(max_length=20,null=True)
    
    def __str__(self):
         return self.fname +' '+ self.lname

class patient_health_detail(models.Model):
    patient_visit=models.AutoField
    patient_id=models.ForeignKey(patient_detail, on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    symptoms = models.TextField(max_length=30)
    diagnostic = models.TextField(max_length=30)

    prescription= models.TextField(max_length=30)
    note = models.TextField(max_length=30,null=True)
    m_time = models.TextField(max_length=30,null=True)
    schd_time = models.TextField(max_length=30,null=True)
    countt = models.TextField(max_length=20,null=True)

    medicine_outside = models.TextField(max_length=30,default=0)
    schd_outside = models.TextField(max_length=30,null=True)
    time_outside = models.TextField(max_length=30,null=True)
    note_outside = models.TextField(max_length=30,null=True)
    count_outside =  models.TextField(max_length=20,null=True)

    report = models.CharField(max_length=30)
    refdoc = models.CharField(max_length=20,null=True)
    date = models.DateField(default=datetime.now, blank=True)
    time=models.TimeField(default=datetime.now, blank=True)
    fees = models.IntegerField(default=0)
    paid = models.IntegerField(default=0)
    paid_original=models.IntegerField(default=0)
    left_from_patient=models.IntegerField(default=0)
    left_from_doc=models.IntegerField(default=0)
    
    def __str__(self):
         return self.fname +' '+ self.lname

class Account(models.Model):
    patient_id = models.OneToOneField(patient_detail, on_delete=models.CASCADE,primary_key=True)
    tfees = models.IntegerField(default=0)
    tpaid = models.IntegerField(default=0)
    tleft_from_patient=models.IntegerField(default=0)
    tleft_from_doc=models.IntegerField(default=0)

class Patient_group(models.Model):
    gid = models.AutoField
    gname =  models.CharField(max_length=20)
    member = models.TextField(null=True)
    tfees = models.IntegerField(default=0)
    tpaid = models.IntegerField(default=0)
    tleft_from_patient=models.IntegerField(default=0)
    tleft_from_doc=models.IntegerField(default=0)

    def __str__(self):
         return self.gname
