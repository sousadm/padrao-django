import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Usuario(AbstractUser):
    uuid = models.UUIDField(_("User UUID"), editable=False, default=uuid.uuid4)
    username = models.CharField('Usuário', max_length=30, unique=True)
    first_name = models.CharField(_('Nome'), max_length=150, blank=True)
    last_name = models.CharField(_('Sobrenome'), max_length=150, blank=True)
    celular = models.CharField('Celular', max_length=20, null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
    is_consulta = models.BooleanField('Consulta', blank=True, default=False)
    is_staff = models.BooleanField(_('Administrador'), default=False)
    is_active = models.BooleanField(_('Ativo'), default=True,)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = _("usuario")
        verbose_name_plural = _("usuarios")
        db_table = "usuario"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("url_user_edit", kwargs={"uuid": self.uuid})
