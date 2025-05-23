from django import template

register = template.Library()

@register.filter
def translate_role(role):
    return {
        'specialist': 'Especialista',
        'scientist': 'Cientista',
        'user': 'Usuário',
        'admin': 'Administrador',
        'default': 'Padrão'
    }.get(role, role)