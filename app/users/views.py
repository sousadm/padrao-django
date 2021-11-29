import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from app.core.senha import gerar_senha_letras_numeros
from app.core.views import send_mail_template
from app.users.forms import EditUsuarioForm, EditPasswordForm
from app.users.models import Usuario


@login_required(login_url='login')
def userList(request):
    context = {}
    template_name = 'users/user_list.html'
    lista = Usuario.objects.all().order_by('username')

    page = request.GET.get('page', 1)
    paginator = Paginator(lista, 10)
    try:
        lista: paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(paginator.num_pages)

    context['lista'] = lista
    return render(request, template_name, context)


@login_required(login_url='login')
def userEdit(request, uuid):
    context = {}
    template_name = 'users/user_edit.html'
    usuario = Usuario.objects.get(uuid=uuid)
    form = EditUsuarioForm(request.POST or None, instance=usuario)

    if request.method == 'POST':
        try:
            if request.POST.get('btn_ativa') or request.POST.get('btn_staff'):
                if request.POST.get('btn_ativa'):
                    usuario.is_active = not usuario.is_active

                if request.POST.get('btn_staff'):
                    usuario.is_staff = not usuario.is_staff

                usuario.save()
                return HttpResponseRedirect(reverse('url_user_edit', kwargs={'uuid': usuario.uuid}))

            if form.is_valid():
                usuario = form.save()
                messages.success(request, 'modificado com sucesso')
                return HttpResponseRedirect(reverse('url_user_edit', kwargs={'uuid': usuario.uuid}))

        except Exception as e:
            messages.error(request, e)

    context['form'] = form
    context['usuario'] = usuario
    return render(request, template_name, context)


@login_required(login_url='login')
def userRegister(request):
    context = {}
    usuario = Usuario()
    template_mail = 'users/email_password.html'
    template_name = 'users/user_edit.html'
    form = EditUsuarioForm(request.POST or None, instance=usuario)
    if request.method == 'POST':
        try:
            if form.is_valid():
                usuario = form.save()

                senha = gerar_senha_letras_numeros(6)
                hasher = PBKDF2PasswordHasher()
                salt = hasher.salt()
                usuario.password = hasher.encode(senha, salt)
                usuario.save()

                messages.success(request, 'senha enviada para e-mail')

                context_mail = {
                    'username': usuario.username,
                    'keyuser': senha,
                    'email': usuario.email,
                    'mensagem': 'Sr(a): ' + usuario.name +
                                '\n Segue senha de acesso'
                                '\n Para sua segurança, acesse o sistema e modifique sua senha',
                }
                send_mail_template(
                    'senha de acesso',
                    template_mail,
                    context_mail,
                    [usuario.email]
                )
                return HttpResponseRedirect(reverse('url_user_edit', kwargs={'uuid': usuario.uuid}))

        except Exception as e:
            messages.error(request, e)

    context['form'] = form
    context['usuario'] = usuario
    return render(request, template_name, context)


@login_required(login_url='login')
def userPassword(request):
    template_name = 'users/password.html'
    context = {}
    try:
        senha_atual = request.POST.get('senha_atual') or ''
        nova_senha = request.POST.get('nova_senha') or ''
        confirma_senha = request.POST.get('confirma_senha') or ''
        if request.method == 'POST':
            if nova_senha != confirma_senha:
                raise Exception('senha nova diferente da confirmação')
            usuario = request.user
            usuario.set_password(nova_senha)
            usuario.save()
            return HttpResponseRedirect(reverse('url_user_edit', kwargs={'uuid': usuario.uuid}))
    except Exception as e:
        messages.error(request, e)

    context['senha_atual'] = senha_atual
    context['nova_senha'] = nova_senha
    context['confirma_senha'] = confirma_senha
    return render(request, template_name, context)
