from rest_framework import serializers

from .models import Recipient


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ["name", "postal_code", "phone_number"]


class VerificationCodeSerializer(serializers.Serializer):
    verification_code = serializers.CharField(min_length=6, max_length=6)
