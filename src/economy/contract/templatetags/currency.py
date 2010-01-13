from django import template
import locale
register = template.Library()
 
@register.filter()
def currency(value, decimals=0):
    if not value:
        value = 0
    return locale.format("%%.%df" % int(decimals), value, grouping=True) # , monetary=False
