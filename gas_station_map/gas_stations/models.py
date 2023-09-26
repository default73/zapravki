from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class BankCard(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField(verbose_name='Expiration Date', help_text='Enter the expiration date in MM/YY format')
    cvv = models.CharField(max_length=3)


class GasStation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class FuelType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Column(models.Model):
    number = models.CharField(max_length=50)
    id_GasStation = models.ForeignKey(GasStation, on_delete=models.CASCADE)
    fuel = models.ForeignKey(FuelType, on_delete=models.CASCADE)




class BankCard(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=100)
    expiration_date = models.DateField()
    cvv_code = models.CharField(max_length=3)

class Payment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    gas_station = models.ForeignKey(GasStation, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)