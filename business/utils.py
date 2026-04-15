from datetime import datetime

def generer_recu_texte(vente):
    """Génère un format de reçu professionnel pour l'affichage et l'impression"""
    
    # On récupère le nom et la référence proprement
    produit_nom = vente.produit.nom
    ref = vente.produit.reference if vente.produit.reference else "N/A"
    
    lignes = [
        "================================",
        "       SMART BUSINESS PRO       ",
        "    --- REÇU DE VENTE ---      ",
        "================================",
        f"Facture N° : #VEN-{vente.id:04d}",
        f"Date       : {vente.date_vente.strftime('%d/%m/%Y %H:%M')}",
        "--------------------------------",
        f"PRODUIT    : {produit_nom}",
        f"REF        : {ref}",
        f"QUANTITE   : {vente.quantite}",
        f"PRIX UNITA.: {vente.produit.prix_vente} FCFA",
        "--------------------------------",
        f"TOTAL TTC  : {vente.prix_total} FCFA",
        "================================",
        "  Statut : PAYÉ ET ENCAISSÉ     ",
        "  Logiciel par : Toure Abou     ",
        "================================",
        "   Merci de votre confiance !   ",
        "================================"
    ]
    return "\n".join(lignes)