from django.db import models
from django.contrib.auth.models import User


class Jenjang(models.Model):
    nama = models.CharField(max_length=100)
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ['nama']
        verbose_name_plural = 'Jenjang'

    def __str__(self):
        return self.nama


class MataPelajaran(models.Model):
    nama = models.CharField(max_length=100)
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ['nama']
        verbose_name_plural = 'Mata Pelajaran'

    def __str__(self):
        return self.nama


class PaketLes(models.Model):
    jenjang = models.ForeignKey(
        Jenjang,
        on_delete=models.CASCADE,
        related_name='paket_les'
    )

    mata_pelajaran = models.ForeignKey(
        MataPelajaran,
        on_delete=models.CASCADE,
        related_name='paket_les'
    )

    nama_paket = models.CharField(max_length=150)

    biaya = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    deskripsi = models.TextField(
        blank=True,
        null=True
    )

    aktif = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nama_paket']
        verbose_name_plural = 'Paket Les'

    def __str__(self):
        return self.nama_paket


class Siswa(models.Model):

    JENIS_KELAMIN = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='siswa'
    )

    nama_lengkap = models.CharField(max_length=150)

    jenis_kelamin = models.CharField(
        max_length=1,
        choices=JENIS_KELAMIN
    )

    tempat_lahir = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    tanggal_lahir = models.DateField(
        blank=True,
        null=True
    )

    sekolah = models.CharField(
        max_length=150
    )

    kelas_sekolah = models.CharField(
        max_length=50
    )

    alamat = models.TextField()

    no_hp = models.CharField(
        max_length=20
    )

    no_hp_ortu = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    foto = models.ImageField(
        upload_to='siswa/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nama_lengkap']
        verbose_name_plural = 'Siswa'

    def __str__(self):
        return self.nama_lengkap


class Pendaftaran(models.Model):

    STATUS = (
        ('MENUNGGU_PEMBAYARAN', 'Menunggu Pembayaran'),
        ('MENUNGGU_VERIFIKASI', 'Menunggu Verifikasi'),
        ('AKTIF', 'Aktif'),
        ('DITOLAK', 'Ditolak'),
        ('SELESAI', 'Selesai'),
    )

    kode_pendaftaran = models.CharField(
        max_length=30,
        unique=True
    )

    siswa = models.ForeignKey(
        Siswa,
        on_delete=models.CASCADE,
        related_name='pendaftaran'
    )

    paket = models.ForeignKey(
        PaketLes,
        on_delete=models.CASCADE,
        related_name='pendaftaran'
    )

    tanggal_daftar = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default='MENUNGGU_PEMBAYARAN'
    )

    catatan = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-tanggal_daftar']
        verbose_name_plural = 'Pendaftaran'

    def __str__(self):
        return self.kode_pendaftaran


class Pembayaran(models.Model):

    pendaftaran = models.OneToOneField(
        Pendaftaran,
        on_delete=models.CASCADE,
        related_name='pembayaran'
    )

    nominal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    nama_pengirim = models.CharField(
        max_length=150
    )

    bank_pengirim = models.CharField(
        max_length=100
    )

    bukti_transfer = models.ImageField(
        upload_to='bukti_transfer/'
    )

    tanggal_upload = models.DateTimeField(
        auto_now_add=True
    )

    verified_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-tanggal_upload']
        verbose_name_plural = 'Pembayaran'

    def __str__(self):
        return self.pendaftaran.kode_pendaftaran


class Jadwal(models.Model):

    jenjang = models.ForeignKey(
        Jenjang,
        on_delete=models.CASCADE,
        related_name='jadwal'
    )

    judul = models.CharField(
        max_length=150
    )

    file_jadwal = models.FileField(
        upload_to='jadwal/'
    )

    aktif = models.BooleanField(
        default=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['judul']
        verbose_name_plural = 'Jadwal'

    def __str__(self):
        return self.judul


class Rekening(models.Model):

    nama_bank = models.CharField(
        max_length=100
    )

    nomor_rekening = models.CharField(
        max_length=50
    )

    atas_nama = models.CharField(
        max_length=150
    )

    aktif = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name_plural = 'Rekening'

    def __str__(self):
        return f'{self.nama_bank} - {self.nomor_rekening}'