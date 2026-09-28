from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from market_app.models import Market, Seller, Product
from .serializiers import MarketSerializer, SellerSerializer, ProductSerializer

# --- 1. INDUSTRIE-STANDARD: MODEL VIEW SETS (ALLES IN EINER KLASSE) ---

# Das hier ersetzt MarketsView, MarketSingleView und alle deine @api_view Funktionen!
class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

# Ersetzt seller_view und single_seller_view. Alle 5 CRUD Aktionen sind automatisch drin.
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

# Ersetzt deine unfertigen ProductViewSets.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# --- 2. SONDERFALL: SPEZIFISCH GEFILTERTE LISTEN (HIER SIND GENERICS PERFEKT) ---

# Diese View wird über eine Sonder-URL aufgerufen (/market/<pk>/sellers/).
# Sie listet nicht alle Verkäufer auf, sondern filtert sie nach dem Markt. 
# Dafür ist eine generische View (ListCreateAPIView) das perfekte Werkzeug!
class SellerOfMarketList(generics.ListCreateAPIView):
    serializer_class = SellerSerializer # Wir nutzen einfach den normalen SellerSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        market = get_object_or_404(Market, pk=pk)
        return market.sellers.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        market = get_object_or_404(Market, pk=pk)
        serializer.save(markets=[market])


# =====================================================================
# --- LERN-ARCHIV: ALTE VERSIONEN (MIXINS & FUNCTION BASED VIEWS) ---
# =====================================================================

# FRAGE: Single views nutzen meist GET, PUT, PATCH, DELETE. Multi views nutzen meist GET, POST.
# ANTWORT: Exakt! Deswegen gibt es bei Generics die ListCreateAPIView (GET-List, POST) 
# und die RetrieveUpdateDestroyAPIView (GET-Single, PUT, PATCH, DELETE). Ein ModelViewSet vereint einfach alle.

# --- STUFE 2: GENERICS (Guter Weg, aber ModelViewSet ist für komplett CRUD noch kürzer) ---
# class MarketsView(generics.ListCreateAPIView):
#     queryset = Market.objects.all()
#     serializer_class = MarketSerializer
#
# class MarketSingleView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Market.objects.all()
#     serializer_class = MarketSerializer

# --- STUFE 1.5: MIXINS (Das maßgeschneiderte Lego-Set. Zuviel Schreibarbeit für normales CRUD) ---
# class MarketSingleView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin ,generics.GenericAPIView):
#     queryset = Market.objects.all()
#     serializer_class = MarketSerializer
#     def get(self, request, *args, **kwargs): return self.retrieve(request, *args, **kwargs)
#     def put(self, request, *args, **kwargs): return self.update(request, *args, **kwargs)
#     def delete(self, request, *args, **kwargs): return self.destroy(request, *args, **kwargs)

# --- STUFE 1: FUNCTION BASED VIEWS (Reine Handarbeit, fehleranfällig. In der Praxis obsolet für DB-Modelle) ---
# @api_view(['GET', 'PUT', 'DELETE'])
# def single_seller_view(request, pk):
#     try:
#         seller = Seller.objects.get(pk=pk)
#     except Seller.DoesNotExist:
#         return Response({"error": "Seller not found"}, status=404)
# ... (restlicher Code wie in deiner Vorlage)

#