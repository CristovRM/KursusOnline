from rest_framework import viewsets
from django.core.files.storage import FileSystemStorage
from django.conf import settings
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
    serializer_class = KursusSerializer

    def get_queryset(self):
        pengajar_id = self.request.query_params.get('pengajar')
        if pengajar_id:
            return Kursus.objects.filter(pengajar_id=pengajar_id)
        return Kursus.objects.all()
    def perform_create(self, serializer):
        foto_file = self.request.FILES.get('foto')
        if foto_file:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(foto_file.name, foto_file)
            serializer.save(foto=filename)
        else:
            serializer.save()

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
    serializer_class = PendapatanPengajarSerializer

    def get_queryset(self):
        queryset = PendapatanPengajar.objects.all()

        pengajar = self.request.query_params.get('pengajar')
        transaksi = self.request.query_params.get('transaksi')

        if pengajar:
            queryset = queryset.filter(pengajar_id=pengajar)
        if transaksi:
            queryset = queryset.filter(transaksi_id=transaksi)

        return queryset

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