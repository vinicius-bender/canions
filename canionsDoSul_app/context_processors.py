def breadcrumbs(request):
    path = request.path
    parts = [p for p in path.strip('/').split('/') if p]
    breadcrumbs = []
    url = ''
    
    breadcrumb_names = {
        'cadastrar': 'Cadastrar Cadeia Taxonômica',
        'criar_observacao': 'Criar Observação',
        'minhas_observacoes': 'Minhas Observações',
        'observacoes': 'Últimas Observações',
        'criar_espécie': 'Criar Espécie',
        'criar_familia': 'Criar Familia',
        'criar_genero': 'Criar Genero',
        'criar_localizacao': 'Criar Localização',
        'criar_observação': 'Criar Observação',
        'deletar_observacao': 'Deletar Observação',
        'editar_observacao': 'Editar Observação',
        'Home': 'Home',
        'registrar': 'Registrar Usuário',
        'latlng': 'Cadastro por Latitude/Longitude',
        'cidade': 'Cadastro por Cidade/Estado',
        'promover_usuario': 'Promover Usuário',
        # adicione mais conforme necessário
    }

    for part in parts:
        url += f'/{part}'
        breadcrumbs.append({
            'name': breadcrumb_names.get(part, part.replace('_', ' ').capitalize()),
            'url': url
        })
    
    return {'breadcrumbs': breadcrumbs}

def user_roles(request):
    user = request.user
    return {
        'is_specialist': hasattr(user, 'specialist'),
        'is_scientist': hasattr(user, 'scientist'),
    }