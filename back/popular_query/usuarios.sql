python manage.py shell

from api.models import Usuario

usuarios = [
    ("carlos", "Carlos Silva", "carlos.silva@email.com", "11999990001", "PROPRIETARIO"),
    ("ana", "Ana Souza", "ana.souza@email.com", "11999990002", "PROPRIETARIO"),
    ("marcos", "Marcos Lima", "marcos.lima@email.com", "11999990003", "PROPRIETARIO"),
    ("juliana", "Juliana Pereira", "juliana.pereira@email.com", "11999990004", "MORADOR"),
    ("rafael", "Rafael Costa", "rafael.costa@email.com", "11999990005", "MORADOR"),
    ("fernanda", "Fernanda Alves", "fernanda.alves@email.com", "19985545202", "MORADOR"),
    ("bruno", "Bruno Rocha", "bruno.rocha@email.com", "11999990007", "PROPRIETARIO"),
    ("patricia", "Patrícia Gomes", "patricia.gomes@email.com", "11999990008", "MORADOR"),
    ("lucas", "Lucas Martins", "lucas.martins@email.com", "19985545365", "MORADOR"),
    ("camila", "Camila Ribeiro", "camila.ribeiro@email.com", "11999990010", "PROPRIETARIO"),
]

for username, nome, email, telefone, tipo in usuarios:
    if not Usuario.objects.filter(username=username).exists():
        Usuario.objects.create_user(
            username=username,
            nome=nome,
            email=email,
            telefone=telefone,
            tipo=tipo,
            password="Senai@123"
        )
        print("Criado:", username)
    else:
        print("Já existe:", username)
