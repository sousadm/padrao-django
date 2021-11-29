from django.apps import AppConfig


class ProdutoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.produto'
    verbose_name = 'Produto'
