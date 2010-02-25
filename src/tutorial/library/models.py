from django.db import models
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField

class Library(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    state = USStateField()
    phone_number = PhoneNumberField()
    zip_code = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.name
        
class Patron(models.Model):
    name = models.CharField(max_length=200)
    library = models.ForeignKey(Library)
    
    def __unicode__(self):
       return self.name
       
class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library)
    
    def __unicode__(self):
        return self.name
        
class Book(models.Model):
    title = models.CharField(max_length=200)
    libraries = models.ManyToManyField(Library)
    
    def __unicode__(self):
        return self.title