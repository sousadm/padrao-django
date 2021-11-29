# users/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = (
            "username",
            "email",
        )


class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = "__all__"


class EditUsuarioForm(forms.ModelForm):
    user_log = get_user_model()

    class Meta:
        model = Usuario
        fields = ['email', 'celular', 'username', 'first_name', 'last_name', 'is_consulta', 'is_staff']

    def __init__(self, *args, **kwargs):
        super(EditUsuarioForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            if instance.id:
                self.fields['username'].widget.attrs['readonly'] = True
                self.fields['email'].widget.attrs['autofocus'] = True
            else:
                self.fields['username'].widget.attrs['autofocus'] = True


class EditPasswordForm(forms.Form):
    atual = forms.CharField(widget=forms.PasswordInput, label='Senha atual')
    nova = forms.CharField(widget=forms.PasswordInput, label='Nova senha')
    confirma = forms.CharField(widget=forms.PasswordInput, label='Confirma senha')
