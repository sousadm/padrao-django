from django import forms

from .models import Categoria, Produto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('descricao', 'origem')

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['descricao'].widget.attrs['autofocus'] = True
            self.fields['descricao'].widget.attrs['readonly'] = not instance.is_active


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['codigo'].widget.attrs['autofocus'] = True
            self.fields['preco'].widget.attrs['autofocus'] = True


class CategoriaBaseForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('descricao',)

    # def save(self, commit=True):
    #     instance = super(CategoriaBaseForm, self).save(commit=False)
    #     if commit:
    #         instance.save()
    #         obj = (Categoria) instance.save()
    #         obj.
    #         obj.save()
    #     return instance