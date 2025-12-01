from rest_framework import serializers
from .models import Listing, Feature

class ListingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    features = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Feature.objects.all()
    )

    class Meta:
        model = Listing
        fields = [
            'id', 'user', 'city', 'make', 'car_model', 'generation',
            'year', 'mileage_km', 'body_type', 'fuel_type',
            'transmission', 'drive_type', 'color',
            'engine_volume_l', 'power_hp', 'steering_wheel',
            'condition', 'vin', 'description',
            'price_kzt', 'status', 'published_at',
            'features',
            'contact_name', 'contact_phone',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['published_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        features = validated_data.pop('features', [])
        listing = Listing.objects.create(**validated_data)
        listing.features.set(features)
        return listing
        
    def update(self, instance, validated_data):
        features = validated_data.pop('features', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        if features is not None:
            instance.features.set(features)
        return instance