from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MemberViewSet, KategoriViewSet, KursusViewSet, TransaksiViewSet,
    MateriKursusViewSet, RatingViewSet, PendapatanPengajarViewSet,
    PendapatanAdminViewSet, TugasAkhirViewSet, SertifikatViewSet, PengumpulanTugasAkhirViewSet
)

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'kategori', KategoriViewSet)
router.register(r'kursus', KursusViewSet)
router.register(r'transaksi', TransaksiViewSet)
router.register(r'materi', MateriKursusViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'pendapatan-pengajar', PendapatanPengajarViewSet)
router.register(r'pendapatan-admin', PendapatanAdminViewSet)
router.register(r'tugas-akhir', TugasAkhirViewSet)
router.register(r'sertifikat', SertifikatViewSet)
router.register(r'pengumpulantugasakhir', PengumpulanTugasAkhirViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
