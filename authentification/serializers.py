from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from authentification.models import User
from datetime import date


class UserSerializer(ModelSerializer):
    """
    Serializer for the User model.

    Attributes:
        password (CharField): Write-only field for the user's password.
        Other fields correspond to User model attributes.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'password',
                  'birthdate',
                  'can_be_contacted',
                  'can_be_shared',
                  'is_supervisor']

    def validate_birthdate(self, value):
        """
        Validate that the user's age is at least 15 years.

        Args:
            value (date): User's birthdate.

        Returns:
            date: The validated birthdate.

        Raises:
            serializers.ValidationError: If the user is younger than 15 years.
        """
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError("You must be at least 15 years old.")
        return value

    def create(self, validated_data):
        """
        Create a new user instance with validated data.

        Args:
            validated_data (dict): Validated data for creating the user.

        Returns:
            User: Newly created User instance.
        """
        validated_data['birthdate'] = self.validate_birthdate(validated_data['birthdate'])
        return User.objects.create_user(**validated_data)
