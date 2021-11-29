from django import get_version
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.mail import get_connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string
from django.urls import reverse

from app import settings


def send_mail_template(subject, template_name, context, recipient_list,
                       from_mail=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
    message_html = render_to_string(template_name, context)
    message_txt = striptags(message_html)

    connection = get_connection(
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD)

    email = EmailMultiAlternatives(
        subject=subject,
        body=message_txt,
        from_email=from_mail,
        to=recipient_list,
        connection=connection
    )

    email.attach_alternative(
        message_html,
        "text/html")

    email.send(fail_silently=fail_silently)


#mostra versão do django
def version():
    print(get_version())


def config(request):
    context = {'APP_ICON_TITLE': settings.APP_ICON_TITLE}
    return context


def home(request):
    context = {}
    # template = loader.get_template('home.html')
    template = 'core/home.html'
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    # return HttpResponse(template.render(context, request))
    return render(request, 'core/home.html', {})

# def home(request):
    # return HttpResponseRedirect()
    # return render(request, 'core/home.html', {})
