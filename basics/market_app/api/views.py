from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializiers import MarketSerializer, SellerDetailSerializer, SellerCreateSerializer
from market_app.models import Market, Seller

@api_view(['GET', 'POST']) # GET ist hier der default
def first_view(request):
    
    if request.method == 'GET':
        # 1. Wir holen uns alle Märkte (als QuerySet/Liste von Objekten) aus der Datenbank.
        markets = Market.objects.all() 
        
        # 2. Wir übergeben die Datenbank-Objekte an den Serializer.
        # many=True ist zwingend nötig, da wir hier mehrere Objekte (QuerySet) übergeben.
        # HIER findet die Umwandlung noch NICHT statt – der Serializer wird nur vorbereitet.
        serializer = MarketSerializer(markets, many=True) 
        
        # 3. Sobald wir "serializer.data" aufrufen, findet die tatsächliche Umwandlung statt 
        # (Datenbank-Objekte -> Python Dictionaries -> JSON).
        # Anstatt eines Json- oder HttpResponse nutzen wir in DRF den mächtigeren 'Response'.
        return Response(serializer.data)
    
    
    if request.method == 'POST':
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

@api_view(['GET', 'DELETE', 'PUT'])
def markets_single_view(request, pk):
    
    if request.method == 'GET':
        market = Market.objects.get(pk=pk) 
        serializer = MarketSerializer(market, many=False) 
        return Response(serializer.data)

    if request.method == 'PUT':
            market = Market.objects.get(pk=pk)
            # 'partial'sagt aus?? ( Das man z.B. nur ein Feld bearbeiten kann?)
            serializer = MarketSerializer(market, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

    if request.method == 'DELETE':
            market = Market.objects.get(pk=pk) 
            serializer = MarketSerializer(market, many=False)
            market.delete()
            return Response(serializer.data)


@api_view(['GET', 'DELETE', 'POST'])
def seller_view(request):
    
    if request.method == 'GET':
        sellers= Seller.objects.all() 
        serializer = SellerDetailSerializer(sellers, many=True) 
        return Response(serializer.data)

    if request.method == 'POST':
            serializer = SellerCreateSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

    
