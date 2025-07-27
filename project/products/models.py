from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # language = models.CharField(max_length=50, default='en') 

