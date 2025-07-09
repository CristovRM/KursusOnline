from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from main.models import (
    Member, Kategori, Kursus, Transaksi, MateriKursus,
    Rating, PendapatanPengajar, PendapatanAdmin, TugasAkhir, Sertifikat, PengumpulanTugasAkhir
)

class MemberSerializer(serializers.ModelSerializer):
    # password tidak wajib, hanya tulis (write_only)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Member
        fields = ['id', 'nama', 'email', 'pekerjaan', 'password', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  # ambil password jika ada dan hapus dari dict
        if password:
            instance.password = make_password(password)
        # update field lain
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

class KursusSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False, write_only=True)  # hanya saat input POST
    foto_url = serializers.SerializerMethodField()  # untuk GET tampil URL

    kategori = KategoriSerializer(read_only=True)
    pengajar = MemberSerializer(read_only=True)

    # Tapi saat POST/PUT kamu tetap butuh id-nya
    kategori_id = serializers.PrimaryKeyRelatedField(
        queryset=Kategori.objects.all(), source='kategori', write_only=True
    )
    pengajar_id = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), source='pengajar', write_only=True
    )

    class Meta:
        model = Kursus
        fields = '__all__'
        extra_fields = ['foto_url']  # untuk GET

    def get_foto_url(self, obj):
        if obj.foto:
            return f"/media/{obj.foto}"
        return None
    
    def update(self, instance, validated_data):
        foto = validated_data.pop('foto', None)

        if foto:
            import time, os
            from django.conf import settings

            nama_file = f"{int(time.time())}_{foto.name.replace(' ', '_')}"
            path = os.path.join(settings.MEDIA_ROOT, nama_file)

            with open(path, 'wb+') as dest:
                for chunk in foto.chunks():
                    dest.write(chunk)

            instance.foto = nama_file

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance 
    

class TransaksiSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    kursus = serializers.PrimaryKeyRelatedField(queryset=Kursus.objects.all())

    
    user_detail = MemberSerializer(source='user', read_only=True)
    kursus_detail = KursusSerializer(source='kursus', read_only=True)

    class Meta:
        model = Transaksi
        fields = '__all__'


class MateriKursusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MateriKursus
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)
    kursus = KursusSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'

class PendapatanPengajarSerializer(serializers.ModelSerializer):
    pengajar = MemberSerializer(read_only=True)
    transaksi = TransaksiSerializer(read_only=True)
    class Meta:
        model = PendapatanPengajar
        fields = '__all__'

class PendapatanAdminSerializer(serializers.ModelSerializer):
    transaksi = TransaksiSerializer(read_only=True)

    class Meta:
        model = PendapatanAdmin
        fields = '__all__'

class TugasAkhirSerializer(serializers.ModelSerializer):
    class Meta:
        model = TugasAkhir
        fields = '__all__'

class SertifikatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sertifikat
        fields = '__all__'

class PengumpulanTugasAkhirSerializer(serializers.ModelSerializer):
    class Meta:
        model = PengumpulanTugasAkhir
        fields = '__all__'
