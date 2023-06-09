from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, GetTokenPairSerializer
from rest_framework.views import APIView
from django.db import IntegrityError
from .response import *
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'users/home.html'


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return success()
                except IntegrityError as ex:
                    return bad_request_error(str(ex))
            return bad_request_error(serializer.errors)
        except Exception as ex:
            return system_error(str(ex))


class GetTokenPairView(TokenObtainPairView):
    serializer_class = GetTokenPairSerializer

    def post(self, request, *args, **kwargs):
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

