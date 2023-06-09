import re
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

"""
This code defines a custom password validator function named custom_password_validator().
The function takes a password as input.
It uses regular expressions to enforce specific password requirements:
pass_regex checks if there are at least two digits in the password.
The first if statement checks if the password length is less than 10 characters.
The second if statement checks if the password meets the digit requirement.
The third if statement checks if the password contains at least one special character.
If any of the requirements fail, a ValidationError is raised.
"""
def custom_password_validator(password):
    pass_regex = r"\d.*\d"
    if len(password) < 10:
        raise ValidationError("Password must be at least 10 characters long.")
    if not re.search(pass_regex, password):
        raise ValidationError("Password must contain at least 2 digits.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least 1 special character.")


"""
The CustomUserSerializer class is defined for serializing the CustomUser model.
The serializer includes fields for id, name, email, and password.
The password field is marked as write_only to ensure it is not included when serializing the data.
The email field uses the EmailValidator to validate the email format.
The to_representation() method is overridden to handle errors during serialization. If there are any errors, a custom error response is returned.
The Meta class specifies the model as CustomUser and lists the desired fields to include in the serialized representation.
The create() method is overridden to handle the creation of a new CustomUser instance. It calls CustomUser.objects.create_user() with the validated data

"""
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


"""
The GetTokenPairSerializer class extends the TokenObtainPairSerializer provided by Django REST Framework SimpleJWT.
The validate() method is overridden to add custom fields to the token response.
It calls the parent class's validate() method to perform the default validation.
The user is obtained either from self.user or self.context['user'].
The user_id is added to the response data before returning it.
"""
class GetTokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user or self.context['user']

        # Add custom fields to the response
        data['user_id'] = user.id

        return data