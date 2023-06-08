import re
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


def custom_password_validator(password):
    pass_regex = r"\d.*\d"
    if len(password) < 10:
        raise ValidationError("Password must be at least 10 characters long.")
    if not re.search(pass_regex, password):
        raise ValidationError("Password must contain at least 2 digits.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least 1 special character.")

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[custom_password_validator])
    email = serializers.EmailField(validators=[EmailValidator()])

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.errors:
            error_data = {
                'status': 'error',
                'message': self.errors,
            }
            return error_data
        return data

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name = validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class GetTokenPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)

        return attrs
