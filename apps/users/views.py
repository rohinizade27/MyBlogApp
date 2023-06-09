from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, GetTokenPairSerializer
from rest_framework.views import APIView
from django.db import IntegrityError
from .response import *
from django.views.generic import TemplateView


"""
The HomeView class is a view that extends TemplateView.
It renders the users/home.html template.
"""
class HomeView(TemplateView):
    template_name = 'users/home.html'


"""
The RegisterView class is an API view that handles user registration.
It extends the APIView class and allows any user to access it (permission_classes = [AllowAny]).
The post() method is responsible for handling the HTTP POST request.
Inside the method, an instance of CustomUserSerializer is created with the request data.
If the serializer is valid, the user data is saved using serializer.save().
If the save operation raises an IntegrityError, a bad request response is returned with the error message.
If the serializer is invalid, a bad request response is returned with the validation errors.
Any other exceptions that occur during the registration process result in a system error response.
"""
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Create an instance of the CustomUserSerializer with the request data
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    # Save the user data
                    serializer.save()
                    return success()  # Return a success response
                except IntegrityError as ex:
                    return bad_request_error(str(ex))  # Return a bad request response with the error message
            return bad_request_error(serializer.errors)  # Return a bad request response with the validation errors
        except Exception as ex:
            return system_error(str(ex))  # Return a system error response with the error message

"""
The GetTokenPairView class is a view used to obtain token pairs (access token and refresh token).
It extends the TokenObtainPairView provided by Django REST Framework SimpleJWT.
The serializer_class attribute is set to GetTokenPairSerializer.
The post() method handles the HTTP POST request for obtaining token pairs.
An instance of GetTokenPairSerializer is created with the request data.
The serializer is validated, and if it's valid, the super().post() method is called to generate the token pair response.
The response data is customized by including the refresh token, access token, and user ID.
The customized response data is returned in the API response.
"""
class GetTokenPairView(TokenObtainPairView):
    serializer_class = GetTokenPairSerializer

    def post(self, request, *args, **kwargs):
        # Create an instance of the GetTokenPairSerializer with the request data
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        response = super().post(request, *args, **kwargs)

        # Customize the response format
        response_data = {
            'refresh': response.data['refresh'],
            'access': response.data['access'],
            'user_id': response.data['user_id'],
        }

        return Response(response_data)


