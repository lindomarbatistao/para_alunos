from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario, Imovel, Contrato, Pagamento
from .serializers import *
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
# import pandas as pd

class MeView(RetrieveAPIView):
    serializer_class = UsuarioMeSerializer

    def get_object(self):
        # MUDANÇA: se não existir perfil, cria automaticamente
        # Motivo: evita erro para usuários criados pelo admin/shell
        perfil, created = Usuario.objects.get_or_create(
            user=self.request.user,
            defaults={
                "nome": self.request.user.username,  # sugestão
                "email": self.request.user.email,    # se existir no model Usuario
                "tipo": "morador",                      # obrigatório (NOT NULL no seu banco)
            }
        )
        return perfil


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Usuário criado com sucesso."}, status=status.HTTP_201_CREATED)


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsuarioFilter
    
    def get_queryset(self):
        qs = super().get_queryset()

        # Admin/staff tem acesso total
        if self.request.user.is_staff:
            return qs

        # Usuário comum: só o próprio perfil
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        # Quando chamar /usuarios/me/ usa o serializer específico
        if self.action == "me":
            return UsuarioMeSerializer
        return super().get_serializer_class()

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """
        GET /api/usuarios/me/
        Retorna o perfil Usuario do request.user + flags do User (is_staff, etc)
        """
        usuario = Usuario.objects.filter(user=request.user).first()
        if not usuario:
            return Response({"detail": "Perfil do usuário não encontrado."}, status=404)

        serializer = self.get_serializer(usuario)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="tipo-choices",
        permission_classes=[AllowAny],  # ✅ público: usado no Register
    )
    def tipo_choices(self, request):
        """
        GET /api/usuarios/tipo-choices/
        Retorna os choices do campo tipo (proprietario/morador)
        """
        return Response([
            {"value": v, "label": l}
            for v, l in Usuario.TIPO_CHOICES
        ])
    

class ImovelViewSet(ModelViewSet):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer
    permission_classes = [IsAuthenticated]

    # ✅ filtros
    filter_backends = [DjangoFilterBackend]
    filterset_class = ImovelFilter

    def get_queryset(self):
        qs = super().get_queryset()
        # Admin/staff vê tudo
        if self.request.user.is_staff:
            return qs
        # Usuário comum vê só os imóveis onde ele é proprietario
        return qs.filter(proprietario__user=self.request.user)


class PagamentoViewSet(ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = [IsAuthenticated]  # evita AnonymousUser

    filter_backends = [DjangoFilterBackend]
    filterset_class = PagamentoFilter  # o filtro certo

    def get_queryset(self):
        qs = super().get_queryset()

        # MUDANÇA (Item 5.2): admin vê tudo
        if self.request.user.is_staff:
            return qs

        # MUDANÇA (Item 5.2): usuário comum vê apenas contratos do seu perfil
        # return qs.filter(usuario__user=self.request.user)
        return qs.filter(contrato__proprietario__user=self.request.user)


class ContratoViewSet(ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContratoFilter
    
    def get_queryset(self):
        qs = super().get_queryset()

        # MUDANÇA (Item 5.2): admin vê tudo
        if self.request.user.is_staff:
            return qs

        # MUDANÇA (Item 5.2): usuário comum vê apenas contratos do seu perfil
        # return qs.filter(usuario__user=self.request.user)
        return qs.filter(proprietario__user=self.request.user)
    
    
class DashboardViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # só GET

    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer

    def list(self, request, *args, **kwargs):
        total_imoveis = Imovel.objects.count()
        disponiveis = Imovel.objects.filter(status='DISPONIVEL').count()
        alugados = Imovel.objects.filter(status='ALUGADO').count()
        pagamentos_em_aberto = Pagamento.objects.filter(status=False).count()

        # últimos 5 imóveis
        imoveis_destaque = (
            Imovel.objects
            .order_by('-id')[:5]
            .values('id', 'titulo', 'tipo', 'status', 'valor_aluguel', 'proprietario_id')
        )

        # últimos 5 contratos
        contratos_recentes = (
            Contrato.objects
            .select_related('imovel', 'proprietario', 'morador')
            .order_by('-id')[:5]
            .values(
                'id', 'data_inicio', 'data_fim', 'valor',
                'imovel_id', 'imovel__titulo',
                'proprietario__nome', 'morador__nome',
            )
        )

        return Response({
            "status": {
                "imoveis_cadastrados": total_imoveis,
                "disponiveis": disponiveis,
                "alugados": alugados,
                "pagamentos_em_aberto": pagamentos_em_aberto,
            },
            "imoveis_destaque": list(imoveis_destaque),
            "contratos_recentes": list(contratos_recentes),
        })
        


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def importar_imoveis(request):
#     arquivo = request.FILES.get("file")

#     if not arquivo:
#         return Response(
#             {"detail": "Nenhum arquivo enviado."},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         df = pd.read_excel(arquivo)

#         colunas_esperadas = ["titulo", "tipo", "valor_aluguel", "status", "proprietario_id"]
#         for coluna in colunas_esperadas:
#             if coluna not in df.columns:
#                 return Response(
#                     {"detail": f"Coluna obrigatória ausente: {coluna}"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         for _, row in df.iterrows():
#             proprietario_id = int(row["proprietario_id"])

#             if not Usuario.objects.filter(id=proprietario_id).exists():
#                 return Response(
#                     {"detail": f"proprietario com id {proprietario_id} não existe."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             Imovel.objects.create(
#                 titulo=row["titulo"],
#                 tipo=row["tipo"],
#                 valor_aluguel=row["valor_aluguel"],
#                 status=row["status"],
#                 proprietario_id=proprietario_id,
#             )

#         return Response(
#             {"detail": "Importação concluída com sucesso."},
#             status=status.HTTP_201_CREATED
#         )

#     except Exception as e:
#         return Response(
#             {"detail": f"Erro ao importar arquivo: {str(e)}"},
#             status=status.HTTP_400_BAD_REQUEST
#         )