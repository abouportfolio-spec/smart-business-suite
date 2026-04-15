from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('business.urls')), # On dit à Django d'aller chercher les vues dans l'app business
]