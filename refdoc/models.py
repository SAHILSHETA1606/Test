from django.db import models

# Create your models here.

class Doc_group(models.Model):
    gid = models.AutoField
    gname =  models.CharField(max_length=20)
    # member = models.TextField(null=True)
    # details=models.TextField(max_length=100,default=0)

class RefDoc(models.Model):
    
    doc_id=models.AutoField
    name=models.TextField(max_length=25,default=0)
    details=models.TextField(max_length=100,default=0)
    gid=models.ForeignKey(Doc_group, on_delete=models.CASCADE)#models.IntegerField(default=0)
    
    def __str__(self):
        return self.name 