from django.contrib import admin
from .models import DocumentGroup, Document
# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title"]
    readonly_fields = ['downloads']

class DocumentInLine(admin.StackedInline):
    model = Document
    readonly_fields = ['downloads']
    extra = 0

class DocumentGroupAdmin(admin.ModelAdmin):
    list_display = ["title"]
    inlines = [DocumentInLine]

admin.site.register(DocumentGroup, DocumentGroupAdmin)
admin.site.register(Document, DocumentAdmin)
