from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializiers import MarketSerializer, SellerDetailSerializer, SellerCreateSerializer
from market_app.models import Market, Seller

@api_view(['GET', 'POST']) 
def first_view(request):
    
    if request.method == 'GET':
        # 1. DB abfragen.
        markets = Market.objects.all() 
        
        # 2. many=True ist ZWINGEND, da wir eine Liste/QuerySet übergeben.
        # Hier wird der Serializer nur vorbereitet, noch nichts umgewandelt.
        serializer = MarketSerializer(markets, many=True) 
        
        # 3. .data startet die Umwandlung (DB -> Dict -> JSON). 
        # Response kümmert sich um die korrekte HTTP-Formatierung.
        return Response(serializer.data)
    
    if request.method == 'POST':
        # JSON-Daten (request.data) in den Serializer werfen.
        serializer = MarketSerializer(data=request.data)
        
        # MUSS zwingend gerufen werden! Führt max_length, validate_location etc. aus.
        if serializer.is_valid():
            # Weil wir dem Serializer KEINE DB-Instanz gegeben haben, triggert save() -> create()
            serializer.save()
            return Response(serializer.data)
        else:
            # Enthält genau, in welchen Feldern Fehler aufgetreten sind.
            return Response(serializer.errors)
        

@api_view(['GET', 'DELETE', 'PUT'])
def markets_single_view(request, pk):
    
    if request.method == 'GET':
        market = Market.objects.get(pk=pk) 
        # many=False (Default), weil wir nur EIN Objekt abfragen.
        serializer = MarketSerializer(market, many=False) 
        return Response(serializer.data)

    if request.method == 'PUT':
            market = Market.objects.get(pk=pk)
            
            # WICHTIG: Wir übergeben Objekt UND Daten. 
            # Das sagt DRF: "Aha, es existiert schon! Bei save() muss ich update() nutzen!"
            # partial=True: Erlaubt unvollständige Daten (z.B. nur 'name' wird gesendet).
            serializer = MarketSerializer(market, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save() # Triggert die update() Methode im Serializer.
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

    if request.method == 'DELETE':
            market = Market.objects.get(pk=pk) 
            serializer = MarketSerializer(market, many=False)
            market.delete() # Direkt löschen, Serializer wird nur noch für die letzte Antwort genutzt.
            return Response(serializer.data)


@api_view(['GET', 'DELETE', 'POST'])
def seller_view(request):
    
    if request.method == 'GET':
        sellers= Seller.objects.all() 
        # Lese-Serializer liefert schöne Strings statt reiner IDs.
        serializer = SellerDetailSerializer(sellers, many=True) 
        return Response(serializer.data)

    if request.method == 'POST':
            # Schreib-Serializer erwartet eine ID-Liste und baut die ManyToMany-Beziehung.
            serializer = SellerCreateSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save() # save ruft Serializer-Methoden auf
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
