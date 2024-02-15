from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
import json

class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role)

    def __str__(self) :
        return self.user.username

class Inventory(models.Model):
    product_Id=models.CharField(blank=True,max_length=10,unique=True)
    product_Name=models.CharField(blank=True,max_length=50)
    vendor=models.CharField(blank=True,max_length=10)
    mrp=models.FloatField()
    batch_num=models.CharField(blank=True,max_length=10)
    batch_date=models.DateField()
    quantity=models.IntegerField()
    status=models.CharField(blank=True,max_length=10, choices=(('approved', 'Approved'),('pending','Pending')))

    class Meta:
        db_table='records'
    
    def __str__(self):
        return self.product_Name

class RequestRecord(models.Model):
    requested_user=models.ForeignKey(User, on_delete=models.CASCADE)
    payload=models.CharField(max_length=255)
    request_status=models.CharField(blank=True,max_length=10, choices=(('approved', 'Approved'),('pending','Pending'),('reject','Reject')))
    action=models.CharField(blank=True,max_length=10, choices=(('edit', 'Edit'),('delete','Delete'),('add','Add')))

    def save(self,*args,**kwargs):
        if(self.request_status == 'approved'):
            payloadData = json.loads(self.payload)
            if(self.action == 'delete'):
                inventory = Inventory.objects.get(product_Id=payloadData['product_id'])
                inventory.delete()
            if(self.action == 'Adding'):
                product=Inventory(
                    product_Id=payloadData['product_id'],
                    product_Name=payloadData['product_name'],
                    vendor=payloadData['vendor'],
                    mrp=payloadData['mrp'],
                    batch_num=payloadData['batch_number'],
                    batch_date=payloadData['batch_date'],
                    quantity=payloadData['quantity'],
                    status='approved'
                )
                product.save()
            Inventory.objects.filter(product_Id=payloadData['product_id']).update(
                product_Name=payloadData['product_name'],
                vendor=payloadData['vendor'],
                mrp=payloadData['mrp'],
                batch_num=payloadData['batch_number'],
                batch_date=payloadData['batch_date'],
                quantity=payloadData['quantity']
            )
        super().save(*args,**kwargs)

