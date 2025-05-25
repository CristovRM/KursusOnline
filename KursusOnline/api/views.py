from rest_framework import viewsets
from main.models import Member  # ⬅️ ambil dari main
from .serializers import MemberSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

