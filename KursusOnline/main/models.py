from django.db import models

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
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    pengajar = models.ForeignKey(Member, on_delete=models.CASCADE, limit_choices_to={'role': 'pengajar'})

    def __str__(self):
        return self.nama

class Transaksi(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.CharField(max_length=10)
    bukti = models.CharField(max_length=255)
    subscription_start_date = models.DateField()
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)

    def __str__(self):
        return f"Transaksi #{self.id} - {self.user.nama}"

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
    STATUS_CHOICES = [
        ('belum dikumpulkan', 'Belum Dikumpulkan'),
        ('diperiksa', 'Diperiksa'),
        ('lulus', 'Lulus'),
        ('tidak lulus', 'Tidak Lulus'),
    ]
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)
    file_url = models.CharField(max_length=255)
    catatan_pengajar = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='belum dikumpulkan')
    tanggal_dikumpulkan = models.DateField(blank=True, null=True)
    tanggal_dinilai = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.nama} - {self.kursus.nama} - {self.status}"

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
        ).aggregate(total=Sum('jumlah'))['total'] or 0

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