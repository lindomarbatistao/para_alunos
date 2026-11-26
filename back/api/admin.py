from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario, Imovel, Contrato, Pagamento

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Dados do sistema de aluguéis",
            {
                "fields": (
                    "telefone",
                    "tipo",
                )
            }
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Dados do sistema de aluguéis",
            {
                "fields": (
                    "email",
                    "telefone",
                    "tipo",
                )
            }
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "tipo",
        "is_staff",
        "is_active",
        "telefone"
    )

    list_filter = (
        "tipo",
        "is_staff",
        "is_active",
    )

admin.site.register(Imovel)
admin.site.register(Contrato)
admin.site.register(Pagamento)
