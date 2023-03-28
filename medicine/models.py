from django.db import models

# Create your models here.
class Medicine(models.Model):
    medicine_name=models.CharField(max_length=30)
    medicine_type=models.CharField(max_length=30)
   

    def __str__(self):
        return self.medicine_name +''+ self.medicine_type