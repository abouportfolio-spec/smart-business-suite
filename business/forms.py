from django import forms
from .models import Produit, Vente

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'prix_achat', 'prix_vente', 'stock']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Ex: Smartphone X'}),
            'prix_achat': forms.NumberInput(attrs={'placeholder': 'Prix d\'achat'}),
            'prix_vente': forms.NumberInput(attrs={'placeholder': 'Prix de vente'}),
            'stock': forms.NumberInput(attrs={'placeholder': 'Quantité initiale'}),
        }

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['produit', 'quantite']
        widgets = {
            'produit': forms.Select(attrs={'class': 'custom-select'}),
            'quantite': forms.NumberInput(attrs={'placeholder': 'Quantité à vendre', 'min': '1'}),
        }