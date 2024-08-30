import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

class Customer(models.Model):
    uuid = models.CharField(max_length=200, null=False, default=None)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100, null=True)

class Item(models.Model):
    # Category: women_bag, men_bag, women_phonecase
    category = models.CharField(max_length=20) 
    # Primary key - unique ID
    tag = models.CharField(max_length=20)
    # Short display title on main page.
    title = models.CharField(max_length=50)
    # Detail and concise description on item detail page.
    length = models.FloatField(default=40)
    width = models.FloatField(default=40)
    height = models.FloatField(default=40)
    material = models.CharField(max_length=30,default="PU")
    description = models.CharField(max_length=200) 
    img_url = models.CharField(max_length=100)
    price = models.IntegerField(default=40)
   
class Choice(models.Model):
    choice_text = models.CharField(max_length=20)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None, null=True) 
    def __str__(self) -> str:
        return self.choice_text
  
class Order(models.Model):
    # Purchase session.
    session_id = models.CharField(max_length=100)
    # Order summary.
    order_summary = models.CharField(max_length=1000, default=None, null=True)
    # Purchased item information.
    item = models.ForeignKey(Item, on_delete=models.CASCADE) # Used to identify items
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, default = None, null=True)
    amount = models.IntegerField(default=40)
    quantity = models.IntegerField(default=1)
    # Customer information, null if directly buy without signing in.
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None, null=True)
    # Delivery address.
    street_address_line_1 = models.CharField(max_length=100, null=True)
    street_address_line_2 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    # Contact information.
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    # Ordered date.
    order_date = models.DateTimeField("date ordered", default=timezone.now)
    # Cart object indicator
    is_cart_object = models.BooleanField(default=False)
    # Order status
    status = models.CharField(max_length=20, default="pending review") 

class Customer_Cart(models.Model):
    # identify a customer
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # identify an item
    item = models.ForeignKey(Item, on_delete=models.CASCADE) 
    # Optional: identify the choice of an item
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, default=None, null=True)