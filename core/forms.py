from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_('Name'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your name'),
            'class': 'form-control'
        }),
        error_messages={
            'required': _('Please enter your name.'),
            'max_length': _('Name is too long (maximum 100 characters).')
        }
    )
    
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'placeholder': _('Enter your email'),
            'class': 'form-control'
        }),
        error_messages={
            'required': _('Please enter your email address.'),
            'invalid': _('Please enter a valid email address.')
        }
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': _('Enter your message'),
            'class': 'form-control',
            'rows': 6
        }),
        label=_('Message'),
        min_length=10,
        error_messages={
            'required': _('Please enter your message.'),
            'min_length': _('Message is too short (minimum 10 characters).')
        }
    )


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email')
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label=_('First Name'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your first name')
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label=_('Last Name'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your last name')
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Choose a username')
            }),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Choose a username')
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Enter password')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Confirm password')
        })
        self.fields['username'].label = _('Username')
        self.fields['password1'].label = _('Password')
        self.fields['password2'].label = _('Confirm Password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email is already registered'))
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your username')
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password')
        })
    )