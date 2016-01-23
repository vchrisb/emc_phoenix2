from django.contrib import admin

from .models import Featurette, FAQ

class FeaturetteAdmin(admin.ModelAdmin):
    list_display = ["position", "heading", "privacy", "publish"]
    ordering = ['position']

admin.site.register(Featurette,FeaturetteAdmin)

class FAQAdmin(admin.ModelAdmin):
    list_display = ["position", "question", "privacy", "publish"]
    ordering = ['position']

admin.site.register(FAQ,FAQAdmin)
