from django.db import models

# Create your models here.

class Bus(models.Model):
    name = models.CharField(max_length=100)        # e.g. "Bus #1 - Azara Locality"
    description = models.CharField(max_length=200) # e.g. "Picking up students. 5 Stops"

    def __str__(self):
        return self.name


class Stop(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='stops')
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    eta = models.CharField(max_length=20)   # e.g. "07:10 AM"
    order = models.PositiveIntegerField()   # stop sequence number

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.bus.name} → {self.name}"


class BusLocation(models.Model):
    """Stores the real-time position of a bus (updated server-side)."""
    bus = models.OneToOneField(Bus, on_delete=models.CASCADE, related_name='location')
    lat = models.FloatField()
    lng = models.FloatField()
    segment_index = models.IntegerField(default=0)   # which segment the bus is on
    segment_t = models.FloatField(default=0.0)       # 0.0–1.0 progress within segment
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus.name} location"