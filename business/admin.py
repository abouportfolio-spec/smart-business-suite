from django.contrib import admin
from .models import Produit

# Register your models here.
@admin.register(Produit)
class produitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix_achat', 'prix_vente', 'stock', 'date_ajout', 'benefice_unitaire')
