from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dodaj', views.dodaj, name='dodaj'),
    path('kontakt', views.kontakt, name='kontakt'),
    path('edytuj/<int:id>', views.edytuj, name='edytuj'),
    path('usun/<int:id>', views.usun, name='usun'),

]