from django.urls import path
from .views import GetNumbers

urlpatterns = [
    path('area-code/', GetNumbers.as_view(), name='get_numbers'),
]
