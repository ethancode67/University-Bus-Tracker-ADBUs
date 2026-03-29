from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Bus, BusLocation
import json


# ─── Bus API ───────────────────────────────────────────────────────────────────

def index(request):
    return render(request, 'index.html')

def tracker(request):
    return render(request, 'tracker.html')

def bus_route(request, bus_id=1):
    try:
        bus = Bus.objects.prefetch_related('stops').get(pk=bus_id)
        loc = bus.location
    except Bus.DoesNotExist:
        return JsonResponse({"error": "Bus not found"}, status=404)

    stops = [
        {"name": s.name, "lat": s.lat, "lng": s.lng, "eta": s.eta, "order": s.order}
        for s in bus.stops.all()
    ]

    return JsonResponse({
        "bus": {"id": bus.id, "name": bus.name, "description": bus.description},
        "stops": stops,
        "location": {
            "lat": loc.lat,
            "lng": loc.lng,
            "segment_index": loc.segment_index,
            "segment_t": loc.segment_t,
            "updated_at": loc.updated_at.isoformat(),
        }
    })


@csrf_exempt
@require_POST
def update_location(request, bus_id=1):
    try:
        data = json.loads(request.body)
        loc = BusLocation.objects.get(bus_id=bus_id)
        loc.lat = data["lat"]
        loc.lng = data["lng"]
        loc.segment_index = data["segment_index"]
        loc.segment_t = data["segment_t"]
        loc.save()
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ─── Auth API ──────────────────────────────────────────────────────────────────

@csrf_exempt
@require_POST
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        email    = data.get("email", "").strip()
        password = data.get("password", "")

        if not username or not email or not password:
            return JsonResponse({"error": "All fields required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        if len(password) < 8:
            return JsonResponse({"error": "Password must be at least 8 characters"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({"status": "ok", "username": user.username})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_POST
def login_view(request):
    try:
        data     = json.loads(request.body)
        email    = data.get("email", "").strip()
        password = data.get("password", "")

        # Django's authenticate uses username, so look up by email first
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid email or password"}, status=401)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({"error": "Invalid email or password"}, status=401)

        login(request, user)
        return JsonResponse({"status": "ok", "username": user.username})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"status": "ok"})


def check_auth(request):
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True, "username": request.user.username})
    return JsonResponse({"authenticated": False}, status=401)