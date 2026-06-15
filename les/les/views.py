from django.shortcuts import render, redirect
from .models import PaketLes
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validasi input wajib diisi
        if not username:
            messages.error(request, 'Username wajib diisi.')
            return redirect('login')

        if not password:
            messages.error(request, 'Password wajib diisi.')
            return redirect('login')

        # Autentikasi user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(
                request,
                f'Selamat datang, {user.username}!'
            )

            return redirect('home')

        messages.error(
            request,
            'Username atau password salah.'
        )

        return redirect('login')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # Validasi username wajib diisi
        if not username:
            messages.error(request, 'Username wajib diisi.')
            return redirect('register')

        # Validasi password wajib diisi
        if not password1 or not password2:
            messages.error(request, 'Password wajib diisi.')
            return redirect('register')

        # Validasi panjang password
        if len(password1) < 8:
            messages.error(
                request,
                'Password minimal 8 karakter.'
            )
            return redirect('register')

        # Validasi konfirmasi password
        if password1 != password2:
            messages.error(
                request,
                'Konfirmasi password tidak cocok.'
            )
            return redirect('register')

        # Validasi username sudah digunakan
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                'Username sudah digunakan.'
            )
            return redirect('register')

        # Simpan user
        User.objects.create_user(
            username=username,
            password=password1
        )

        messages.success(
            request,
            'Pendaftaran berhasil. Silakan login.'
        )

        return redirect('login')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')