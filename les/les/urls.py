from django.contrib import admin
from django.urls import path
from . import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.home, name='home'),
    path('tentang-kami/', v.about, name='about'),
    path('pendaftaran/', v.daftar, name='daftar'),
]
