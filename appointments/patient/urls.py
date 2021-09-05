from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('query_appointment/', views.CreateBookingView.as_view(), name='query_appointment'),
]
