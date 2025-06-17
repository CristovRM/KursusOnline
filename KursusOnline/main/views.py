from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminLoginForm
from .models import Member, Kursus, Transaksi, PendapatanAdmin, PendapatanPengajar, Rating, MateriKursus, TugasAkhir
from django.db.models import Sum
from .forms import UserLoginForm
from .forms import MateriForm
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
import requests
from django.conf import settings


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
def mycourse(request):
    context={}
    return render(request, "main/student/mycourse.html", context)
def mycourse1(request):
    context={}
    return render(request, "main/student/mycourse1.html", context)

from django.contrib.auth.hashers import check_password

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
        'admin_nama': request.session.get('admin_nama'),
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

def dashboard_pengajar(request):
    if request.session.get('user_role') != 'pengajar':
        return redirect('login_user')

    pengajar_id = request.session.get('user_id')
    pengajar_nama = request.session.get('user_nama')

    total_kursus = Kursus.objects.filter(pengajar_id=pengajar_id).count()
    total_pendapatan = PendapatanPengajar.objects.filter(pengajar_id=pengajar_id).aggregate(total=Sum('jumlah'))['total'] or 0
    rating_avg = Rating.objects.filter(kursus__pengajar_id=pengajar_id).aggregate(avg=Avg('rating'))['avg'] or 0
    rating_avg = round(rating_avg, 2)

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

    kursus_list = Kursus.objects.filter(pengajar_id=pengajar_id).select_related('kategori')

    context = {
        'pengajar_nama': pengajar_nama,
        'kursus_list': kursus_list,
        'foto_url_prefix': settings.MEDIA_URL,
    }

    return render(request, 'main/teacher/kursus_saya.html', context)

def detail_kursus_pengajar(request, kursus_id):
    if request.session.get('user_role') != 'pengajar':
        return redirect('login_user')

    kursus = Kursus.objects.get(id=kursus_id)
    
    # Validasi: hanya pengajar yang punya kursus ini yang bisa lihat
    if kursus.pengajar.id != request.session.get('user_id'):
        return redirect('kursus_saya_pengajar')

    materi_list = MateriKursus.objects.filter(kursus=kursus).order_by('urutan')

    context = {
        'kursus': kursus,
        'materi_list': materi_list,
        'MEDIA_URL': settings.MEDIA_URL,  # ← tambahkan ini agar bisa dipakai di template
    }

    return render(request, 'main/teacher/detail_kursus.html', context)

# student
def dashboard_student(request):
    if request.session.get('user_role') != 'peserta':
        return redirect('login')  # atau login_user jika berbeda

    peserta_id = request.session.get('user_id')
    peserta_nama = request.session.get('user_nama')

    # Jumlah kursus yang diikuti peserta
    total_kursus_diikuti = Transaksi.objects.filter(user_id=peserta_id).count()

    # Kursus yang diikuti (limit 5 terbaru)
    kursus_diikuti = Transaksi.objects.select_related('kursus').filter(user_id=peserta_id).order_by('-id')[:5]

    # Rata-rata rating yang diberikan oleh peserta (jika ada)
    rating_diberikan = Rating.objects.filter(user_id=peserta_id).aggregate(avg=Avg('rating'))['avg'] or 0
    rating_diberikan = round(rating_diberikan, 2)

    context = {
        'peserta_nama': peserta_nama,
        'total_kursus_diikuti': total_kursus_diikuti,
        'kursus_diikuti': kursus_diikuti,
        'rating_diberikan': rating_diberikan,
    }

    return render(request, 'main/student/dashboard.html', context)

def transaksi_peserta(request):
    if request.session.get('user_role') != 'peserta':
        return redirect('login')  # Pastikan hanya peserta yang bisa akses

    peserta_id = request.session.get('user_id')

    # Ambil semua transaksi yang dilakukan peserta
    transaksi_list = Transaksi.objects.filter(user_id=peserta_id).select_related('kursus').order_by('-tanggal_transaksi')

    context = {
        'transaksi_list': transaksi_list,
        'peserta_nama': request.session.get('user_nama'),
    }

    return render(request, 'main/student/transaksi_peserta.html', context)

def tambah_materi(request, kursus_id):
    kursus = get_object_or_404(Kursus, id=kursus_id)

    # Cek kepemilikan kursus
    if kursus.pengajar.id != request.session.get('user_id'):
        return redirect('kursus_saya_pengajar')

    if request.method == 'POST':
        form = MateriForm(request.POST, request.FILES, kursus=kursus)
        if form.is_valid():
            materi = form.save(commit=False)
            materi.kursus = kursus
            materi.save()
            return redirect('detail_kursus_pengajar', kursus_id=kursus.id)
    else:
        form = MateriForm(kursus=kursus)

    return render(request, 'main/teacher/form_materi.html', {
        'form': form,
        'kursus': kursus,
        'mode': 'Tambah'
    })

def edit_materi(request, pk):
    materi = get_object_or_404(MateriKursus, pk=pk)
    kursus = materi.kursus

    # Cek kepemilikan kursus
    if kursus.pengajar.id != request.session.get('user_id'):
        return redirect('kursus_saya_pengajar')

    if request.method == 'POST':
        form = MateriForm(request.POST, request.FILES, instance=materi, kursus=kursus)
        if form.is_valid():
            updated_materi = form.save(commit=False)
            if not request.FILES.get('file_url'):
                updated_materi.file_url = materi.file_url  # file tetap jika tidak diubah
            updated_materi.save()
            return redirect('detail_kursus_pengajar', kursus_id=kursus.id)
    else:
        form = MateriForm(instance=materi, kursus=kursus)

    return render(request, 'main/teacher/form_materi.html', {
        'form': form,
        'kursus': kursus,
        'mode': 'Edit'
    })


def hapus_materi(request, pk):
    materi = get_object_or_404(MateriKursus, pk=pk)
    kursus_id = materi.kursus.id

    if materi.kursus.pengajar.id == request.session.get('user_id'):
        materi.delete()

    return redirect('detail_kursus_pengajar', kursus_id=kursus_id)

def daftar_peserta(request, kursus_id):
    kursus = get_object_or_404(Kursus, id=kursus_id)

    # Pastikan pengajar kursus ini adalah yang login
    if kursus.pengajar.id != request.session.get('user_id'):
        return redirect('kursus_saya_pengajar')

    # Ambil semua transaksi yang berhasil dibayar untuk kursus ini
    peserta_transaksi = Transaksi.objects.filter(kursus=kursus, is_paid='yes').select_related('user')

    return render(request, 'main/teacher/daftar_peserta.html', {
        'kursus': kursus,
        'peserta_transaksi': peserta_transaksi
    })
def lihat_ulasan(request, kursus_id):
    kursus = get_object_or_404(Kursus, id=kursus_id)

    # Pastikan hanya pengajar kursus ini yang bisa melihat
    if kursus.pengajar.id != request.session.get('user_id'):
        return redirect('kursus_saya_pengajar')

    ulasan_list = Rating.objects.filter(kursus=kursus).select_related('user')

    return render(request, 'main/teacher/ulasan_kursus.html', {
        'kursus': kursus,
        'ulasan_list': ulasan_list
    })
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