from django.db import models
from django.contrib.humanize.templatetags.humanize import intcomma
from datetime import date
from django.utils import timezone
from django.shortcuts import render, redirect
from decimal import Decimal

class Member(models.Model):
    ROLE_CHOICES = [
        ('peserta', 'Peserta'),
        ('pengajar', 'Pengajar'),
        ('admin', 'Admin'),
    ]

    nama = models.CharField(max_length=255, default='Anonim')
    email = models.EmailField(unique=True)
    pekerjaan = models.CharField(max_length=255, default='Mahasiswa')
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='peserta')

    def __str__(self):
        return f"{self.nama} ({self.role})"
    class Meta:
        db_table = 'main_member'  # ← ini penting agar pakai tabel yang sudah ada

class Kategori(models.Model):
    nama = models.CharField(max_length=255)

    def __str__(self):
        return self.nama

class Kursus(models.Model):
    nama = models.CharField(max_length=255)
    deskripsi = models.TextField()
    foto = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    pengajar = models.ForeignKey(Member, on_delete=models.CASCADE, limit_choices_to={'role': 'pengajar'})
    
    def format_harga_rupiah(self):
        return f"Rp{intcomma(int(self.harga))},00"

    def __str__(self):
        return self.nama

class Transaksi(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    bukti = models.ImageField(upload_to='bukti_transaksi/', null=True, blank=True)
    subscription_start_date = models.DateField(null=True, blank=True, editable=False)
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        generate_pendapatan = False

        if not is_new:
            old = Transaksi.objects.get(pk=self.pk)
            if not old.is_paid and self.is_paid:
                self.subscription_start_date = timezone.now().date()
                generate_pendapatan = True
        else:
            if self.is_paid:
                self.subscription_start_date = timezone.now().date()
                super().save(*args, **kwargs)  # Save dulu agar pk tersedia
                self._generate_pendapatan()
                return

        super().save(*args, **kwargs)

        if generate_pendapatan:
            self._generate_pendapatan()

    def _generate_pendapatan(self):
        harga = self.kursus.harga
        tanggal = timezone.now().date()

        # Jangan dobel-dobel kalau sudah ada
        if not PendapatanPengajar.objects.filter(transaksi=self).exists():
            PendapatanPengajar.objects.create(
                pengajar=self.kursus.pengajar,
                transaksi=self,
                jumlah=harga * Decimal('0.7'),
                tanggal=tanggal
            )

        if not PendapatanAdmin.objects.filter(transaksi=self).exists():
            PendapatanAdmin.objects.create(
                transaksi=self,
                jumlah=harga * Decimal('0.3'),
                tanggal=tanggal
            )

class MateriKursus(models.Model):
    TIPE_MATERI_CHOICES = [
        ('video', 'Video'),
        ('modul', 'Modul'),
    ]
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    tipe_materi = models.CharField(max_length=10, choices=TIPE_MATERI_CHOICES)
    file_url = models.FileField(upload_to='materi_files/')
    urutan = models.IntegerField()

    def __str__(self):
        return f"{self.kursus.nama} - {self.judul}"

class Rating(models.Model):
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kursus.nama} - {self.user.nama} ({self.rating})"

class PendapatanPengajar(models.Model):
    pengajar = models.ForeignKey(Member, on_delete=models.CASCADE, limit_choices_to={'role': 'pengajar'})
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal = models.DateField()

    def __str__(self):
        return f"{self.pengajar.nama} - Rp{self.jumlah}"

class PendapatanAdmin(models.Model):
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal = models.DateField()

    def __str__(self):
        return f"Admin - Rp{self.jumlah} (Transaksi #{self.transaksi.id})"

class TugasAkhir(models.Model):
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)
    judul = models.CharField(max_length=255, default='Petunjuk Tugas Akhir')
    deskripsi = models.TextField(blank=True)
    file_url = models.FileField(upload_to='tugas_akhir/')
    tanggal_dibuat = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Tugas Akhir - {self.kursus.nama}"
    
class PengumpulanTugasAkhir(models.Model):
    tugas = models.ForeignKey(TugasAkhir, on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    file_url = models.FileField(upload_to='jawaban_tugas/')
    catatan_pengajar = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('belum diperiksa', 'Belum Diperiksa'),
            ('lulus', 'Lulus'),
            ('tidak lulus', 'Tidak Lulus')
        ],
        default='belum diperiksa'
    )
    tanggal_dikumpulkan = models.DateField(auto_now_add=True)
    tanggal_dinilai = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.nama} - {self.tugas.kursus.nama}"


class Sertifikat(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)
    nomor_sertifikat = models.CharField(max_length=100)
    tanggal_diterbitkan = models.DateField()
    file_url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nomor_sertifikat} - {self.user.nama}"
    
def laporan_pengajar(request):
    pengajar_id = request.session.get('user_id')
    
    # Validasi pengajar
    if not pengajar_id:
        return redirect('login')

    # Ambil semua kursus milik pengajar
    kursus_list = Kursus.objects.filter(pengajar_id=pengajar_id)

    laporan_kursus = []
    total_pendapatan = 0
    total_peserta = 0

    for kursus in kursus_list:
        pendapatan = PendapatanPengajar.objects.filter(
            pengajar_id=pengajar_id,
            transaksi__kursus=kursus
        ).aggregate(total=sum('jumlah'))['total'] or 0

        peserta_count = Transaksi.objects.filter(
            kursus=kursus,
            is_paid='yes'
        ).count()

        total_pendapatan += pendapatan
        total_peserta += peserta_count

        laporan_kursus.append({
            'kursus': kursus,
            'pendapatan': pendapatan,
            'peserta': peserta_count
        })

    return render(request, 'main/teacher/laporan_pengajar.html', {
        'laporan_kursus': laporan_kursus,
        'total_pendapatan': total_pendapatan,
        'total_peserta': total_peserta
    })