from rest_framework import serializers
from market_app.models import Market, Seller

# --- 1. EIGENE VALIDATOREN (STANDALONE) ---
# Diese Funktion kann in beliebig vielen Serializern wiederverwendet werden.
# Sie wird aufgerufen, wenn in der View "is_valid()" ausgeführt wird.
def validate_no_x_or_y(value): 
    errors = [] # Sammelt alle gefundenen Fehler
    
    if 'X' in value:
        errors.append('no X in location')
    if 'Y' in value:
        errors.append('no Y in location')

    if errors:
         # Wirft einen Fehler. DRF fängt diesen ab und wandelt ihn in eine 
         # saubere 400 Bad Request JSON-Antwort für das Frontend um.
         raise serializers.ValidationError(errors)
    return value
              

# --- 2. DER BASIS-SERIALIZER (VOLLE KONTROLLE) ---
# Erbt von serializers.Serializer. Das heißt: Wir müssen jedes Feld, 
# create() und update() komplett selbst definieren.
# (Der Serializer macht das, was json.loads nicht kann: Validierung & DB-Management)
class MarketSerializer(serializers.Serializer):
    
    # read_only=True: Die ID wird von der DB vergeben. 
    # Bei einem POST (Erstellen) darf der User sie nicht mitschicken.
    id = serializers.IntegerField(read_only=True)
    
    # max_length=255: DRF meckert sofort, wenn der String zu lang ist.
    # validators=[...]: Hier binden wir unsere Standalone-Funktion von oben ein.
    name = serializers.CharField(max_length=255, validators=[validate_no_x_or_y])
    location = serializers.CharField(max_length=255)
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    # 'self' bezieht sich auf die Instanz dieses Serializers. ?? (Was ist diese Instanz? Wie sieht die aus?)

    # Wird AUTOMATISCH durch serializer.save() in der View aufgerufen, 
    # wenn wir KEIN bestehendes Datenbank-Objekt übergeben haben (also beim POST).
    def create(self, validated_data): 
        # **validated_data entpackt das Dictionary in Keyword-Argumente.
        # Aus {"name": "Lidl", "location": "Berlin"} wird (name="Lidl", location="Berlin").
        return Market.objects.create(**validated_data)

    # Wird AUTOMATISCH durch serializer.save() in der View aufgerufen, 
    # wenn wir ein bestehendes DB-Objekt übergeben haben (also beim PUT/PATCH).
    def update(self, instance, validated_data): 
            # .get() schaut: Gibt es neue Daten für 'name'? 
            # Wenn nein (z.B. bei PATCH), behalte den alten Wert (instance.name).
            instance.name = validated_data.get('name', instance.name)
            instance.location = validated_data.get('location', instance.location)
            instance.description = validated_data.get('description', instance.description)
            instance.net_worth = validated_data.get('net_worth', instance.net_worth)
            instance.save() # Speichert das geänderte Objekt in der DB.
            return instance

    # FELDSPEZIFISCHE VALIDIERUNG:
    # Namenskonvention: validate_<feldname>. DRF sucht automatisch danach.
    # "value" ist hier exakt der Inhalt, den der User für "location" mitgeschickt hat.
    def validate_location(self, value): 
        if 'X' in value:
            raise serializers.ValidationError('no X in location')
        return value


# --- 3. LESE-SERIALIZER (FÜR GET) ---
class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField(max_length=255)
    
    # many=True, weil ein Verkäufer mehrere Märkte hat (ManyToMany).
    # StringRelatedField gibt anstelle von nackten IDs (z.B. [1, 2]) 
    # die lesbaren __str__ Repräsentationen der Märkte aus (z.B. ["Aldi", "Lidl"]).
    markets = serializers.StringRelatedField(many=True)


# --- 4. SCHREIB-SERIALIZER (FÜR POST) ---
# Wir trennen Lesen und Schreiben, weil das Input-Format oft anders ist 
# als das gewünschte Output-Format.
class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField(max_length=255)
    
    # write_only=True: Wird nur für Input vom User genutzt, im Response wird es versteckt.
    # ListField mit child=IntegerField(): Erwartet ein JSON-Format wie "markets": [1, 2, 3]
    markets = serializers.ListField(write_only=True, child=serializers.IntegerField()) 

    # Prüft, ob alle vom User geschickten Markt-IDs überhaupt existieren.
    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            # Schickt der User 3 IDs, aber wir finden nur 2, werfen wir einen Fehler.
            raise serializers.ValidationError("some Market-id's not found")
        return value

    def create(self, validated_data):
         # WICHTIGSTER TEIL: ManyToMany (M2M) speichern.
         
         # 1. Wir reißen die IDs aus den Daten heraus (.pop), 
         # weil das Seller-Modell beim Erstellen keine direkte Liste verarbeiten kann.
         market_ids = validated_data.pop('markets')
         
         # 2. Seller in der Datenbank erstellen (nur mit name und contact_info).
         seller = Seller.objects.create(**validated_data) 
         
         # 3. Echte Markt-Objekte aus der DB holen.
         markets = Market.objects.filter(id__in=market_ids)
         
         # 4. M2M-Beziehungen können erst geknüpft werden, WENN das Hauptobjekt (Seller) existiert.
         seller.markets.set(markets) 
         return seller

