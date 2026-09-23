from rest_framework import serializers
from market_app.models import Market

class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    def create(self, validated_data):
        # Wir übergeben nicht das dictionary selbst die die keyword-dictonary arguments (kwargs)
        return Market.objects.create(**validated_data) 