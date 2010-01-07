from django import template
import locale
locale.setlocale(locale.LC_ALL, 'no_NO')
register = template.Library()
 
@register.filter()
def currency(value, decimals=0):
    if not value:
        value = 0
    return locale.format("%%.%df" % int(decimals), value, grouping=True) # , monetary=False
