from rest_framework import serializers
from .models import LoanApplication, FraudFlag
from django.contrib.auth import get_user_model

User = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Serializes basic user information for loan display purposes.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User 
        fields = ['id', 'email', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name() 


class LoanRequestSerializer(serializers.ModelSerializer):
    """
    Handles serialization, validation, and creation of loan applications.
    """

    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = LoanApplication 
        fields = ['user', 'amount_requested', 'purpose', 'status', 'date_applied']
        read_only_fields = ['date_applied']  

    def validate_amount_requested(self, value):
        """
        Validates that amount is not negative or empty.
        """

        if value is None:
            raise serializers.ValidationError("The amount requested cannot be empty.")
        if value < 0:
            raise serializers.ValidationError("The amount requested cannot be a negative value.")
        return value

    def validate_purpose(self, value):
        """
        Validates that purpose is a clean, meaningful string.
        """

        value = value.strip()
        if not value:
            raise serializers.ValidationError("The purpose cannot be empty.")
        if value.isdigit():
            raise serializers.ValidationError("Purpose cannot be purely numeric.")
        if len(value) > 100:
            raise serializers.ValidationError("Purpose cannot exceed 100 characters.")
        return value
    
    def validate_status(self, value):
        """
        Ensures that the status value is within allowed choices.
        """
        if value not in dict(LoanApplication.STATUS_CHOICES):
            raise serializers.ValidationError("Invalid status choice")
        return value



    def create(self, validated_data):
        """
        Creates a loan application and associates it with the requesting user.
        Status is initialized as 'pending'.
        """

        user = self.context['request'].user 
        return LoanApplication.objects.create(user=user, status='pending', **validated_data)


    def update(self, instance, validated_data):
        """
        Allows updating the loan status (e.g., approve, reject, flag).
        """

        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
