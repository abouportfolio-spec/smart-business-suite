from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    reference = models.CharField(max_length=50, unique=True, null=True, blank=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        if self.reference:
            return f"{self.nom} [{self.reference}]"
        return self.nom

    @property
    def benefice_unitaire(self):
        return self.prix_vente - self.prix_achat

    @property
    def valeur_stock_potentielle(self):
        return self.prix_vente * self.stock

    # --- BRIQUE INTELLIGENTE ---
    def estimation_jours_restants(self):
        """
        Analyse les ventes des 7 derniers jours pour prédire la rupture de stock.
        """
        il_y_a_une_semaine = timezone.now() - timedelta(days=7)
        # On utilise related_name='ventes' que tu as défini dans la ForeignKey
        total_vendu = self.ventes.filter(date_vente__gte=il_y_a_une_semaine).aggregate(Sum('quantite'))['quantite__sum'] or 0

        if total_vendu <= 0:
            return None # Indique qu'il n'y a pas assez de données pour prédire

        vitesse_journaliere = total_vendu / 7
        jours_restants = self.stock / vitesse_journaliere
        return round(jours_restants, 1)

class Vente(models.Model):
    # Utilisation de related_name='ventes' pour faciliter les calculs prédictifs
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='ventes')
    quantite = models.PositiveIntegerField()
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    date_vente = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.produit and self.quantite > self.produit.stock:
            raise ValidationError(f"Stock insuffisant ! Il ne reste que {self.produit.stock} unités.")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.full_clean()
            self.prix_total = self.produit.prix_vente * self.quantite

            # Mise à jour du stock
            self.produit.stock -= self.quantite
            self.produit.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vente : {self.produit.nom} ({self.quantite})"