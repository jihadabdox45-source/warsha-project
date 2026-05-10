from django import template
from django.utils import translation

register = template.Library()


@register.simple_tag
def current_language():
    return translation.get_language()


@register.simple_tag
def is_arabic():
    return translation.get_language() == 'ar'


@register.filter
def get_translated_field(obj, field_name):
    current_lang = translation.get_language()
    
    if current_lang == 'ar':
        translated_field = f"{field_name}_ar"
        if hasattr(obj, translated_field):
            translated_value = getattr(obj, translated_field)
            if translated_value:
                return translated_value
    
    return getattr(obj, field_name, '')


@register.simple_tag
def get_field_by_language(obj, field_name, language=None):
    if language is None:
        language = translation.get_language()
    
    if language == 'ar':
        translated_field = f"{field_name}_ar"
        if hasattr(obj, translated_field):
            translated_value = getattr(obj, translated_field)
            if translated_value:
                return translated_value
    
    return getattr(obj, field_name, '')