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
    path('teacher/my-course/<int:kursus_id>/tugas-akhir/tambah/', views.tambah_tugas_akhir, name='tambah_tugas_akhir'),
    path('teacher/my-course/tugas-akhir/<int:pk>/edit/', views.edit_tugas_akhir, name='edit_tugas_akhir'),
    path('teacher/my-course/tugas-akhir/<int:pk>/hapus/', views.hapus_tugas_akhir, name='hapus_tugas_akhir'),
    path('teacher/my-course/tugas/<int:tugas_id>/pengumpulan/', views.lihat_pengumpulan_tugas, name='lihat_pengumpulan_tugas'),




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
    path('student/transaksi/', views.transaksi_peserta, name='transaksi_peserta'),
    path("certificate/", views.certificate_view, name="certificate"),
    path('student/kursus/<int:kursus_id>/', views.detail_kursus_peserta, name='detail_kursus_peserta'),
    path('student/mycourse/', views.mycourse_student, name='mycourse_student'),
    path('peserta/kumpulkan-tugas/<int:tugas_id>/', views.kumpulkan_tugas, name='kumpulkan_tugas'),
    path('peserta/<int:kursus_id>/ulasan/', views.tambah_ulasan, name='tambah_ulasan'),
    path('peserta/kursus/<int:kursus_id>/edit-ulasan/', views.edit_ulasan_peserta, name='edit_ulasan_peserta'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
