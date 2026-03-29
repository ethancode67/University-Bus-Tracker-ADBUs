# tracker/tick.py  — run with: python manage.py shell < tracker/tick.py
# Or better: use Celery Beat / APScheduler for production

import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adbus_project.settings')
django.setup()

from tracker.models import BusLocation, Stop, Bus

STEP = 0.2
TICK_SEC = 10

def tick():
    bus = Bus.objects.get(pk=1)
    stops = list(bus.stops.order_by('order'))
    loc = bus.location

    loc.segment_t += STEP

    if loc.segment_t >= 1.0:
        loc.segment_t = 0.0
        loc.segment_index += 1
        if loc.segment_index >= len(stops) - 1:
            loc.segment_index = 0

    i = loc.segment_index
    a, b = stops[i], stops[min(i + 1, len(stops) - 1)]
    t = loc.segment_t
    loc.lat = a.lat + (b.lat - a.lat) * t
    loc.lng = a.lng + (b.lng - a.lng) * t
    loc.save()
    print(f"Bus at segment {loc.segment_index}, t={loc.segment_t:.1f} → ({loc.lat:.5f}, {loc.lng:.5f})")

while True:
    tick()
    time.sleep(TICK_SEC)