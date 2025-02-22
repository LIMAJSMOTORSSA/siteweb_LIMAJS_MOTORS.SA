from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('service/', views.service_view, name='service'),
]