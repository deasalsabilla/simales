from django.shortcuts import render
from .models import PaketLes

def home(request):
    paket_les = PaketLes.objects.filter(aktif=True)

    context = {
        'paket_les': paket_les
    }

    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def daftar(request):
    return render(request, 'daftar.html')

def bayar(request):
    return render(request, 'bayar.html')

def jadwal(request):
    return render(request, 'jadwal.html')