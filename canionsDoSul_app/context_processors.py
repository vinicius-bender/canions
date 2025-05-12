def breadcrumbs(request):
    path = request.path
    parts = [p for p in path.strip('/').split('/') if p]
    breadcrumbs = []
    url = ''
    
    breadcrumb_names = {
        'cadastrar': 'Cadastrar',
        'criar_observacao': 'Criar Observação',
        'minhas_observacoes': 'Minhas Observações',
        'observacoes': 'Últimas observações',
        'criar_espécie': 'Criar espécie',
        'criar_familia': 'Criar familia',
        'criar_genero': 'Criar genero',
        'criar_localizacao': 'Criar localização',
        'criar_observação': 'Criar observação',
        'deletar_observacao': 'Deletar observação',
        'editar_observacao': 'Editar observação',
        'Home': 'Home',
        # adicione mais conforme necessário
    }

    for part in parts:
        url += f'/{part}'
        breadcrumbs.append({
            'name': breadcrumb_names.get(part, part.replace('_', ' ').capitalize()),
            'url': url
        })
    
    return {'breadcrumbs': breadcrumbs}