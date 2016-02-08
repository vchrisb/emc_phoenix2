from rest_framework import serializers
from .models import DocumentGroup, Document

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('url', 'title', 'filename', 'downloads')

class DocumentGroupSerializer(serializers.HyperlinkedModelSerializer):
    document = DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = DocumentGroup
        fields = ('url', 'title', 'document')
