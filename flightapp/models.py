from django.db import models

# Create your models here.
class FlightAddModel(models.Model):
    city = models.CharField(max_length=64)
    airport = models.CharField(max_length=64)
    code = models.CharField(max_length=5)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    country = models.CharField(max_length=64)
    depart_time = models.TimeField(auto_now=False, auto_now_add=False)
    duration = models.CharField(max_length=30)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    airline = models.CharField(max_length=64)
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)
    seats=models.IntegerField()



    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
######----------------------------------------------------------------------------
class Passenger(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone = models.IntegerField()
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname
class FlightBook(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    departure_date = models.CharField(max_length=20)
    return_date = models.CharField(max_length=20,null=True, blank=True)
    category = models.CharField(max_length=10)
    way = models.CharField(max_length=10)




class NewPassenger(models.Model):
    flight = models.ForeignKey(FlightAddModel, on_delete=models.CASCADE)
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)

class Order(models.Model):
    passenger=models.ForeignKey(Passenger,on_delete=models.CASCADE)
    flights=models.ManyToManyField(FlightAddModel)
    booking_date=models.DateTimeField(auto_now_add=True)


class orderticket(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    order_status=models.BooleanField(default=True)




