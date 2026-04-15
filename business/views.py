from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Sum, F
from .models import Produit, Vente
from .forms import ProduitForm, VenteForm
from .utils import generer_recu_texte

def dashboard(request):
    produits = Produit.objects.all().order_by('-date_ajout')
    ventes = Vente.objects.all().order_by('-date_vente')[:10]
    
    # CALCUL EXPERT : Agrégation SQL pour la performance
    stats = produits.aggregate(
        total_valeur=Sum(F('prix_vente') * F('stock')),
        total_qte=Sum('stock')
    )
    
    # Données pour le graphique
    labels = [str(p) for p in produits]
    data_stock = [p.stock for p in produits]
    
    # Initialisation des formulaires
    form_p = ProduitForm()
    form_v = VenteForm()

    if request.method == 'POST':
        # --- GESTION AJOUT PRODUIT ---
        if 'submit_produit' in request.POST:
            form_p = ProduitForm(request.POST)
            if form_p.is_valid():
                form_p.save()
                messages.success(request, "Produit ajouté avec succès !")
                return redirect('dashboard')
        
        # --- GESTION ENREGISTREMENT VENTE & GÉNÉRATION REÇU ---
        elif 'submit_vente' in request.POST:
            form_v = VenteForm(request.POST)
            if form_v.is_valid():
                try:
                    # Sauvegarde et récupération de l'instance de vente
                    vente = form_v.save()
                    
                    # GÉNÉRATION DU REÇU (Objectif Final)
                    recu = generer_recu_texte(vente)
                    
                    # Stockage temporaire dans la session pour l'affichage unique
                    request.session['dernier_recu'] = recu
                    
                    messages.success(request, "Vente enregistrée !")
                    return redirect('dashboard')
                except ValidationError as e:
                    form_v.add_error(None, e)
            else:
                messages.error(request, "Erreur dans le formulaire de vente.")

    context = {
        'produits': produits,
        'ventes': ventes,
        'total_stock': stats['total_valeur'] or 0,
        'total_articles': stats['total_qte'] or 0,
        'labels': labels,
        'data_stock': data_stock,
        'form_p': form_p,
        'form_v': form_v,
        # On récupère le reçu de la session s'il existe
        'recu_a_afficher': request.session.get('dernier_recu'),
    }
    return render(request, 'business/dashboard.html', context)

def supprimer_session_recu(request):
    """Vue technique pour nettoyer la session après fermeture du reçu"""
    if 'dernier_recu' in request.session:
        del request.session['dernier_recu']
    return redirect('dashboard')

def modifier_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == "POST":
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, f"{produit.nom} mis à jour !")
            return redirect('dashboard')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'business/modifier.html', {'form': form, 'produit': produit})

def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    nom = produit.nom
    produit.delete()
    messages.warning(request, f"{nom} a été supprimé.")
    return redirect('dashboard')