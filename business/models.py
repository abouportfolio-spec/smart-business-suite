from django.db import models
from django.core.exceptions import ValidationError

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    # Ajout de la référence pour différencier les articles (ex: XPS-9310)
    reference = models.CharField(max_length=50, unique=True, null=True, blank=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    date_ajout = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        # Format expert : affiche la référence si elle existe
        if self.reference:
            return f"{self.nom} [{self.reference}]"
        return self.nom
    
    @property
    def benefice_unitaire(self):
        return self.prix_vente - self.prix_achat

    @property
    def valeur_stock_potentielle(self):
        """Calcul utilisé par la vue pour le total du stock"""
        return self.prix_vente * self.stock

class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='ventes')
    quantite = models.PositiveIntegerField()
    # Le prix_total est calculé automatiquement, pas besoin de le modifier à la main
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    date_vente = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Sécurité : vérifier si le stock est suffisant
        if self.produit and self.quantite > self.produit.stock:
            raise ValidationError(f"Stock insuffisant ! Il ne reste que {self.produit.stock} unités.")

    def save(self, *args, **kwargs):
        # Sécurité Architecte : on ne décrémente le stock que lors de la CRÉATION (pas d'un update)
        if not self.pk: 
            self.full_clean() # Force la validation de clean()
            self.prix_total = self.produit.prix_vente * self.quantite
            
            # Mise à jour atomique simple du stock
            self.produit.stock -= self.quantite
            self.produit.save()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vente : {self.produit.nom} ({self.quantite})"