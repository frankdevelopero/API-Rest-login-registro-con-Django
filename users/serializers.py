from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework.serializers import (
    CharField,
    EmailField,
)


class UserLoginSerializer(serializers.ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label="Correo electrónico", required=True, allow_blank=False)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token',
            'first_name',
            'last_name',
            'id',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "id": {"read_only": True},
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email:
            raise ValidationError("Ingresa  tu correo, es requerido")
        user = User.objects.filter(
            Q(email=email)
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('Este correo no esta registrado')

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Credenciales incorrectas, intenta de nuevo")
        data["token"] = "TOKEN RANDOM" # generar token y enviar
        data["first_name"] = user_obj.first_name
        data["last_name"] = user_obj.last_name
        data["id"] = user_obj.id
        return data


class UserSerializer(serializers.Serializer):
    passid = serializers.ReadOnlyField()  # Permitimos solo para lectura
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        """
        Crea una instancia de User a partir de los datos de Validate Data
        que contiene valores deserializados
        :param validated_data: Diccionario con datos de Usuario
        :return: objeto User
        """
        instance = User()
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza una instancia a partir de los datos
        :param instance:
        :param validated_data:
        :return: objeto actualizado
        """
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email = validated_data.get('email')
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def validate_email(self, data):
        """
        Valida si existe un usuario con el mismo email
        :param data:
        :return: Data
        """
        users = User.objects.filter(email=data)
        if not self.instance and len(users) != 0:
            raise serializers.ValidationError(data+" ya esta registrado")

        elif self.instance and self.instance.username != data and len(users) != 0:
            raise serializers.ValidationError(data+" ya esta registrado")

        else:
            return data
