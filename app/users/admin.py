# users/admin.py
from django.contrib import admin
from .forms import UsuarioChangeForm, UsuarioCreationForm
from .models import Usuario


# Register your models here.
@admin.register(Usuario)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario
    list_display = ("email", "name", "is_active")
