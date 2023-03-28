from django.db import models

# Create your models here.
class Disease(models.Model):
    disease=models.TextField(max_length=15,default=0)
    def __str__(self):
        return self.disease