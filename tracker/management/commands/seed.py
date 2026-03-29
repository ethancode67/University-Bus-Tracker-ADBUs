from django.core.management.base import BaseCommand
from tracker.models import Bus, Stop, BusLocation

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bus, _ = Bus.objects.get_or_create(
            name="Bus #1 - Azara Locality",
            defaults={"description": "Picking up students. 7 Stops"}
        )

        stops_data = [
            ("Airport Stop",        26.103373, 91.593815, "07:10 AM", 0),
            ("Decathlon Stop",      26.100746, 91.612154, "07:20 AM", 1),
            ("Police Station Stop", 26.116258, 91.614339, "07:30 AM", 2),
            ("Zudio Stop",          26.125571, 91.618271, "07:40 AM", 3),
            ("Dharapur Stop",       26.137317, 91.627107, "07:50 AM", 4),
        ]

        for name, lat, lng, eta, order in stops_data:
            Stop.objects.get_or_create(bus=bus, order=order, defaults={
                "name": name, "lat": lat, "lng": lng, "eta": eta
            })

        BusLocation.objects.get_or_create(bus=bus, defaults={
            "lat": 26.103373, "lng": 91.593815
        })

        self.stdout.write(self.style.SUCCESS("Database seeded!"))