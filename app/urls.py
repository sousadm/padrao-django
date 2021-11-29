"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from app.core.views import home
from app.produto import views
from app.users.views import userList, userRegister, userEdit, userPassword

urlpatterns = [
                  path('', home, name='home'),
                  path('admin/', admin.site.urls),
                  path('user', userList, name='url_user_list'),
                  path('login/', auth_views.LoginView.as_view(
                      redirect_authenticated_user=True,
                      template_name='users/login.html'), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(
                      template_name='core/home.html'), name='logout'),
                  path('password/', userPassword, name='url_user_password'),
                  path('user/<str:uuid>', userEdit, name='url_user_edit'),
                  path('user/add/', userRegister, name='url_user_add'),
                  path('admin/', admin.site.urls),

                  path('categoria/', views.categoriaList, name='url_categoria'),
                  path('categoria/add', views.CategoriaNew, name='url_categoria_add'),
                  path('categoria/<str:uuid>', views.categoriaEdit, name='url_categoria_edit'),
                  path('categoria/base/', views.categoria_base, name='url_categoria_base'),
                  path('categoria/item/', views.categoria_item, name='url_categoria_item'),
                  path('categoria/<int:pk>/delete', views.categoriaDelete, name='url_categoria_delete'),
                  path('produto/', views.produtoList, name='url_produto_list'),
                  path('produto/add', views.produtoNew, name='url_produto_add'),
                  path('produto/<str:uuid>', views.produtoEdit, name='url_produto_edit'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
