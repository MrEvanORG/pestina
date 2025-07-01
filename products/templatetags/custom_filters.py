from django import template

register = template.Library()

@register.filter
def format_weight(value):
    try:
        kilos = int(value)
        grams = int(round((value - kilos) * 1000))
        result = ""

        if kilos > 0:
            result += f"{kilos} کیلوگرم"
        if grams > 0:
            result += f" و {grams} گرم" if kilos > 0 else f"{grams} گرم"
        if not result:
            result = "۰ گرم"

        return result
    except:
        return value
    

@register.filter
def format_toman(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return "۰ تومان"

    million = value // 1_000_000
    thousand = (value % 1_000_000) // 1_000

    if million and thousand:
        return f"{million} میلیون و {thousand} هزار تومان"
    elif million:
        return f"{million} میلیون تومان"
    elif thousand:
        return f"{thousand} هزار تومان"
    else:
        return f"{value:,} تومان"