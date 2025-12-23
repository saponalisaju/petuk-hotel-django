from django import template

register = template.Library()

bangla_digits = {
    '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
    '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯', '.': '.',
}

@register.filter
def bangla_number(value):
    value_str = str(value)
    return ''.join(bangla_digits.get(ch, ch) for ch in value_str)

@register.filter
def bangla_currency(value):
    return f"{bangla_number(value)}"

@register.filter
def bangla_pluralize(value):
    try:
        number = int(value)
    except (ValueError, TypeError):
        number = 0  
    if number == 1:
        return "১ টি পণ্য"
    else:
        return f"{bangla_number(number)} টি পণ্য"


@register.filter
def bangla_percent(value):
    return f"{bangla_number(value)}%"



