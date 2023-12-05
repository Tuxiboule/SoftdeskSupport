from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from authentification.models import User
from datetime import date


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'birthdate',
                  'can_be_contacted',
                  'can_be_shared']

    def validate_birthdate(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans.")

        return value

    def create(self, validated_data):
        validated_data['birthdate'] = self.validate_birthdate(validated_data['birthdate'])
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.birthdate = self.validate_birthdate(validated_data.get('birthdate', instance.birthdate))
        instance.save()
        return instance
