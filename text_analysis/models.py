from django.db import models

class ServiceManager(models.Model):
   name = models.CharField(max_length=20)
   url = models.URLField()
   
   def __str__(self):
       return self.name

class DeleteService(models.Model):
   name = models.CharField(max_length=20)
   
   def __str__(self):
       return self.name

class TextAnalysisService(models.Model):
   service = models.CharField(max_length=20)
   text = models.TextField()
   
   def __str__(self):
       return self.service
