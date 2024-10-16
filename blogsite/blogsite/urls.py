"""blogsite URL Configuration

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
import os
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.views.generic import TemplateView
from django.conf.urls.static import static
from blog.sitemaps import PostSitemap

sitemaps = {
     'posts': PostSitemap,
}

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),  # for development only
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),  # include the urls from the blog app
    path('home/', include('home.urls')),  # include the urls from the home app
    path('accounts/', include('django.contrib.auth.urls')),  #django auth urls
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),  #social auth urls

    path('', TemplateView.as_view(template_name='home/main.html')),  # home page
    
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    )
]


# media files to serve in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve the static HTML
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns += [
    re_path(r'^site/(?P<path>.*)$', serve,
        {'document_root': os.path.join(BASE_DIR, 'site'),
         'show_indexes': True},
        name='site_path'
        ),
]


# Serve the favicon 
urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'home/static'),
        }
    ),
]

# Switch to social login if it is configured 
# Set the login template for social login
social_login = 'registration/login_social.html'
urlpatterns.insert(0,
                   path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                   )
print('Using', social_login, 'as the login template')
