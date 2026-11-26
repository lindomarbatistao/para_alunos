from rest_framework import serializers
from .models import Usuario, Imovel, Contrato, Pagamento
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Usuario, Imovel, Contrato, Pagamento


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    nome = serializers.CharField()
    telefone = serializers.CharField(
        required=False,
        allow_blank=True,
        default=""
    )
    tipo = serializers.ChoiceField(
        choices=Usuario.TipoUsuario.choices
    )

    def create(self, validated_data):
        tipo = validated_data["tipo"]

        usuario = Usuario.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            nome=validated_data["nome"],
            telefone=validated_data.get("telefone", ""),
            tipo=tipo,
            is_staff=(tipo == Usuario.TipoUsuario.ADMINISTRADOR),
            is_active=True,
            is_superuser=False
        )

        return usuario

class UsuarioMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "nome",
            "first_name",
            "last_name",
            "telefone",
            "tipo",
            "is_staff",
            "is_superuser",
            "is_active",
            "password"
        ]

        read_only_fields = [
            "is_staff",
            "is_superuser",
            "is_active"
        ]
        
        extra_kwargs = {
            "password":{"write_only": True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
  
        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class ImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imovel
        fields = '__all__'


class ContratoSerializer(serializers.ModelSerializer):
    imovel_nome = serializers.CharField(source="imovel.titulo", read_only=True)
    proprietario_nome = serializers.CharField(source="proprietario.nome", read_only=True)
    morador_nome = serializers.CharField(source="morador.nome", read_only=True)

    class Meta:
        model = Contrato
        fields = [
            "id",
            "data_inicio",
            "data_fim",
            "valor",
            "imovel",
            "imovel_nome",
            "proprietario",
            "proprietario_nome",
            "morador",
            "morador_nome",
        ]


class PagamentoSerializer(serializers.ModelSerializer):
    # detalhes para exibição no front
    contrato_label = serializers.SerializerMethodField()
    imovel_nome = serializers.CharField(source="contrato.imovel.titulo", read_only=True)
    morador_nome = serializers.CharField(source="contrato.morador.nome", read_only=True)
    proprietario_nome = serializers.CharField(source="contrato.proprietario.nome", read_only=True)

    class Meta:
        model = Pagamento
        fields = [
            "id",
            "data_pagamento",
            "valor",
            "status",
            "contrato",
            "contrato_label",
            "imovel_nome",
            "proprietario_nome",
            "morador_nome",
        ]

    def get_contrato_label(self, obj):
        # exemplo: "Contrato #5"
        return f"Contrato #{obj.contrato_id}" if obj.contrato_id else "—"


