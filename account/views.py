from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .serializers import RegisterSerializer,LoginSerializer,LogoutSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            data['username'] = data['username'].lower()
            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response({'errors': serializer.errors, 'message': "Something went wrong"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Save user and get the formatted data
            result = serializer.save()

            # Return the required response format
            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Exception:", e)
            return Response({'message': "Something went wrong"},
                            status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({'data': serializer.errors, 'message': "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
            
            token_data = serializer.get_jwt_token(serializer.validated_data)
            if 'access' not in token_data['data']:
                return Response(token_data, status=status.HTTP_401_UNAUTHORIZED)

            # Assuming you have a user object in the serializer
            return Response({
                'token_access': token_data['data']['access'],
                'token_refresh': token_data['data']['refresh'],
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("Exception:", e)
            return Response({'data': {}, 'message': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "User logged out"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        

