from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminLoginForm
from .models import Member, Kursus, Transaksi, PendapatanAdmin, PendapatanPengajar, Rating, MateriKursus, TugasAkhir, Kategori, PengumpulanTugasAkhir
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .forms import UserLoginForm
from .forms import MateriForm
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
import requests
from django.contrib.humanize.templatetags.humanize import intcomma
from django.conf import settings
from .forms import DummyMateriForm
from decimal import Decimal
from main.forms import PengumpulanTugasAkhirForm
from .forms import RatingForm
from main.models import Sertifikat
from main.forms import RegisterPesertaForm
from django.contrib.auth.hashers import make_password

# Create your views here.
def home(request):
    context={}
    return render(request, "main/home.html", context)
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = Member.objects.get(email=email)

                if user.role not in ['peserta', 'pengajar']:
                    messages.error(request, 'Akun Anda tidak diizinkan mengakses halaman ini.')
                    return redirect('login_user')

                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['user_nama'] = user.nama
                    request.session['user_role'] = user.role
                    
                    if user.role == 'peserta':
                        return redirect('peserta_dashboard')
                    elif user.role == 'pengajar':
                        return redirect('dashboard_pengajar')
                else:
                    messages.error(request, 'Password salah.')
            except Member.DoesNotExist:
                messages.error(request, 'Email tidak ditemukan.')
    else:
        form = UserLoginForm()

    return render(request, 'main/login.html', {'form': form})
def course(request):
    context={}
    return render(request, "main/course.html", context)
def about(request):
    context={}
    return render(request, "main/about.html", context)
def contact(request):
    context={}
    return render(request, "main/contact.html", context)
def mycourse_student(request):
    if request.session.get('user_role') != 'peserta':
        return redirect('login')

    peserta_id = request.session.get('user_id')

    kursus_ids = Transaksi.objects.filter(
        user_id=peserta_id, is_paid=True
    ).values_list('kursus_id', flat=True)

    enrolled_courses = Kursus.objects.filter(
        id__in=kursus_ids
    ).select_related('kategori')

    context = {
        'enrolled_courses': enrolled_courses,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'main/student/mycourse.html', context)

from django.contrib.auth.hashers import check_password


# Bagian Admin

def login_admin(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                admin_user = Member.objects.get(email=email, role='admin')

                if check_password(password, admin_user.password):
                    request.session['admin_id'] = admin_user.id
                    request.session['admin_nama'] = admin_user.nama
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Password salah.')
            except Member.DoesNotExist:
                messages.error(request, 'Email tidak ditemukan atau Anda bukan admin.')
    else:
        form = AdminLoginForm()

    return render(request, 'main/admin/login.html', {'form': form})


def admin_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')

    total_users = Member.objects.count()
    total_kursus = Kursus.objects.count()
    total_pendapatan_admin = PendapatanAdmin.objects.aggregate(Sum('jumlah'))['jumlah__sum'] or 0
    transaksi_terbaru = Transaksi.objects.select_related('user', 'kursus').order_by('-id')[:5]

    context = {
        'total_users': total_users,
        'total_kursus': total_kursus,
        'total_pendapatan_admin': total_pendapatan_admin,
        'transaksi_terbaru': transaksi_terbaru,
    }
    return render(request, 'main/admin/dashboard.html', context)

def logout_admin(request):
    request.session.flush()
    return redirect('admin_login')

def manage_user(request):
    response = requests.get('http://127.0.0.1:8000/api/members/')
    data = response.json()
    return render(request, 'main/admin/manageuser.html', {'manage_user': data})
    
def add_user(request):
    if request.method == 'POST':
        payload = {
            "nama": request.POST['nama'],
            "email": request.POST['email'],
            "password": request.POST['password'],
            "pekerjaan": request.POST['pekerjaan'],
            "role": request.POST['role'],
            
        }
        response = requests.post('http://127.0.0.1:8000/api/members/', data=payload)

        if response.status_code in [200, 201]:
            return redirect('manage_user')
        else:
            response_data = response.json() if response.content else {}
            error_message = response_data.get('detail', 'Gagal menambahkan user.')
            return render(request, 'main/admin/manageuser.html', {
                'manage_user': requests.get('http://127.0.0.1:8000/api/members/').json(),
                'error_message': error_message
            })

def edit_user(request, id):
    if request.method == 'POST':
        payload = {
            "nama": request.POST['nama'],
            "email": request.POST['email'],
            "pekerjaan": request.POST['pekerjaan'],
            "role": request.POST['role']
        }

        if request.POST.get('password'):
            payload['password'] = request.POST['password']

        response = requests.put(f"http://127.0.0.1:8000/api/members/{id}/", json=payload)

        if response.status_code in [200, 204]:
            return redirect('manage_user')
        else:
            print("API Error:", response.status_code, response.text)  # Debug
            print("Response Content:", response.text)  # <-- print isi errornya di sini
            response_data = response.json() if response.content else {}
            error_message = response_data.get('detail', 'Gagal mengedit user.')
            return render(request, 'main/admin/manageuser.html', {
                'manage_user': requests.get('http://127.0.0.1:8000/api/members/').json(),
                'error_message': error_message
            })

def delete_user(request, id):
    requests.delete(f'http://127.0.0.1:8000/api/members/{id}/')
    return redirect('manage_user')

def transaksi(request):
    response = requests.get('http://127.0.0.1:8000/api/transaksi/')
    data = response.json()
    return render(request, 'main/admin/transaksi.html', {'transaksi': data})

# Bagian Pengajar

def dashboard_pengajar(request):
    if request.session.get('user_role') != 'pengajar':
        return redirect('login_user')

    pengajar_id = request.session.get('user_id')
    pengajar_nama = request.session.get('user_nama')

    kursus_resp = requests.get(f'http://127.0.0.1:8000/api/kursus/?pengajar={pengajar_id}')
    kursus_list = kursus_resp.json() if kursus_resp.status_code == 200 else []
    total_kursus = len(kursus_list)

    # Ambil semua transaksi yang dibayar untuk semua kursus
    total_pendapatan = 0
    for kursus in kursus_list:
        transaksi_resp = requests.get('http://127.0.0.1:8000/api/transaksi/', params={
            'kursus': kursus['id'],
            'is_paid': 'true'
        })
        transaksi_list = transaksi_resp.json() if transaksi_resp.status_code == 200 else []

        for transaksi in transaksi_list:
            pendapatan_resp = requests.get('http://127.0.0.1:8000/api/pendapatan-pengajar/', params={
                'pengajar': pengajar_id,
                'transaksi': transaksi['id']
            })
            pendapatan_list = pendapatan_resp.json() if pendapatan_resp.status_code == 200 else []
            for p in pendapatan_list:
                total_pendapatan += float(p['jumlah'])

    # Rating rata-rata
    rating_resp = requests.get(f'http://127.0.0.1:8000/api/rating/')
    rating_list = rating_resp.json() if rating_resp.status_code == 200 else []
    rating_filtered = [r['rating'] for r in rating_list if r['kursus'] in [k['id'] for k in kursus_list]]
    rating_avg = round(sum(rating_filtered) / len(rating_filtered), 2) if rating_filtered else 0

    context = {
        'pengajar_nama': pengajar_nama,
        'total_kursus': total_kursus,
        'total_pendapatan': total_pendapatan,
        'rating_avg': rating_avg,
    }

    return render(request, 'main/teacher/dashboard.html', context)

def kursus_saya_pengajar(request):
    if request.session.get('user_role') != 'pengajar':
        return redirect('login_user')

    pengajar_id = request.session.get('user_id')
    pengajar_nama = request.session.get('user_nama')

    response = requests.get(f'http://127.0.0.1:8000/api/kursus/?pengajar={pengajar_id}')
    kursus_list = response.json() if response.status_code == 200 else []

    context = {
        'pengajar_nama': pengajar_nama,
        'kursus_list': kursus_list,
        'foto_url_prefix': settings.MEDIA_URL,
    }

    return render(request, 'main/teacher/kursus_saya.html', context)

def detail_kursus_pengajar(request, kursus_id):
    if request.session.get('user_role') != 'pengajar':
        return redirect('login_user')

    # Ambil kursus dari API
    kursus_resp = requests.get(f'http://127.0.0.1:8000/api/kursus/{kursus_id}/')
    if kursus_resp.status_code != 200:
        return redirect('kursus_saya_pengajar')
    kursus = kursus_resp.json()

    if kursus['pengajar'] != request.session.get('user_id'):
        return redirect('kursus_saya_pengajar')

    # Materi via API
    materi_resp = requests.get(f'http://127.0.0.1:8000/api/materi/?kursus={kursus_id}')
    materi_list = materi_resp.json() if materi_resp.status_code == 200 else []
    materi_list.sort(key=lambda x: x['urutan'])

    # Tugas akhir via API
    tugas_resp = requests.get(f'http://127.0.0.1:8000/api/tugas-akhir/?kursus={kursus_id}')
    tugas_list = tugas_resp.json() if tugas_resp.status_code == 200 else []
    tugas_list.sort(key=lambda x: x['tanggal_dibuat'], reverse=True)

    return render(request, 'main/teacher/detail_kursus.html', {
        'kursus': kursus,
        'materi_list': materi_list,
        'tugas_akhir_list': tugas_list,
        'MEDIA_URL': settings.MEDIA_URL,
    })


# student
def dashboard_student(request):
    if request.session.get('user_role') != 'peserta':
        return redirect('login')

    peserta_id = request.session.get('user_id')
    peserta_nama = request.session.get('user_nama')

    # Ambil ID kursus yang sudah diikuti oleh peserta
    kursus_diikuti_ids = Transaksi.objects.filter(
    user_id=peserta_id,
    is_paid=True
    ).values_list('kursus_id', flat=True)


    # Total kursus diikuti
    total_kursus_diikuti = len(kursus_diikuti_ids)

    # Kursus yang belum diikuti (bisa di-enroll)
    semua_kursus = Kursus.objects.exclude(id__in=kursus_diikuti_ids).select_related('kategori')

    # Kategori dari semua kursus
    semua_kategori = Kategori.objects.filter(kursus__in=semua_kursus).distinct()

    # Rata-rata rating yang diberikan peserta
    rating_diberikan = Rating.objects.filter(user_id=peserta_id).aggregate(avg=Avg('rating'))['avg'] or 0
    rating_diberikan = round(rating_diberikan, 2)

    context = {
        'peserta_nama': peserta_nama,
        'total_kursus_diikuti': total_kursus_diikuti,
        'rating_diberikan': rating_diberikan,
        'semua_kursus': semua_kursus,
        'semua_kategori': semua_kategori,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'main/student/dashboard.html', context)

def transaksi_peserta(request):
    if request.session.get('user_role') != 'peserta':
        return redirect('login')

    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        telepon = request.POST.get('telepon')
        metode = request.POST.get('metode')
        bukti = request.FILES.get('bukti')  # Optional
        
        peserta_id = request.session.get('user_id')
        kursus_id = request.GET.get('kursus_id')  # Asumsikan id kursus dikirim via URL

        try:
            kursus = Kursus.objects.get(id=kursus_id)
        except Kursus.DoesNotExist:
            return render(request, 'main/student/transaksi_peserta.html', {
                'error': 'Kursus tidak ditemukan.'
            })

        transaksi = Transaksi.objects.create(
            user_id=peserta_id,
            kursus=kursus,
            total_harga=kursus.harga,
            subscription_start_date=timezone.now(),
            is_paid=False,  # default belum lunas
            bukti=bukti,
        )

        return redirect('transaksi_berhasil')  # ganti dengan nama url yang sesuai

    # Untuk metode GET, hanya tampilkan form pembelian
    return render(request, 'main/student/transaksi_peserta.html', {
        'peserta_nama': request.session.get('user_nama')
    })
def tambah_materi(request, kursus_id):
    pengajar_id = request.session.get('user_id')

    kursus_resp = requests.get(f"http://127.0.0.1:8000/api/kursus/{kursus_id}/")
    if kursus_resp.status_code != 200 or kursus_resp.json()['pengajar'] != pengajar_id:
        return redirect('kursus_saya_pengajar')
    kursus = kursus_resp.json()

    if request.method == 'POST':
        payload = {
            'judul': request.POST['judul'],
            'deskripsi': request.POST['deskripsi'],
            'tipe_materi': request.POST['tipe_materi'],
            'urutan': request.POST['urutan'],
            'kursus': kursus_id
        }
        files = {'file_url': request.FILES['file_url']} if request.FILES.get('file_url') else None

        response = requests.post(
            "http://127.0.0.1:8000/api/materi/",
            data=payload,
            files=files
        )
        if response.status_code in [200, 201]:
            return redirect('detail_kursus_pengajar', kursus_id=kursus_id)

    form = DummyMateriForm()
    return render(request, 'main/teacher/form_materi.html', {
        'kursus': kursus,
        'mode': 'Tambah',
        'form': form,
    })

def edit_materi(request, pk):
    pengajar_id = request.session.get('user_id')

    # Ambil data materi
    materi_resp = requests.get(f'http://127.0.0.1:8000/api/materi/{pk}/')
    if materi_resp.status_code != 200:
        return redirect('kursus_saya_pengajar')
    materi = materi_resp.json()

    # Ambil kursus dan pastikan pemilik
    kursus_resp = requests.get(f"http://127.0.0.1:8000/api/kursus/{materi['kursus']}/")
    if kursus_resp.status_code != 200 or kursus_resp.json()['pengajar'] != pengajar_id:
        return redirect('kursus_saya_pengajar')

    kursus = kursus_resp.json()

    # POST: proses update data
    if request.method == 'POST':
        form = DummyMateriForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            payload = {
                'judul': data['judul'],
                'deskripsi': data['deskripsi'],
                'tipe_materi': data['tipe_materi'],
                'urutan': data['urutan'],
                'kursus': kursus['id'],
            }
            files = {'file_url': request.FILES['file_url']} if 'file_url' in request.FILES else None

            response = requests.put(
                f"http://127.0.0.1:8000/api/materi/{pk}/", data=payload, files=files
            )
            if response.status_code in [200, 204]:
                return redirect('detail_kursus_pengajar', kursus_id=kursus['id'])
    else:
        # GET: tampilkan form dengan data awal
        form = DummyMateriForm(initial={
            'judul': materi.get('judul'),
            'deskripsi': materi.get('deskripsi'),
            'tipe_materi': materi.get('tipe_materi'),
            'urutan': materi.get('urutan'),
        })

    return render(request, 'main/teacher/form_materi.html', {
        'kursus': kursus,
        'mode': 'Edit',
        'materi': materi,
        'form': form,
    })


def hapus_materi(request, pk):
    # Ambil materi dari API untuk verifikasi pemilik kursus
    materi_resp = requests.get(f"http://127.0.0.1:8000/api/materi/{pk}/")
    if materi_resp.status_code != 200:
        return redirect('kursus_saya_pengajar')
    materi = materi_resp.json()

    kursus_id = materi['kursus']

    kursus_resp = requests.get(f"http://127.0.0.1:8000/api/kursus/{kursus_id}/")
    if kursus_resp.status_code != 200 or kursus_resp.json()['pengajar'] != request.session.get('user_id'):
        return redirect('kursus_saya_pengajar')

    # Hapus
    requests.delete(f"http://127.0.0.1:8000/api/materi/{pk}/")

    return redirect('detail_kursus_pengajar', kursus_id=kursus_id)

def daftar_peserta(request, kursus_id):
    pengajar_id = request.session.get('user_id')

    # Ambil data kursus
    kursus_resp = requests.get(f"http://127.0.0.1:8000/api/kursus/{kursus_id}/")
    if kursus_resp.status_code != 200 or kursus_resp.json()['pengajar'] != pengajar_id:
        return redirect('kursus_saya_pengajar')

    kursus = kursus_resp.json()

    # Ambil semua transaksi yang sudah dibayar
    transaksi_resp = requests.get('http://127.0.0.1:8000/api/transaksi/', params={
        'kursus': kursus_id,
        'is_paid': 'yes'
    })

    peserta_transaksi = transaksi_resp.json() if transaksi_resp.status_code == 200 else []

    return render(request, 'main/teacher/daftar_peserta.html', {
        'kursus': kursus,
        'peserta_transaksi': peserta_transaksi
    })
def lihat_ulasan(request, kursus_id):
    pengajar_id = request.session.get('user_id')

    kursus_resp = requests.get(f"http://127.0.0.1:8000/api/kursus/{kursus_id}/")
    if kursus_resp.status_code != 200 or kursus_resp.json()['pengajar'] != pengajar_id:
        return redirect('kursus_saya_pengajar')

    kursus = kursus_resp.json()

    # Ambil ulasan berdasarkan kursus
    ulasan_resp = requests.get('http://127.0.0.1:8000/api/rating/', params={'kursus': kursus_id})
    ulasan_list = ulasan_resp.json() if ulasan_resp.status_code == 200 else []

    return render(request, 'main/teacher/ulasan_kursus.html', {
        'kursus': kursus,
        'ulasan_list': ulasan_list
    })
def laporan_pengajar(request):
    pengajar_id = request.session.get('user_id')
    if not pengajar_id:
        return redirect('login_user')

    kursus_resp = requests.get('http://127.0.0.1:8000/api/kursus/', params={'pengajar': pengajar_id})
    kursus_list = kursus_resp.json() if kursus_resp.status_code == 200 else []

    laporan_kursus = []
    total_pendapatan = 0
    total_peserta = 0

    for kursus in kursus_list:
        kursus_id = kursus['id']

        # Hitung pendapatan pengajar dari API
        pendapatan_resp = requests.get('http://127.0.0.1:8000/api/pendapatan-pengajar/', params={
            'pengajar': pengajar_id,
            'transaksi__kursus': kursus_id
        })
        pendapatan_list = pendapatan_resp.json() if pendapatan_resp.status_code == 200 else []
        pendapatan = sum(Decimal(p['jumlah']) for p in pendapatan_list)

        # Hitung jumlah peserta
        peserta_resp = requests.get('http://127.0.0.1:8000/api/transaksi/', params={
            'kursus': kursus_id,
            'is_paid': 'yes'
        })
        peserta_count = len(peserta_resp.json()) if peserta_resp.status_code == 200 else 0

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

def logout(request):
    request.session.flush()
    return redirect('login')

def certificate_view(request):
    if request.session.get('user_role') != 'peserta':
        return redirect('login')  # Hanya peserta yang bisa akses

    peserta_nama = request.session.get('user_nama')

    # Untuk sekarang hardcode dulu datanya
    context = {
        'participant_name': peserta_nama,
        'course_name': "Intro to Web Development",
        'completion_date': "June 11, 2025",
        'instructor_name': "Ms. Nora Lecturer",
        'certificate_number': "WD-2025-00123",
        'platform_name': "KursusOnline"
    }

    return render(request, 'main/student/certificate.html', context)

from main.models import TugasAkhir  # pastikan sudah di-import

def detail_kursus_peserta(request, kursus_id):
    if request.session.get('user_role') != 'peserta':
        return redirect('login')

    kursus = get_object_or_404(Kursus, id=kursus_id)
    peserta_id = request.session.get('user_id')

    is_paid = Transaksi.objects.filter(
        user_id=peserta_id,
        kursus=kursus,
        is_paid=True
    ).exists()

    if is_paid:
        materi_list = MateriKursus.objects.filter(kursus=kursus).order_by('urutan')
    else:
        materi_list = MateriKursus.objects.filter(kursus=kursus, urutan__lte=3).order_by('urutan')

    tugas_akhir_list = TugasAkhir.objects.filter(kursus=kursus)
    ulasan_list = Rating.objects.filter(kursus=kursus).order_by('-created_at')

    return render(request, 'main/student/detail_kursus_peserta.html', {
        'kursus': kursus,
        'materi_list': materi_list,
        'tugas_akhir_list': tugas_akhir_list,
        'is_paid': is_paid,
        'ulasan_list': ulasan_list,
    })

def tambah_tugas_akhir(request, kursus_id):
    pengajar_id = request.session.get('user_id')

    kursus_resp = requests.get(f"http://127.0.0.1:8000/api/kursus/{kursus_id}/")
    if kursus_resp.status_code != 200 or kursus_resp.json()['pengajar'] != pengajar_id:
        return redirect('kursus_saya_pengajar')
    kursus = kursus_resp.json()

    if request.method == 'POST':
        payload = {
            'judul': request.POST['judul'],
            'deskripsi': request.POST['deskripsi'],
            'kursus': kursus_id
        }
        files = {'file_url': request.FILES['file_url']} if request.FILES.get('file_url') else {}

        response = requests.post('http://127.0.0.1:8000/api/tugas-akhir/', data=payload, files=files)
        if response.status_code in [200, 201]:
            return redirect('detail_kursus_pengajar', kursus_id=kursus_id)

    return render(request, 'main/teacher/tambah_tugas_akhir.html', {
        'kursus': kursus,
    })
    
def kumpulkan_tugas(request, tugas_id):
    tugas = get_object_or_404(TugasAkhir, pk=tugas_id)
    peserta_id = request.session.get('user_id')
    user = get_object_or_404(Member, pk=peserta_id)

    # Cek apakah sudah pernah mengumpulkan
    existing_submission = PengumpulanTugasAkhir.objects.filter(tugas=tugas, user=user).first()

    if request.method == 'POST':
        form = PengumpulanTugasAkhirForm(request.POST, request.FILES, instance=existing_submission)
        if form.is_valid():
            pengumpulan = form.save(commit=False)
            pengumpulan.user = user
            pengumpulan.tugas = tugas
            pengumpulan.status = 'belum diperiksa'
            pengumpulan.save()
            messages.success(request, "✅ Jawaban berhasil dikirim.")
            return redirect('kumpulkan_tugas', tugas_id=tugas.id)
    else:
        form = PengumpulanTugasAkhirForm(instance=existing_submission)

    return render(request, 'main/student/form_pengumpulan_tugas.html', {
        'form': form,
        'tugas': tugas,
        'pengumpulan': existing_submission
    })
def edit_tugas_akhir(request, pk):
    tugas_resp = requests.get(f"http://127.0.0.1:8000/api/tugas-akhir/{pk}/")
    if tugas_resp.status_code != 200:
        return redirect('kursus_saya_pengajar')
    tugas = tugas_resp.json()

    kursus_resp = requests.get(f"http://127.0.0.1:8000/api/kursus/{tugas['kursus']}/")
    if kursus_resp.status_code != 200 or kursus_resp.json()['pengajar'] != request.session.get('user_id'):
        return redirect('kursus_saya_pengajar')
    kursus = kursus_resp.json()

    if request.method == 'POST':
        payload = {
            'judul': request.POST['judul'],
            'deskripsi': request.POST['deskripsi'],
            'kursus': tugas['kursus']
        }
        files = {'file_url': request.FILES['file_url']} if request.FILES.get('file_url') else None

        response = requests.put(f"http://127.0.0.1:8000/api/tugas-akhir/{pk}/", data=payload, files=files)
        if response.status_code in [200, 204]:
            return redirect('detail_kursus_pengajar', kursus_id=kursus['id'])

    return render(request, 'main/teacher/tambah_tugas_akhir.html', {
        'kursus': kursus,
        'tugas': tugas,
        'edit_mode': True
    })



def hapus_tugas_akhir(request, pk):
    tugas_resp = requests.get(f"http://127.0.0.1:8000/api/tugas-akhir/{pk}/")
    if tugas_resp.status_code != 200:
        return redirect('kursus_saya_pengajar')
    tugas = tugas_resp.json()

    kursus_id = tugas['kursus']

    kursus_resp = requests.get(f"http://127.0.0.1:8000/api/kursus/{kursus_id}/")
    if kursus_resp.status_code != 200 or kursus_resp.json()['pengajar'] != request.session.get('user_id'):
        return redirect('kursus_saya_pengajar')

    requests.delete(f"http://127.0.0.1:8000/api/tugas-akhir/{pk}/")

    return redirect('detail_kursus_pengajar', kursus_id=kursus_id)

def lihat_pengumpulan_tugas(request, tugas_id):
    tugas = get_object_or_404(TugasAkhir, pk=tugas_id)
    pengumpulan_list = PengumpulanTugasAkhir.objects.filter(tugas=tugas)

    if request.method == 'POST':
        pengumpulan_id = request.POST.get('pengumpulan_id')
        pengumpulan = get_object_or_404(PengumpulanTugasAkhir, pk=pengumpulan_id)
        pengumpulan.status = request.POST.get('status')
        pengumpulan.catatan_pengajar = request.POST.get('catatan_pengajar')
        pengumpulan.tanggal_dinilai = timezone.now().date()
        pengumpulan.save()
        messages.success(request, "✅ Penilaian berhasil diperbarui.")

        return redirect('lihat_pengumpulan_tugas', tugas_id=tugas.id)

    return render(request, 'main/teacher/pengumpulan_tugas.html', {
        'tugas': tugas,
        'pengumpulan_list': pengumpulan_list
    })

def tambah_ulasan(request, kursus_id):
    if request.session.get('user_role') != 'peserta':
        return redirect('login')

    user_id = request.session.get('user_id')
    user = get_object_or_404(Member, pk=user_id)
    kursus = get_object_or_404(Kursus, pk=kursus_id)

    # cek apakah sudah pernah memberi ulasan
    existing = Rating.objects.filter(user=user, kursus=kursus).first()
    form = RatingForm(instance=existing)
    mode = "Edit" if existing else "Tambah"

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=existing)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = user
            rating.kursus = kursus
            rating.save()
            messages.success(request, "✅ Ulasan berhasil disimpan.")
            return redirect('detail_kursus_peserta', kursus_id=kursus.id)

    return render(request, 'main/student/form_ulasan.html', {
        'form': form,
        'kursus': kursus,
        'mode': mode,
    })
def edit_ulasan_peserta(request, kursus_id):
    if request.session.get('user_role') != 'peserta':
        return redirect('login')

    kursus = get_object_or_404(Kursus, id=kursus_id)
    user_id = request.session.get('user_id')
    user = get_object_or_404(Member, id=user_id)

    ulasan = Rating.objects.filter(kursus=kursus, user=user).first()
    if not ulasan:
        messages.error(request, "Ulasan tidak ditemukan.")
        return redirect('detail_kursus_peserta', kursus_id=kursus_id)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=ulasan)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Ulasan berhasil diperbarui.")
            return redirect('detail_kursus_peserta', kursus_id=kursus_id)
    else:
        form = RatingForm(instance=ulasan)

    return render(request, 'main/student/form_edit_ulasan.html', {
        'form': form,
        'kursus': kursus
    })
def sertifikat_index(request):
    peserta_id = request.session.get('user_id')
    if not peserta_id:
        return redirect('login')

    # Ambil semua kursus yang diikuti peserta
    transaksi_list = Transaksi.objects.filter(user_id=peserta_id, is_paid=True).select_related('kursus')

    data_kursus = []
    for transaksi in transaksi_list:
        kursus = transaksi.kursus
        sertifikat = Sertifikat.objects.filter(user_id=peserta_id, kursus=kursus).first()
        data_kursus.append({
            'kursus': kursus,
            'sertifikat': sertifikat
        })

    return render(request, 'main/student/sertifikat_index.html', {
        'data_kursus': data_kursus
    })

def lihat_sertifikat(request, sertifikat_id):
    sertifikat = get_object_or_404(Sertifikat, pk=sertifikat_id)

    context = {
        "participant_name": sertifikat.user.nama,
        "course_name": sertifikat.kursus.nama,
        "platform_name": "ZapCourse",
        "completion_date": sertifikat.tanggal_diterbitkan.strftime("%d %B %Y"),
        "year": sertifikat.tanggal_diterbitkan.year,
        "instructor_name": sertifikat.kursus.pengajar.nama,
        "certificate_number": sertifikat.nomor_sertifikat,
    }

    return render(request, 'main/student/sertifikat_detail.html', context)


def register_peserta(request):
    if request.method == 'POST':
        form = RegisterPesertaForm(request.POST)
        if form.is_valid():
            peserta = form.save(commit=False)
            peserta.role = 'peserta'
            peserta.password = make_password(form.cleaned_data['password'])  # ← hash password di sini
            peserta.save()
            return redirect('login')
    else:
        form = RegisterPesertaForm()
    return render(request, 'main/register_peserta.html', {'form': form})