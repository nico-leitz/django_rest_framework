from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializiers import MarketSerializer, SellerSerializer
from market_app.models import Market, Seller

@api_view(['GET', 'POST']) 
def first_view(request):
    
    if request.method == 'GET':
        markets = Market.objects.all() 
        serializer = MarketSerializer(markets, many=True) 
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MarketSerializer(data=request.data, many=True)
        
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


@api_view(['GET', 'POST'])
def seller_view(request):
    
    if request.method == 'GET':
        sellers = Seller.objects.all() 
        serializer = SellerSerializer(sellers, many=True) 
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def single_seller_view(request, pk):
    
    try:
        seller = Seller.objects.get(pk=pk)
        
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=404)

    if request.method == 'GET':
        serializer = SellerSerializer(seller, many=False) 
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        seller.delete()
        return Response(status=204)
            