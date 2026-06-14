from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    Jenjang,
    MataPelajaran,
    PaketLes,
    Siswa,
    Pendaftaran,
    Pembayaran,
    Jadwal,
    Rekening,
)

@admin.register(Jenjang)
class JenjangAdmin(ModelAdmin):
    list_display = ("nama", "aktif")
    list_filter = ("aktif",)
    search_fields = ("nama",)

    search_help_text = "Cari nama jenjang"

@admin.register(MataPelajaran)
class MataPelajaranAdmin(ModelAdmin):
    list_display = ("nama", "aktif")
    list_filter = ("aktif",)
    search_fields = ("nama",)

    search_help_text = "Cari mata pelajaran"

@admin.register(PaketLes)
class PaketLesAdmin(ModelAdmin):
    list_display = (
        "nama_paket",
        "jenjang",
        "mata_pelajaran",
        "biaya",
        "aktif",
    )

    list_filter = (
        "jenjang",
        "mata_pelajaran",
        "aktif",
    )

    search_fields = (
        "nama_paket",
        "jenjang__nama",
        "mata_pelajaran__nama",
    )

    autocomplete_fields = (
        "jenjang",
        "mata_pelajaran",
    )

    list_filter_submit = True

@admin.register(Siswa)
class SiswaAdmin(ModelAdmin):
    list_display = (
        "nama_lengkap",
        "sekolah",
        "kelas_sekolah",
        "no_hp",
        "created_at",
    )

    search_fields = (
        "nama_lengkap",
        "sekolah",
        "no_hp",
        "no_hp_ortu",
    )

    list_filter = (
        "jenis_kelamin",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Data Siswa",
            {
                "fields": (
                    "nama_lengkap",
                    "jenis_kelamin",
                    "tanggal_lahir",
                )
            },
        ),
        (
            "Data Sekolah",
            {
                "fields": (
                    "sekolah",
                    "kelas_sekolah",
                )
            },
        ),
        (
            "Kontak",
            {
                "fields": (
                    "no_hp",
                    "no_hp_ortu",
                    "alamat",
                )
            },
        ),
        (
            "Informasi Sistem",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

@admin.register(Pendaftaran)
class PendaftaranAdmin(ModelAdmin):
    list_display = (
        "kode_pendaftaran",
        "siswa",
        "paket",
        "status",
        "tanggal_daftar",
    )

    list_filter = (
        "status",
        "tanggal_daftar",
    )

    search_fields = (
        "kode_pendaftaran",
        "siswa__nama_lengkap",
        "siswa__no_hp",
    )

    autocomplete_fields = (
        "siswa",
        "paket",
    )

    readonly_fields = (
        "tanggal_daftar",
    )

    list_per_page = 25

    list_filter_submit = True

@admin.register(Pembayaran)
class PembayaranAdmin(ModelAdmin):
    list_display = (
        "pendaftaran",
        "nama_pengirim",
        "bank_pengirim",
        "nominal",
        "tanggal_upload",
        "verified_at",
    )

    search_fields = (
        "pendaftaran__kode_pendaftaran",
        "nama_pengirim",
        "bank_pengirim",
    )

    list_filter = (
        "bank_pengirim",
        "tanggal_upload",
    )

    autocomplete_fields = (
        "pendaftaran",
    )

    readonly_fields = (
        "tanggal_upload",
    )

    list_filter_submit = True

@admin.register(Jadwal)
class JadwalAdmin(ModelAdmin):
    list_display = (
        "judul",
        "jenjang",
        "aktif",
        "uploaded_at",
    )

    search_fields = (
        "judul",
        "jenjang__nama",
    )

    list_filter = (
        "jenjang",
        "aktif",
    )

    autocomplete_fields = (
        "jenjang",
    )

    readonly_fields = (
        "uploaded_at",
    )

    fieldsets = (
        (
            "Informasi Jadwal",
            {
                "fields": (
                    "jenjang",
                    "judul",
                    "file_jadwal",
                    "aktif",
                )
            },
        ),
        (
            "Informasi Sistem",
            {
                "fields": (
                    "uploaded_at",
                )
            },
        ),
    )

@admin.register(Rekening)
class RekeningAdmin(ModelAdmin):
    list_display = (
        "nama_bank",
        "nomor_rekening",
        "atas_nama",
        "aktif",
    )

    search_fields = (
        "nama_bank",
        "nomor_rekening",
        "atas_nama",
    )

    list_filter = (
        "aktif",
    )

    list_filter_submit = True