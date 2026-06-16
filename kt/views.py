from django.shortcuts import render, redirect, get_object_or_404

from .models import Kontakt
from.forms import KontaktForm

# Create your views here.
def index(request):
    listaKontaktow = Kontakt.objects.all()
    return render(request, 'index.html', {'listaKontaktow': listaKontaktow})
def dodaj(request):
    if request.method == 'POST':
        ob = KontaktForm(request.POST)
        ob.save()
        return redirect('index')
    else:
        form = KontaktForm()
        return render(request, 'dodaj.html', {'form': form})

def edytuj(request, id):
    kontakt = Kontakt.objects.get(pk=id)
    if request.method == 'POST':
            ob = KontaktForm(request.POST, instance=kontakt)
            ob.save()
            return redirect('index')
    else:
            form = KontaktForm(instance=kontakt)
            return render(request, 'edytuj.html', {'form': form})
def usun(request, id):
    Kontakt.objects.filter(pk=id).delete()
    return redirect('index')
    #formularz = KontaktForm()
    #return render(request, 'dodaj.html', {'formularz': formularz})
def kontakt(request):
    return render(request, 'kontakt.html')