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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('profile-update/', views.userUpdate, name='update_profile'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('add-property/', views.createProject, name='property'),
    path('profile/', views.single_profile, name='profile'),
    path('signup/', views.registerUser, name='register'),
    path('properties/<slug:property_id>/',
         views.review_view,
         name='property_detail'),
    path('properties/', views.projects, name='properties'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
