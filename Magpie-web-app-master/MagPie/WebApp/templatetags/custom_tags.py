"""
To create custom tags to be used in the templates
"""
__author__ = 'webonise'

from django import template
import datetime

register = template.Library()

@register.filter()
def date_from_ms(milliseconds):
    """
    Take the milliseconds value and converts it into date time format
    """
    return datetime.datetime.fromtimestamp(milliseconds/1000).strftime('%b %d, %Y')
