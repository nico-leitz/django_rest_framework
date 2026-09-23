from django.urls import path
from .views import first_view, markets_single_view

urlpatterns = [
  path('', first_view),
  path('<int:pk>/',  markets_single_view)
]
