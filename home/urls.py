from django.urls import path
from . import views

# Defines the URL patterns for the Home application, mapping each URL path
# to its corresponding view function.
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about/', views.about, name='home.about'),
    path('get-started/', views.get_started_redirect, name='get_started'),
]