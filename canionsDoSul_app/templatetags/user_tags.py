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

@register.filter
def not_in(value, args):
    return value not in args.split(',')