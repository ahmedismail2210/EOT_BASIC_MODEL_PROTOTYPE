"""
URL configuration for reviewmodel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from webapp2 import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('properties/<int:property_id>/',
         views.review_view,
         name='property_detail'),
    path('admin/', admin.site.urls),
    # path('' , views.index ,name='home'),
    path('profile-update/', views.userUpdate, name='update_profile'),
    path('', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('reset_password/',
         auth_view.PasswordResetView.as_view(
             template_name='reset_password.html'),
         name='reset_password'),
    path('reset_password_done/',
         auth_view.PasswordResetDoneView.as_view(
             template_name='reset_password_done.html'),
         name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(
             template_name='reset_password_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_view.PasswordResetCompleteView.as_view(
             template_name='reset_password_complete.html'),
         name='password_reset_complete'),
    path('add-property/', views.createProject, name='property'),
    path('profile/', views.single_profile, name='profile'),
    path('signup/', views.registerUser, name='register'),
    path('properties/', views.projects, name='properties'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('about/', views.about, name='about')
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
