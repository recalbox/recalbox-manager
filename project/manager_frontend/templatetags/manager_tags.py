from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    """
    Very simple template filter to be able to easily get an item from 'dictionnary' using given 'key'
    
    Usage:
    
        {{ mydict|get_item:'foo' }}
    """
    return dictionary.get(key)