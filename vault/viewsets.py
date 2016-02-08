from rest_framework import viewsets

from .serializers import DocumentGroupSerializer, DocumentSerializer
from .models import DocumentGroup, Document

class DocumentGroupViewSet(viewsets.ModelViewSet):
    queryset = DocumentGroup.objects.all()
    serializer_class = DocumentGroupSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
