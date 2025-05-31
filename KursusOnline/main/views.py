from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminLoginForm
from .models import Member, Kursus, Transaksi, PendapatanAdmin
from django.db.models import Sum
import requests


# Create your views here.
def home(request):
    context={}
    return render(request, "main/home.html", context)
def login(request):
    context={}
    return render(request, "main/login.html", context)
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

# Crud TABEL MEMBER.

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
            print("API Error:", response.status_code, response.text)
            print("Response Content:", response.text)
            response_data = response.json() if response.content else {}
            error_message = response_data.get('detail', 'Gagal mengedit user.')
            return render(request, 'main/admin/manageuser.html', {
                'manage_user': requests.get('http://127.0.0.1:8000/api/members/').json(),
                'error_message': error_message
            })

def delete_user(request, id):
    requests.delete(f'http://127.0.0.1:8000/api/members/{id}/')
    return redirect('manage_user')

