from django import template
register = template.Library()

@register.simple_tag
def stars(n: int, out_of: int = 5):
    n = int(n or 0)
    n = 0 if n < 0 else n
    n = out_of if n > out_of else n
    return '★' * n + '☆' * (out_of - n)
