from rest_framework import generics
from rest_framework.response import Response
from .serializers import RegisterSerializer
from .jwt import CustomTokenObtainPairSerializer


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
        return Response({
            "token": str(CustomTokenObtainPairSerializer.get_token(user)),
            "message": "successful"
        })
