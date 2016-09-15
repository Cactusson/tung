from django import template


register = template.Library()


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
