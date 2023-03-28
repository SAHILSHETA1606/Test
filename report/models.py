from django.db import models

# Create your models here.
class Report(models.Model):
    report=models.TextField(max_length=15,default=0)
    def __str__(self):
        return self.report