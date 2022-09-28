from django.db import models

# Create your models here.

#permission
class Roles(models.Model): 
    name = models.CharField(max_length=200, unique=True)
    class Meta:
        db_table = 'Roles'

class Modules(models.Model):
    name = models.CharField(max_length=200, unique=True)
    class Meta:
        db_table = 'Modules'

class Access_modules(models.Model):
    roles_id = models.IntegerField()
    modules_name = models.CharField(max_length=200)
    actions = models.CharField(max_length=200)  
    class Meta:
        db_table = 'Access_modules'        
#permission
