from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scrape_and_compare/', views.scrape_and_compare, name='scrape_and_compare'),
]