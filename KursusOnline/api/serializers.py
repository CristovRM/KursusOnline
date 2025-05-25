from rest_framework import serializers
from main.models import Member  # ⬅️ ambil dari main

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'