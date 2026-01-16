from rest_framework import serializers
from .models import PerksBenefits

class PerksBenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerksBenefits
        fields = [
            "id",
            "user",
            "name",
            "description",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at"
        ]

        