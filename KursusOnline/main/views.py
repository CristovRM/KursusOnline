from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminLoginForm
from .models import Member

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

def login_admin(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                admin_user = Member.objects.get(email=email, password=password, role='admin')
                request.session['admin_id'] = admin_user.id
                request.session['admin_nama'] = admin_user.nama
                return redirect('admin_dashboard')  # ganti sesuai URL dashboard admin kamu
            except Member.DoesNotExist:
                messages.error(request, 'Email atau password salah, atau Anda bukan admin.')
    else:
        form = AdminLoginForm()

    return render(request, 'main/admin/login.html', {'form': form})