from rest_framework import serializers
from basics.models import Manufacturer, ManufacturerUser, Product, User

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'description', 'net_worth']
        
        # -------------------------------------------------------------------------
        # DER SERIALIZER ALS TÜRSTEHER UND ÜBERSETZER
        #
        # Die 'fields'-Liste ist eine ZWEISEITIGE Barriere:
        #
        # Bei einem POST / PUT (Eingehende Daten schreiben):
        # 1. TÜRSTEHER: Die 'fields' bestimmen, was überhaupt akzeptiert wird.
        #    Schickt der Nutzer Daten mit, die nicht in der Liste stehen, 
        #    werden sie aus Sicherheitsgründen verworfen.
        # 2. VALIDIERUNG: Er prüft, ob alle gelisteten Felder korrekt ausgefüllt 
        #    sind (z.B. Pflichtfelder da sind, Zahlenformate stimmen).
        # 3. SPEICHERUNG: Nach Aufforderung der View schreibt er sie in die DB.
        #
        # Bei einem GET (Ausgehende Daten abrufen):
        # 1. ÜBERSETZER: Er nimmt das komplexe Datenbankobjekt von der View.
        # 2. FILTER: Er übersetzt genau die Attribute in JSON, die in 'fields'
        #    stehen. Alles andere bleibt in der Datenbank verborgen.
        # --------------------------------------------------------------------------

class ManufacturerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerUser
        fields = ['manufacturer', 'user', 'role', 'joined_date']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'manufacturer', 'name', 'description', 'price']
