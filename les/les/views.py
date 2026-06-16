from django.shortcuts import render, redirect, get_object_or_404
from .models import PaketLes, Siswa, Pendaftaran, Rekening, Pembayaran, Jadwal
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def home(request):
    paket_les = PaketLes.objects.filter(aktif=True)

    context = {
        'paket_les': paket_les
    }

    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def daftar(request):
    paket_les = PaketLes.objects.filter(aktif=True)

    if request.method == 'POST':
        paket = get_object_or_404(
            PaketLes,
            id=request.POST.get('paket'),
            aktif=True
        )

        siswa, created = Siswa.objects.get_or_create(
            user=request.user,
            defaults={
                'nama_lengkap': request.POST.get('nama_lengkap'),
                'jenis_kelamin': request.POST.get('jenis_kelamin'),
                'tempat_lahir': request.POST.get('tempat_lahir'),
                'tanggal_lahir': request.POST.get('tanggal_lahir') or None,
                'sekolah': request.POST.get('sekolah'),
                'kelas_sekolah': request.POST.get('kelas_sekolah'),
                'alamat': request.POST.get('alamat'),
                'no_hp': request.POST.get('no_hp'),
                'no_hp_ortu': request.POST.get('no_hp_ortu'),
            }
        )

        # Jika data siswa sudah ada, update datanya
        if not created:
            siswa.nama_lengkap = request.POST.get('nama_lengkap')
            siswa.jenis_kelamin = request.POST.get('jenis_kelamin')
            siswa.tempat_lahir = request.POST.get('tempat_lahir')
            siswa.tanggal_lahir = request.POST.get('tanggal_lahir') or None
            siswa.sekolah = request.POST.get('sekolah')
            siswa.kelas_sekolah = request.POST.get('kelas_sekolah')
            siswa.alamat = request.POST.get('alamat')
            siswa.no_hp = request.POST.get('no_hp')
            siswa.no_hp_ortu = request.POST.get('no_hp_ortu')
            siswa.save()

        # Cek apakah sudah pernah mendaftar paket yang sama
        sudah_terdaftar = Pendaftaran.objects.filter(
            siswa=siswa,
            paket=paket
        ).exclude(status='DITOLAK').exists()

        if sudah_terdaftar:
            messages.warning(
                request,
                'Anda sudah terdaftar pada paket les ini.'
            )
            return redirect('daftar')

        # Generate kode pendaftaran
        while True:
            kode = f"LES-{random.randint(100000, 999999)}"

            if not Pendaftaran.objects.filter(
                kode_pendaftaran=kode
            ).exists():
                break

        pendaftaran = Pendaftaran.objects.create(
            kode_pendaftaran=kode,
            siswa=siswa,
            paket=paket
        )

        messages.success(
            request,
            'Pendaftaran berhasil dilakukan.'
        )

        return redirect(
    'bayar2',
    pendaftaran_id=pendaftaran.id
)

    context = {
        'paket_les': paket_les
    }

    return render(request, 'daftar.html', context)

@login_required(login_url='login')
def bayar_daftar(request, pendaftaran_id):

    pendaftaran = get_object_or_404(
        Pendaftaran,
        id=pendaftaran_id,
        siswa__user=request.user
    )

    rekening_list = Rekening.objects.filter(
        aktif=True
    )

    if request.method == 'POST':

        # Cek apakah sudah pernah upload pembayaran
        if hasattr(pendaftaran, 'pembayaran'):
            messages.warning(
                request,
                'Bukti pembayaran sudah pernah dikirim.'
            )
            return redirect(
                'bayar2',
                pendaftaran_id=pendaftaran.id
            )

        bukti_transfer = request.FILES.get(
            'bukti_transfer'
        )

        if not bukti_transfer:
            messages.error(
                request,
                'Bukti transfer wajib diupload.'
            )
            return redirect(
                'bayar2',
                pendaftaran_id=pendaftaran.id
            )

        Pembayaran.objects.create(
            pendaftaran=pendaftaran,
            nominal=300000,
            nama_pengirim=request.POST.get(
                'nama_pengirim'
            ),
            bank_pengirim=request.POST.get(
                'bank_pengirim'
            ),
            bukti_transfer=bukti_transfer
        )

        pendaftaran.status = 'MENUNGGU_VERIFIKASI'
        pendaftaran.save()

        messages.success(
            request,
            'Bukti pembayaran berhasil dikirim.'
        )

        return redirect(
            'bayar2',
            pendaftaran_id=pendaftaran.id
        )

    context = {
        'pendaftaran': pendaftaran,
        'rekening_list': rekening_list,
    }

    return render(
        request,
        'bayar2.html',
        context
    )

def bayar(request):
    rekening_list = Rekening.objects.filter(
        aktif=True
    ).order_by('nama_bank')

    context = {
        'rekening_list': rekening_list,
        'nominal': 300000,
    }

    return render(request, 'bayar.html', context)

@login_required
def jadwal(request):

    if not hasattr(request.user, 'siswa'):
        return render(
            request,
            'jadwal.html',
            {
                'jadwal_list': []
            }
        )

    siswa = request.user.siswa

    jadwal_list = Jadwal.objects.filter(
        aktif=True,
        jenjang__paket_les__pendaftaran__siswa=siswa,
        jenjang__paket_les__pendaftaran__status='AKTIF'
    ).distinct()

    return render(
        request,
        'jadwal.html',
        {
            'jadwal_list': jadwal_list
        }
    )

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

def kontak(request):
    return render(request, 'kontak.html')

@login_required
def les_saya(request):
    try:
        siswa = request.user.siswa

        pendaftaran_list = Pendaftaran.objects.filter(
            siswa=siswa
        ).select_related(
            'paket',
            'paket__jenjang',
            'paket__mata_pelajaran'
        )

    except:
        pendaftaran_list = []

    context = {
        'pendaftaran_list': pendaftaran_list
    }

    return render(request, 'les_saya.html', context)