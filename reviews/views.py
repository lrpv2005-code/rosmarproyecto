from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Serie, Resena
from .forms import RegistroForm, ResenaForm

def home_view(request):
    # Calculate average rating directly using annotation so we can sort
    series = Serie.objects.annotate(
        avg_rating=Avg('resenas__calificacion')
    ).order_by('-avg_rating')[:10]
    
    return render(request, 'reviews/home.html', {'series': series})

def detalle_serie(request, serie_id):
    serie = get_object_or_404(Serie, id=serie_id)
    resenas = serie.resenas.all()
    user_has_reviewed = False

    if request.user.is_authenticated:
        user_has_reviewed = resenas.filter(usuario=request.user).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ResenaForm(request.POST)
        if form.is_valid() and not user_has_reviewed:
            nueva_resena = form.save(commit=False)
            nueva_resena.serie = serie
            nueva_resena.usuario = request.user
            nueva_resena.save()
            return redirect('detalle_serie', serie_id=serie.id)
    else:
        form = ResenaForm()

    return render(request, 'reviews/detalle.html', {
        'serie': serie,
        'resenas': resenas,
        'form': form,
        'user_has_reviewed': user_has_reviewed
    })

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'reviews/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'reviews/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
