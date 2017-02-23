from django import template


register = template.Library()


months_dict = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря',
    }


@register.filter(name="month_number_to_word")
def month_number_to_word(number):
    months = {"1": "Январь",
              "2": "Февраль",
              "3": "Март",
              "4": "Апрель",
              "5": "Май",
              "6": "Июнь",
              "7": "Июль",
              "8": "Август",
              "9": "Сентябрь",
              "10": "Октябрь",
              "11": "Ноябрь",
              "12": "Декабрь",
              }
    return months[str(number)]


@register.filter(name="translate_date")
def translate_date(date):
    year = date.year
    month = date.month
    day = date.day
    return '{} {} {}'.format(day, months_dict[month], year)


@register.filter(name='translate_date_from_text')
def translate_date_from_text(date_text):
    year, month, day = date_text.split('-')
    if day[0] == '0':
        day = day[1]
    month = int(month)
    return '{} {} {}'.format(day, months_dict[month], year)
