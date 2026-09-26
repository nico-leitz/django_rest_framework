from django.urls import path
from .views import MarketsView, MarketsSingleView, seller_view, single_seller_view


urlpatterns = [
  path('market/', MarketsView.as_view()),# class based views müssen immer mit 'as_view()' deklariert werden
  path('market/<int:pk>/',  MarketsSingleView.as_view(), name='market-detail'),
  path('seller/', seller_view),
  path('seller/<int:pk>', single_seller_view, name='seller_single')
]
