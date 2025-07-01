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
    class Meta:
        model = Kursus
        fields = '__all__'

class TransaksiSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)  # ← tambahkan ini

    class Meta:
        model = Transaksi
        fields = '__all__'

class MateriKursusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MateriKursus
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class PendapatanPengajarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendapatanPengajar
        fields = '__all__'

class PendapatanAdminSerializer(serializers.ModelSerializer):
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
