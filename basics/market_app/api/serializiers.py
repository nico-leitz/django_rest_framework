from rest_framework import serializers
from market_app.models import Market, Seller, Product
             

class MarketSerializer(serializers.HyperlinkedModelSerializer):

    # ist view_name einfach ein HyperLink? Was passiert da genau?
    sellers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='seller_single')

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in  existing - allowed:
                self.fields.pop(field_name)
    
    class Meta:
        model = Market
        fields = ['url', 'id', 'sellers', 'name', 'location', 'description', 'net_worth'] # '__all__' nimmt alle Felder
    #   exclude = ['net_worth'] # man kann ich daten ausschließen

    def validate_name(self, value): 
        errors = []
        
        if 'X' in value:
            errors.append('no X in location')
        if 'Y' in value:
            errors.append('no Y in location')

        if errors:
            raise serializers.ValidationError(errors)
        return value

# Vererbung / Wann nutzen??
class MarketHyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):

    # ist view_name einfach ein HyperLink? Was passiert da genau?
    sellers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='seller_single')
    
    class Meta:
        model = Market
        fields = ['url', 'id', 'sellers', 'name', 'location', 'description', 'net_worth'] # '__all__' nimmt alle Felder
    #   exclude = ['net_worth'] # man kann ich daten ausschließen

    def validate_name(self, value): 
        errors = []
        
        if 'X' in value:
            errors.append('no X in location')
        if 'Y' in value:
            errors.append('no Y in location')

        if errors:
            raise serializers.ValidationError(errors)
        return value


class SellerSerializer(serializers.ModelSerializer):
    
    markets = MarketSerializer(many=True, read_only=True)
    markets_ids = serializers.PrimaryKeyRelatedField(
        queryset = Market.objects.all(),
        many = True,
        write_only = True,
        source = 'markets'
    )

    market_count = serializers.SerializerMethodField()
 
    class Meta:
        model = Seller
        fields = '__all__'

    def get_market_count(self, obj):
        return obj.markets.count()


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())

    def create(self, validated_data):
         return Product.objects.create(**validated_data)



## WICHTIG: Wenn wir kein Model haben können wir auch keinen ModelSerializer nutzen
## Normale Serializer nutzt z.B. wenn (Datenabweichen?) ??? Nenne Beispiele

## Was ist ein 'Base' und 'List' Serializer??