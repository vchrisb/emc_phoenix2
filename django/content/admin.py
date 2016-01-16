from django.contrib import admin

from .models import Featurette

class FeaturetteAdmin(admin.ModelAdmin):
    list_display = ["position", "heading", "privacy", "publish"]
    ordering = ['-position']

admin.site.register(Featurette,FeaturetteAdmin)
