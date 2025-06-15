from django import template

register = template.Library()

@register.filter
def translate_role(role):
    return {
        'user': 'Usuário',
        'specialist': 'Especialista',
        'scientist': 'Cientista',
        'admin': 'Administrador',
        'default': 'Padrão',
        'anonymous': 'Anônimo'
    }.get(role, role)

@register.filter
def not_in(value, args):
    return value not in args.split(',')