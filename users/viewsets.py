from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from users.serializers import UserSerializer, UserLoginSerializer

from rest_framework.response import Response
from rest_framework.views import APIView


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):

    """
    aqui agregar una clase de permisos permission_classes =
    Listar usuario solo puede hacer el super usuario
    """

    def list(self, request):
        paginator = PageNumberPagination()
        users = User.objects.all()

        # paginar el queryset
        paginator.paginate_queryset(users, request)
        serializer = UserSerializer(users, many=True)  # Serializa estos objetos y guarda en atributo data

        # devolver la respuesta paginada
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # devuelve el usuario creado
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        user = get_object_or_404(User, pk=pk)  # si exite devuelve si no lanza una excepcion
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        json = {
            "mensaje": "Usuario borrado con éxito"
        }
        return Response(json, status=status.HTTP_204_NO_CONTENT)
