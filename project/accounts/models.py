from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    phone = models.CharField(max_length=15,null=True,blank=True)
    otp = models.CharField(max_length=6,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True,blank=True)

    def is_valid(self):
        return self.is_verified and (self.expired_at is None or self.expired_at > timezone.now())
    class Meta():
        db_table='accounts'

class Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    project_name = models.CharField(max_length=200,null=True , blank=True ,unique=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    technologies = models.TextField(max_length=300,null=True)

    class Meta():
        db_table = 'projects'

class ProjectImage(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='images/%y%m%d')
