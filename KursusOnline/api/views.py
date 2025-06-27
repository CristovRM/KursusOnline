from rest_framework import viewsets
from main.models import (
    Member, Kategori, Kursus, Transaksi, MateriKursus,
    Rating, PendapatanPengajar, PendapatanAdmin, TugasAkhir, Sertifikat, PengumpulanTugasAkhir
)
from .serializers import (
    MemberSerializer, KategoriSerializer, KursusSerializer, TransaksiSerializer,
    MateriKursusSerializer, RatingSerializer, PendapatanPengajarSerializer,
    PendapatanAdminSerializer, TugasAkhirSerializer, SertifikatSerializer, PengumpulanTugasAkhirSerializer
)

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer

class KursusViewSet(viewsets.ModelViewSet):
    queryset = Kursus.objects.all()
    serializer_class = KursusSerializer

class TransaksiViewSet(viewsets.ModelViewSet):
    queryset = Transaksi.objects.all()
    serializer_class = TransaksiSerializer

class MateriKursusViewSet(viewsets.ModelViewSet):
    queryset = MateriKursus.objects.all()
    serializer_class = MateriKursusSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class PendapatanPengajarViewSet(viewsets.ModelViewSet):
    queryset = PendapatanPengajar.objects.all()
    serializer_class = PendapatanPengajarSerializer

class PendapatanAdminViewSet(viewsets.ModelViewSet):
    queryset = PendapatanAdmin.objects.all()
    serializer_class = PendapatanAdminSerializer

class TugasAkhirViewSet(viewsets.ModelViewSet):
    queryset = TugasAkhir.objects.all()
    serializer_class = TugasAkhirSerializer

class SertifikatViewSet(viewsets.ModelViewSet):
    queryset = Sertifikat.objects.all()
    serializer_class = SertifikatSerializer

class PengumpulanTugasAkhirViewSet(viewsets.ModelViewSet):
    queryset = PengumpulanTugasAkhir.objects.all()
    serializer_class = PengumpulanTugasAkhirSerializer