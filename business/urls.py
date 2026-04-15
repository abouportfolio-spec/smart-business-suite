from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('supprimer-session-recu/', views.supprimer_session_recu, name='supprimer_session_recu'),
    path('modifier/<int:pk>/', views.modifier_produit, name='modifier_produit'),
    path('supprimer/<int:pk>/', views.supprimer_produit, name='supprimer_produit'),
]