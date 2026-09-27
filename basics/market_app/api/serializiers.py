from rest_framework import serializers
from market_app.models import Market, Seller, Product

# --- 1. INDUSTRIE-STANDARD: SAUBERE MODEL-SERIALIZER ---

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['id', 'name', 'location', 'description', 'net_worth']
        
    def validate_name(self, value): 
        if 'X' in value or 'Y' in value:
            raise serializers.ValidationError("Name darf kein X oder Y enthalten.")
        return value


class SellerSerializer(serializers.ModelSerializer):
    # LESE-LOGIK: Verschachtelte Markt-Details (GET)
    markets = MarketSerializer(many=True, read_only=True)
    
    # SCHREIB-LOGIK: Nimmt nur IDs entgegen für saubere Verknüpfung (POST/PUT)
    markets_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(),
        many=True,
        write_only=True,
        source='markets'
    )
    
    # Dynamisches Feld (berechnet zur Laufzeit)
    market_count = serializers.SerializerMethodField()
 
    class Meta:
        model = Seller
        fields = ['id', 'name', 'contact_info', 'markets', 'markets_ids', 'market_count']

    def get_market_count(self, obj):
        return obj.markets.count()


class ProductSerializer(serializers.ModelSerializer):
     class Meta:
            model = Product
            fields = '__all__'


# =====================================================================
# --- LERN-ARCHIV: ALTE VERSIONEN & ANTWORTEN AUF DEINE FRAGEN ---
# =====================================================================

# FRAGE: WICHTIG: Normale Serializer (serializers.Serializer) nutzt z.B. wann? Nenne Beispiele.
# ANTWORT: Wenn es keine Datenbank-Tabelle gibt. 
# Beispiel 1: Ein Login-Serializer (nimmt username/password, checkt sie, gibt ein Token zurück, speichert aber nichts).
# Beispiel 2: Ein ContactFormSerializer (nimmt Name/E-Mail/Nachricht, verschickt eine E-Mail über einen SMTP-Server, speichert aber nichts in der DB).

# FRAGE: Was ist ein 'Base' und 'List' Serializer??
# ANTWORT: Das sind oft nur Namenskonventionen der Entwickler. 
# Ein "List"-Serializer hat oft weniger Felder (z.B. ohne langes 'description'-Feld), damit die Ladezeit der Liste schneller ist. 
# Ein "Detail"-Serializer zeigt dann alle Felder an, wenn man auf ein einzelnes Objekt klickt.

# FRAGE: ist view_name einfach ein HyperLink? Was passiert da genau?
# ANTWORT: Ja. Ein HyperlinkedModelSerializer gibt statt IDs (z.B. "market_id": 1) direkt eine fertige klickbare URL für das Frontend aus 
# (z.B. "market": "http://127.0.0.1:8000/api/market/1/"). Das 'view_name' sagt DRF, welche URL aus der urls.py es dafür zusammenbauen soll.
# Wird in der Praxis seltener genutzt als PrimaryKeyRelatedField, da moderne Frontends (React/Vue) sich ihre Routen lieber selbst bauen.

# --- DEIN ALTER MANUELLER PRODUCT-SERIALIZER (Stufe 1: Handarbeit) ---
# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=255)
#     description = serializers.CharField()
#     price = serializers.DecimalField(max_digits=50, decimal_places=2)
#     market = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all())
#     seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())
#     def create(self, validated_data):
#          return Product.objects.create(**validated_data)

# --- DEIN HYPERLINKED SERIALIZER-VERSUCH ---
# class MarketHyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):
#     sellers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='seller_single')
#     class Meta:
#         model = Market
#         fields = ['url', 'id', 'sellers', 'name', 'location', 'description', 'net_worth']