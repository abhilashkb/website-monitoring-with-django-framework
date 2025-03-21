from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_domain, name='add_domain'),
    path('', views.dashboard, name='dashboard'),
    # other URL patterns...
]