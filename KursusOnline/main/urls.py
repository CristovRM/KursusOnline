from . import views
from django.urls import path
from .views import laporan_pengajar
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("course", views.course, name="course"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("my-courses", views.mycourse, name="mycourse"),
    path("my-courses1", views.mycourse1, name="mycourse1"),
    
    # Pengajar
    path('teacher/dashboard/', views.dashboard_pengajar, name='dashboard_pengajar'),
    path('teacher/my-course/', views.kursus_saya_pengajar, name='kursus_saya_pengajar'),
    path('teacher/my-course/<int:kursus_id>/', views.detail_kursus_pengajar, name='detail_kursus_pengajar'),
    path('teacher/my-course/<int:kursus_id>/materi/tambah/', views.tambah_materi, name='tambah_materi'),
    path('teacher/my-course/materi/<int:pk>/edit/', views.edit_materi, name='edit_materi'),
    path('teacher/my-course/materi/<int:pk>/hapus/', views.hapus_materi, name='hapus_materi'),
    path('teacher/my-course/<int:kursus_id>/peserta/', views.daftar_peserta, name='daftar_peserta'),
    path('teacher/my-course/<int:kursus_id>/ulasan/', views.lihat_ulasan, name='lihat_ulasan'),
    path('teacher/laporan/', laporan_pengajar, name='laporan_pengajar'),
    path('logout/', views.logout, name='logout'),



    # Admin
    path('login-admin', views.login_admin, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.logout_admin, name='logout_admin'),
    path('manage-user/', views.manage_user, name='manage_user'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
    
    # Student
    path('student/dashboard', views.dashboard_student, name='peserta_dashboard'),
    path('student/mycourse/', views.mycourse, name='mycourse'),
    path('student/transaksi/', views.transaksi_peserta, name='transaksi_peserta'),
    path("certificate/", views.certificate_view, name="certificate"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
