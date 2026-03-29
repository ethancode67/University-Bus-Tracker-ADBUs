# tracker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.index, name='index'),
    path('tracker/', views.tracker, name='tracker'),

    # Bus API
    path('api/bus/<int:bus_id>/', views.bus_route, name='bus_route'),
    path('api/bus/<int:bus_id>/update/', views.update_location, name='update_location'),

    # Auth API
    path('api/auth/register/', views.register, name='register'),
    path('api/auth/login/', views.login_view, name='login'),
    path('api/auth/logout/', views.logout_view, name='logout'),
    path('api/auth/check/', views.check_auth, name='check_auth'),
]