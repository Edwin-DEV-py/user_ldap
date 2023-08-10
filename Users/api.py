from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
import jwt
import datetime
from ldap3 import Connection, Server

##esta vista sirve para la API de django rest framework que se utilizara para conectar al cliente y genera el token de acceso.
@api_view(['POST'])
@permission_classes([])
def ldap_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

            # Generar el token JWT
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            secret = '3eaf50158d956cef59f00c45a42cabb143a8c6e8e26492ab8bac12dd6a2a2221'
            token = jwt.encode(payload, secret, algorithm='HS256')
            
            # Obtener grupos del usuario desde LDAP
            server = Server('ldap://192.168.0.50')  # Cambia la URL del servidor LDAP
            with Connection(server, user=user.username, password=password, auto_bind=True) as conn:
                conn.search('dc=ejemplo,dc=local', f'(sAMAccountName={user.username})', attributes=['memberOf'])
                groups = conn.entries[0]['memberOf']

            # Convertir la respuesta a una lista de cadenas
            group_names = [group for group in groups]

            return Response({
                'message': 'Logged in successfully',
                'username': user.username,
                'is_superuser': user.is_superuser,
                'jwt': token,
                'ldap_groups': group_names
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Account is inactive'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

