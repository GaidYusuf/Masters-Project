from django.db import models


class EventDetail(models.Model):
    event = models.ForeignKey('IslamicEvent', on_delete=models.CASCADE)
    description = models.TextField(null=True)
    picture = models.ImageField(
        upload_to='event_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.event.name} - Details"


class IslamicEvent(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    hijri_date = models.CharField(max_length=100)

    def __str__(self):
        return self.name
