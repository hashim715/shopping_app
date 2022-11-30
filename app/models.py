from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import (
    post_save
)
import random
# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    description=models.TextField(max_length=1000)
    price=models.IntegerField()
    discount_price=models.IntegerField(null=True,blank=True)
    image=models.ImageField(null=True,blank=True,upload_to="images/product")
    slug=models.SlugField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.title


def slugify_business_title(instance):
    slug=f"{slugify(instance.title)}-business"
    qs=Product.objects.filter(slug=slug)
    if qs.exists():
        rand_int=random.randint(300_000,500_000)
        slug=f"{slug}-{rand_int}"
        checking_again=Product.objects.filter(slug=slug)
        if checking_again.exists():
            slugify_business_title(instance)
        else:
            return slug
    else:
        return slug

@receiver(post_save,sender=Product)
def business_post_save(sender,instance,created,*args,**kwargs):
    print("instance saved")
    if not instance.slug:
        slug_value=slugify_business_title(instance)
        instance.slug=slug_value
        instance.save()
        print("slug field saved")

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,unique=True)
    address=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    zip_code=models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    card_number=models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return self.user.username


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product,blank=True)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username