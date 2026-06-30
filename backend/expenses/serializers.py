from rest_framework import serializers
from .models import Expense, AppSettings


class ExpenseSerializer(serializers.ModelSerializer):
    """Full serializer for the Expense model."""

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'category', 'date', 'description',
            'timestamp', 'suspicious', 'suspicious_reason',
        ]
        read_only_fields = ['id', 'timestamp', 'suspicious', 'suspicious_reason']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_category(self, value):
        if not value.strip():
            raise serializers.ValidationError("Category cannot be empty.")
        return value.strip()


class AppSettingsSerializer(serializers.ModelSerializer):
    """Serializer for the singleton settings row."""

    class Meta:
        model = AppSettings
        fields = ['daily_limit']
