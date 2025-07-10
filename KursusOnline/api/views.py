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
    queryset = Kursus.objects.all()
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

    def perform_update(self, serializer):
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

    def get_queryset(self):
        queryset = Transaksi.objects.all()
        user = self.request.query_params.get('user')
        kursus = self.request.query_params.get('kursus')
        if user:
            queryset = queryset.filter(user_id=user)
        if kursus:
            queryset = queryset.filter(kursus_id=kursus)
        return queryset

class MateriKursusViewSet(viewsets.ModelViewSet):
    queryset = MateriKursus.objects.all()
    serializer_class = MateriKursusSerializer

    def get_queryset(self):
        kursus_id = self.request.query_params.get('kursus')
        if kursus_id:
            return MateriKursus.objects.filter(kursus_id=kursus_id)
        return MateriKursus.objects.all()

class TugasAkhirViewSet(viewsets.ModelViewSet):
    queryset = TugasAkhir.objects.all()
    serializer_class = TugasAkhirSerializer

    def get_queryset(self):
        kursus_id = self.request.query_params.get('kursus')
        if kursus_id:
            return TugasAkhir.objects.filter(kursus_id=kursus_id)
        return TugasAkhir.objects.all()

class PengumpulanTugasAkhirViewSet(viewsets.ModelViewSet):
    queryset = PengumpulanTugasAkhir.objects.all()
    serializer_class = PengumpulanTugasAkhirSerializer

    def get_queryset(self):
        tugas_id = self.request.query_params.get('tugas')
        if tugas_id:
            return PengumpulanTugasAkhir.objects.filter(tugas_id=tugas_id)
        return PengumpulanTugasAkhir.objects.none()

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_queryset(self):
        kursus_id = self.request.query_params.get('kursus')
        if kursus_id:
            return Rating.objects.filter(kursus_id=kursus_id)
        return Rating.objects.none()

class PendapatanPengajarViewSet(viewsets.ModelViewSet):
    queryset = PendapatanPengajar.objects.all()
    serializer_class = PendapatanPengajarSerializer

    def get_queryset(self):
        queryset = PendapatanPengajar.objects.all()

        pengajar = self.request.query_params.get('pengajar')
        transaksi = self.request.query_params.get('transaksi')
        kursus_id = self.request.query_params.get('transaksi__kursus')

        if pengajar:
            queryset = queryset.filter(pengajar_id=pengajar)
        if transaksi:
            queryset = queryset.filter(transaksi_id=transaksi)
        if kursus_id:
            queryset = queryset.filter(transaksi__kursus_id=kursus_id)

        # Pastikan hanya dari transaksi yang sudah dibayar
        queryset = queryset.filter(transaksi__is_paid=True)

        return queryset

class PendapatanAdminViewSet(viewsets.ModelViewSet):
    queryset = PendapatanAdmin.objects.all()
    serializer_class = PendapatanAdminSerializer

class SertifikatViewSet(viewsets.ModelViewSet):
    queryset = Sertifikat.objects.all()
    serializer_class = SertifikatSerializer
