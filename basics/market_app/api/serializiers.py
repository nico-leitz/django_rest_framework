from rest_framework import serializers
from market_app.models import Market, Seller

def validate_no_x_or_y(value): # was passiert hier?
        errors = [] # Alle fehler ziehen
        
        if 'X' in value:
            errors.append('no X in location')
        if 'Y' in value:
            errors.append('no Y in location')

        if errors:
             raise serializers.ValidationError(errors) # Ein der Fehler ausgeben
        return value
              

# Würde der Serializer meckern, wenn ich die länge überschreite?
# Was macht der Serializer, was json.loads / json.dumps nicht macht und wieso nutzen wir den?
class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, validators=[validate_no_x_or_y])
    location = serializers.CharField(max_length=255)
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    # Anhand der Instanz ist dem Serializer klar, welche methode (z.B. create oder update verwendet werden muss)
    # bezieht sich das .self immer auf die jeweilige instanz (also immer eine?)

    def create(self, validated_data): # Wird automatisch ausgeführt? (wenn ja wann??)
        # Hat das was mit der "POST-Methode" aus den views zu tuhen??
        # Wir übergeben nicht das dictionary selbst die die keyword-dictonary arguments (kwargs)
        return Market.objects.create(**validated_data)

    def update(self, instance, validated_data): # Wird automatisch ausgeführt? (wenn ja wann??)
            # Hat das was mit der "PUT-Methode" aus den views zu tuhen??
            instance.name = validated_data.get('name', instance.name)
            instance.location = validated_data.get('location', instance.location)
            instance.description = validated_data.get('description', instance.description)
            instance.net_worth = validated_data.get('net_worth', instance.net_worth)
            instance.save()
            return instance

    # Für einzelne Felder??
    def validate_location(self, value): # was ist der value?? (die location?)
        if 'X' in value:
            raise serializers.ValidationError('no X in location')
        return value


class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField(max_length=255)
    markets = MarketSerializer(read_only=True, many=True) # was genau passiert hier?

class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField(max_length=255)
    markets = serializers.ListField(write_only=True, child=serializers.IntegerField()) #??

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError("some Market-id's not found")
        return value

    def create(self, validated_data):
         market_ids = validated_data.pop('markets')
         seller = Seller.objects.create(**validated_data) # was sind die ** mit validated data?
         markets = Market.objects.filter(id__in=market_ids)
         seller.markets.set(markets)
         return seller