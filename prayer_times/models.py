from django.db import models

class PrayerTime(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    fajr = models.TimeField()
    dhuhr = models.TimeField()
    asr = models.TimeField()
    maghrib = models.TimeField()
    isha = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.date}"
