from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User



# Create your models here.
class Relation(models.Model):
    
    rel=models.CharField(max_length=250)
    def __str__(self):
        return self.rel


class ContactBook(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    full_name = models.CharField(max_length=250)
    relationship = models.ForeignKey(Relation,on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=1000)
    is_favorite = models.BooleanField(default=False) 


    

    def __str__(self):
          return self.full_name
    
class Group(models.Model):
    #user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(ContactBook, related_name="groups")

    

    def __str__(self):
        return self.name
