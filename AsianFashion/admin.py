from django.contrib import admin
from .models import Item, Order, Choice, Customer, Customer_Cart

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class ChoiceAdmin(admin.ModelAdmin):
    search_fields = ["choice_text"]
    list_display=['choice_text','item']

class ItemAdmin(admin.ModelAdmin):
    search_fields = ["tag"]
    inlines = [ChoiceInline]
    list_display=["category","tag","title","price"]

class OrderAdmin(admin.ModelAdmin):
    search_fields = ["email"]
    list_display=["item", "first_name", "last_name", "order_date", "status"]

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ["email"]
    list_display=['email']

class CustomerCartAdmin(admin.ModelAdmin):
    search_fields=['customer']
    list_display=['customer','item']

admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Customer_Cart, CustomerCartAdmin)