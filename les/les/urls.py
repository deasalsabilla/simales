from django.contrib import admin
from django.urls import path
from . import views as v
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.home, name='home'),
    path('tentang-kami/', v.about, name='about'),
    path('pendaftaran/', v.daftar, name='daftar'),
    path('pembayaran/', v.bayar, name='bayar'),
    path(
    'bayar-daftar/<int:pendaftaran_id>/',
    v.bayar_daftar,
    name='bayar2'
),
    path('jadwal/', v.jadwal, name='jadwal'),
    path('login/', v.login_view , name='login'),
    path('register/', v.register, name='register'),

    path('logout/', v.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )