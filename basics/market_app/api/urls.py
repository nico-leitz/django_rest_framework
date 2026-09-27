from django.urls import path, include
from rest_framework import routers
from .views import MarketViewSet, SellerViewSet, ProductViewSet, SellerOfMarketList

# 1. Wir erschaffen den "Roboter", der uns die lästige Tipparbeit für URLs abnimmt.
router = routers.DefaultRouter()

# 2. Wir füttern den Roboter. Wir sagen ihm: "Hier ist mein ViewSet, bau mir bitte alle CRUD-URLs dafür."
#
# Erklärung der 3 Parameter in der Klammer:
# Parameter 1 (r'markets')   -> Das ist die ECHTE URL! Das tippst du in Postman ein (z.B. localhost:8000/markets/)
# Parameter 2 (MarketViewSet)-> Das ist deine Logik aus der views.py, die ausgeführt werden soll.
# Parameter 3 (basename)     -> Das ist nur ein INTERNER SPITZNAME für Django (Erklärung siehe unten).
router.register(r'markets', MarketViewSet, basename='market') 

# Gleiches Spiel für die Verkäufer. Postman-URL: /sellers/ | Interner Spitzname: 'seller'
router.register(r'sellers', SellerViewSet, basename='seller') 

# Gleiches Spiel für die Produkte. Postman-URL: /products/ | Interner Spitzname: 'product'
router.register(r'products', ProductViewSet, basename='product') 


urlpatterns = [
    # 3. Der Roboter hat jetzt im Hintergrund ca. 15 URLs generiert. 
    # Mit 'include(router.urls)' schütten wir all diese fertigen URLs auf einen Schlag in Djangos System.
    # Das leere '' ganz vorne bedeutet: Häng kein extra Wort mehr davor. 
    path('', include(router.urls)),
    
    # 4. Unsere Sonder-Route. Der Roboter baut nur Standard-CRUD (Listen & Einzelansicht). 
    # Da dies eine verschachtelte Spezial-URL ist, müssen wir sie weiterhin per Hand (wie früher) eintragen.
    path('markets/<int:pk>/sellers/', SellerOfMarketList.as_view(), name='market-sellers'),
]

# =====================================================================
# --- LERN-ARCHIV: ALTE VERSIONEN (MANUELLES ROUTING) ---
# =====================================================================
# urlpatterns = [
#   path("", include(router.urls)),
#   path('market/', MarketsView.as_view()), # Manuelle Liste
#   path('market/<int:pk>/', MarketSingleView.as_view(), name='market-detail'), # Manuelle Einzelansicht
#   path('seller/', seller_view), # Alte FBV
#   path('seller/<int:pk>', single_seller_view, name='seller_single') # Alte FBV
# ]