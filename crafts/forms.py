from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Comment, Rating


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Share your thoughts about this craft...'),
                'rows': 4
            })
        }
        labels = {
            'text': _('Your Comment')
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.RadioSelect(choices=[(i, f'{i}★') for i in range(1, 6)])
        }
        labels = {
            'stars': _('Rate this craft')
        }