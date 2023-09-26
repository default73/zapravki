from django.contrib import admin
from .models import Profile, GasStation, FuelType, Column, BankCard, Payment
# Register your models here.

admin.site.register(Profile)
admin.site.register(BankCard)
admin.site.register(GasStation)
admin.site.register(FuelType)
admin.site.register(Column)
admin.site.register(Payment)