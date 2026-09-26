from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializiers import MarketSerializer, SellerSerializer, MarketHyperlinkedSerializer
from market_app.models import Market, Seller
from rest_framework.views import APIView
from rest_framework import mixins, generics

# Bekommen wir hier eine HTML-View?? Was nutzt man das, bzw wo ist der unterschied zu den anderen??
# Ist das hier die ListView für POST und GET??
class MarketsView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)


class MarketsSingleView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin ,generics.GenericAPIView):

    # Wird für das GenericAPIView benötigt? (Die zwei Zeilen)
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs) # retrieve, weil ein einzelne Instanz/Objekt??

    def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
                return self.destroy(request, *args, **kwargs)

# @api_view(['GET', 'DELETE', 'PUT'])
# def markets_single_view(request, pk):
    
#     if request.method == 'GET':
#         market = Market.objects.get(pk=pk) 
#         serializer = MarketSerializer(market, many=False, context={'request': request}) 
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         market = Market.objects.get(pk=pk)
#         serializer = MarketSerializer(market, data=request.data, partial=True, context={'request': request})
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     if request.method == 'DELETE':
#         market = Market.objects.get(pk=pk) 
#         serializer = MarketSerializer(market, many=False, context={'request': request})
#         market.delete()
#         return Response(serializer.data)


@api_view(['GET', 'POST'])
def seller_view(request):
    
    if request.method == 'GET':
        sellers = Seller.objects.all() 
        # wegen 'many=True' bekommen wir eine Liste mehrerer Objects zurück (ist das eine ListView??)
        serializer = SellerSerializer(sellers, many=True, context={'request': request}) 
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
        # wegen 'many=False' bekommen wir keine Liste sondern ein einzelnes Object zurück
        serializer = SellerSerializer(seller, many=False,context={'request': request}) 
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = SellerSerializer(seller, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        seller.delete()
        return Response(status=204)
            