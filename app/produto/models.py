import os
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import ImageField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


# Create your models here.

def get_image_path(instance, filename):
    # return os.path.join('photos', str(instance.id), filename)
    return os.path.join('photos', str(instance.id), filename)


class Categoria(models.Model):
    uuid = models.UUIDField(_("UUID"), editable=False, default=uuid.uuid4)
    origem = models.ForeignKey('Categoria', null=True, related_name='Categoria', on_delete=models.CASCADE)
    codigo = models.CharField('Código', max_length=20, blank=True, null=True)
    descricao = models.CharField('Descrição', max_length=100)
    nivel = models.IntegerField('Nível', default=1, validators=[MaxValueValidator(2), MinValueValidator(1)])
    created_dt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_dt = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_grupo = models.BooleanField('Grupo', default=False)
    is_active = models.BooleanField(_('Ativo'), default=True, )

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.descricao

    def colspan(self):
        return 5 - self.nivel

    def range(self):
        return range(self.nivel - 1)
    
    def get_absolute_url(self):
        return reverse("url_categoria_edit", kwargs={"uuid": self.uuid})

    def get_delete_url(self):
        return reverse("url_categoria_delete", kwargs={"pk": self.pk})


class Produto(models.Model):
    uuid = models.UUIDField(_("url"), editable=False, default=uuid.uuid4)
    codigo = models.CharField('Código', max_length=10, unique=True)
    descricao = models.CharField('Descrição', max_length=50)
    sobre = models.TextField('Descrição')
    image = ImageField(upload_to=get_image_path, blank=True, null=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(_('Ativo'), default=True, )
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2, default=0)
    # preco = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("produto")
        verbose_name_plural = _("produtos")
        db_table = "produto"

    def __str__(self):
        return self.descricao

    def get_absolute_url(self):
        return reverse("url_produto_edit", kwargs={"uuid": self.uuid})
