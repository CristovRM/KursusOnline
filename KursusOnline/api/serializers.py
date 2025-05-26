from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from main.models import (
    Member, Kategori, Kursus, Transaksi, MateriKursus,
    Rating, PendapatanPengajar, PendapatanAdmin, TugasAkhir, Sertifikat
)

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'nama', 'email', 'pekerjaan', 'password', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

class KursusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kursus
        fields = '__all__'

class TransaksiSerializer(serializers.ModelSerializer):
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
