from django import template

register = template.Library()

@register.filter(name='initials')
def initials(value):
    initials = ''

    # Split the name into parts and take the first letter of each part
    for name in value.split():
        if name:  # Ensure the part is not empty
            initials += name[0].upper()

    return initials
