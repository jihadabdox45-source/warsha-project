from modeltranslation.translator import translator, TranslationOptions
from .models import Region, RegionEvent, Craft


class RegionTranslationOptions(TranslationOptions):
    fields = ('name', 'tagline', 'brief', 'top_attraction', 'history')


class RegionEventTranslationOptions(TranslationOptions):
    fields = ('name',)


class CraftTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


translator.register(Region, RegionTranslationOptions)
translator.register(RegionEvent, RegionEventTranslationOptions)
translator.register(Craft, CraftTranslationOptions)