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

@register.simple_tag
def is_specialist_or_scientist(user):
    return user.role in ['specialist', 'scientist']

@register.simple_tag
def is_specialist_or_scientist_admin(user):
    return user.role in ['specialist', 'scientist', 'admin']

@register.simple_tag
def is_admin(user):
    return user.is_authenticated and user.role == "admin"