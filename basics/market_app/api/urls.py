from django.urls import path
from .views import first_view, markets_single_view, seller_view

urlpatterns = [
  path('market/', first_view),
  path('market/<int:pk>/',  markets_single_view),
  path('seller/', seller_view)
]
