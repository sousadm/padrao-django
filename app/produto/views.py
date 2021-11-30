import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from app.produto.forms import CategoriaForm, ProdutoForm, CategoriaBaseForm
from app.produto.models import Categoria, Produto

sql_lista = ''' 
    SELECT
        c2.id,
        c2.nivel ,
        c2.descricao,
        c2.is_grupo 
    FROM categoria c 
    inner join categoria c2 
    on c2.origem_id = c.id  
    order by c.origem_id , c2.id
                                        '''

@login_required(login_url='login')
def categoria(request):
    return categoria_render(request, None)


@login_required(login_url='login')
def categoriaEdit(request, uuid):
    return categoria_render(request, uuid)


def produto_render(request, uuid=None):
    if uuid:
        produto = Produto.objects.get(uuid=uuid)
        form = ProdutoForm(request.POST or None, instance=produto)
    else:
        produto = Produto()
        form = ProdutoForm(request.POST or None)

    template_name = 'produto/produto_edit.html'
    try:
        if request.POST.get('btn_ativar') or request.POST.get('btn_inativar'):
            produto.is_active = not produto.is_active
            produto.save()
            return HttpResponseRedirect(reverse('url_produto_edit', kwargs={'uuid': produto.uuid}))

        if request.POST.get('btn_salvar'):
            form.save()
            return HttpResponseRedirect(reverse('url_produto_edit', kwargs={'uuid': produto.uuid}))

    except Exception as e:
        messages.error(request, e)

    context = {
        'form': form,
        'produto': produto
    }
    return render(request, template_name, context)


@login_required(login_url='login')
def produtoNew(request):
    return produto_render(request)


@login_required(login_url='login')
def produtoEdit(request, uuid=None):
    print('aki')
    return produto_render(request, uuid)


@login_required(login_url='login')
def produtoList(request):
    template_name = 'produto/produto_list.html'
    lista = Produto.objects.all()
    return render(request, template_name, {'lista': lista})


@login_required(login_url='login')
def CategoriaNew(request):
    return categoria_render(request)


def sousa(request):
    print('sousa')


def categoria_render(request, uuid=None):
    subcategoria = Categoria()
    lista = []
    if uuid:
        categoria = Categoria.objects.get(uuid=uuid)
        form = CategoriaForm(request.POST or None, instance=categoria)
        lista = Categoria.objects.raw(
            'select * from categoria where id <> origem_id and origem_id = ' + str(categoria.pk))
    else:
        categoria = Categoria()
        form = CategoriaForm(request.POST or None)

    template_name = 'produto/categoria.html'
    try:
        if request.POST.get('mybtn'):
            messages.info(request, 'aki')

        if request.POST.get('btn_ativar') or request.POST.get('btn_inativar'):
            categoria.is_active = not categoria.is_active
            categoria.save()
            return HttpResponseRedirect(reverse('url_categoria'))
            # return HttpResponseRedirect(reverse('url_categoria_edit', kwargs={'uuid': categoria.uuid}))
    #
    #     if request.POST.get('btn_aplicar'):
    #         form.save()
    #         return HttpResponseRedirect(reverse('url_categoria'))
    #
    except Exception as e:
        messages.error(request, e)

    context = {
        'form': form,
        'categoria': categoria or None,
        'subcategoria': subcategoria,
        'lista': lista
    }
    return render(request, template_name, context)




@login_required(login_url='login')
def categoriaDelete(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    try:
        categoria.delete()
        messages.success(request, 'excluido com sucesso')
    except Exception as e:
        messages.error(request, 'erro ao excluir o registro')
    return HttpResponseRedirect(reverse('url_categoria'))


@login_required(login_url='login')
def categoriaList(request):
    form_base = CategoriaBaseForm(request.POST or None, instance=Categoria())
    template_name = 'produto/categoria_list.html'
    lista = Categoria.objects.raw(sql_lista)
    try:
        if request.POST.get('grava_base'):
            c = form_base.save()
            c.origem = c
            c.save()
            form_base = CategoriaBaseForm()
            messages.success(request, 'gravado com sucesso')

    except Exception as e:
        messages.error(request, e)

    context = {
        'lista': lista,
        'form_base': form_base
    }
    return render(request, template_name, context)


@login_required(login_url='login')
def categoria_append(request, pk=None):
    template_name = 'produto/categoria_base.html'
    if pk:
        categoria = Categoria.objects.get(pk=pk)
    else:
        categoria = Categoria()
    form = CategoriaBaseForm(request.POST or None, instance=categoria)
    try:
        if request.POST:
            form.save()
            messages.success(request, 'Registro gravado com sucesso')
            return HttpResponseRedirect(reverse('url_categoria'))
    except Exception as e:
        messages.error(request, e)
    return render(request, template_name, {'form': form})



def categoria_base(request):
    try:
        base_id = request.POST.get('base_id')
        categoria = Categoria.objects.get(pk=base_id) if base_id else Categoria()
        categoria.descricao = request.POST.get('base_descricao')
        categoria.is_grupo = True
        categoria.save()
        if not categoria.origem:
            categoria = Categoria.objects.get(pk=categoria.pk)
            categoria.origem = categoria
            categoria.save()
    except Exception as e:
        messages.error(request, 'erro ao gravar o registro')
    return HttpResponseRedirect(reverse('url_categoria'))


def categoria_item(request):
    try:
        print('aki')
        item_origem_id = request.POST.get('item_origem_id')
        item_id = request.POST.get('item_id')
        is_grupo = request.POST.get('item_grupo')
        print('is_grupo', is_grupo)

        categoria = Categoria.objects.get(pk=item_id) if item_id else Categoria()
        origem = Categoria.objects.get(pk=item_origem_id) if item_origem_id else Categoria()

        categoria.descricao = request.POST.get('item_descricao')
        categoria.origem = origem
        # categoria.is_grupo = is_grupo
        categoria.save()
    except Exception as e:
        messages.error(request, 'origem_id: ' + str(2) )
    return HttpResponseRedirect(reverse('url_categoria'))
