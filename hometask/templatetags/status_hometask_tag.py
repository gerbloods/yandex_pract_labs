from django import template

register = template.Library()


@register.simple_tag
def hometask_status(is_done):
    if is_done:
        return "Выполнено"

    return "Не выполнено"