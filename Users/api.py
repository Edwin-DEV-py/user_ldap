from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from djoser.views import TokenCreateView

@api_view(['POST'])
def ldap_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Autenticación a través de LDAP
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            # Iniciar sesión del usuario
            login(request, user)

            # Utiliza la vista TokenCreateView de Djoser para generar tokens de acceso y actualización
            token_create_view = TokenCreateView.as_view()
            token_request = request._request  # Obtener el objeto HttpRequest subyacente
            response = token_create_view(token_request)
            
            if response.status_code == status.HTTP_201_CREATED:
                token = response.data.get('access')
                return Response({
                    'message': 'Logged in successfully',
                    'username': user.username,
                    'is_superuser': user.is_superuser,
                    'jwt': token
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Error generating tokens'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Account is inactive'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

