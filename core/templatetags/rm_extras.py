from django import template

register = template.Library()


@register.filter
def rupiah(value):
    try:
        return "Rp" + f"{int(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "Rp0"


@register.filter
def get_item(value, key):
    if isinstance(value, dict):
        return value.get(key)
    return None
