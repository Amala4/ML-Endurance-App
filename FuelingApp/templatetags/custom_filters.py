from django import template

register = template.Library()

@register.filter
def format_duration(value):
    try:
        minutes = int(value)
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m" if hours else f"0h {remaining_minutes}m"
    except (ValueError, TypeError):
        return "No workout entered yet"
