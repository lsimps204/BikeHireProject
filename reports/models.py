from django.db import models

from bikes.models import Location

# Create your models here.
class LocationBikeCount(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    count = models.IntegerField()
    datetime = models.DateTimeField()

    class Meta:
        ordering = ('datetime',)