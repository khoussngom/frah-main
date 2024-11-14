from django.contrib import admin
from .models import Blog, Realisation, ImageGroup, Image,RealisationImage,Category,Newsletter


class RealisationImageInline(admin.TabularInline):
    model = RealisationImage
    extra = 1  # Permet d'afficher au moins une ligne vide pour ajouter une image

class RealisationAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_evenement', 'created_at', 'updated_at']
    inlines = [RealisationImageInline]
      
admin.site.register(Blog)
admin.site.register(Newsletter)
admin.site.register(ImageGroup)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Realisation,RealisationAdmin)

