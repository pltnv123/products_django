from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': 'Р',
    'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
    """
    value: значение, к которому нужно применить фильтр
    code: код валюты
    """
    postfix = CURRENCIES_SYMBOLS[code]

    return f'{value} {postfix}'


def filter_message(message: str):
    """
    message: значение, которое мы получаем от пользователя
     return  - возвращает отфильтрованное от нецензурной лексики сообщение
    """
    variants = ['сука', 'блять', 'пиздец', 'no', 'filter']  # непристойные выражения

    ln = len(variants)
    filtred_message = ''
    string = ''
    pattern = '*'  # чем заменять непристойные выражения
    str(message)
    for i in message:
        string += i
        string2 = string.lower()

        flag = 0
        for j in variants:
            if not string2 in j:
                flag += 1
            if string2 == j:
                filtred_message += pattern * len(string)
                flag -= 1
                string = ''

        if flag == ln:
            filtred_message += string
            string = ''

    if string2 != '' and string2 not in variants:
        filtred_message += string
    elif string2 != '':
        filtred_message += pattern * len(string)

    return filtred_message
