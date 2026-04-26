from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Serie, Resena
from .forms import RegistroForm, ResenaForm

def home_view(request):
    # Calculate average rating directly using annotation so we can sort
    series = Serie.objects.filter(tipo='tv').annotate(
        avg_rating=Avg('resenas__calificacion')
    ).order_by('-avg_rating')[:10]
    
    peliculas = Serie.objects.filter(tipo='movie').annotate(
        avg_rating=Avg('resenas__calificacion')
    ).order_by('-avg_rating')[:10]
    
    return render(request, 'reviews/home.html', {'series': series, 'peliculas': peliculas})

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

    seasons = []
    if serie.tmdb_id:
        from .tmdb_service import obtener_detalle_serie
        detalle = obtener_detalle_serie(serie.tmdb_id)
        if detalle and 'seasons' in detalle:
            seasons = detalle['seasons']

    return render(request, 'reviews/detalle.html', {
        'serie': serie,
        'resenas': resenas,
        'form': form,
        'user_has_reviewed': user_has_reviewed,
        'seasons': seasons
    })

def _lista_series_view(request, titulo, funcion_obtener):
    resultados = funcion_obtener()
    tmdb_ids_locales = Serie.objects.filter(
        tmdb_id__in=[r['tmdb_id'] for r in resultados]
    ).values_list('tmdb_id', flat=True)
    
    guardadas_usuario = []
    if request.user.is_authenticated:
        guardadas_usuario = Serie.objects.filter(
            usuarios_que_guardaron=request.user, 
            tmdb_id__in=[r['tmdb_id'] for r in resultados]
        ).values_list('tmdb_id', flat=True)
        
    for r in resultados:
        r['en_bd'] = r['tmdb_id'] in tmdb_ids_locales
        r['guardada_por_usuario'] = r['tmdb_id'] in guardadas_usuario

        
    return render(request, 'reviews/lista_series.html', {
        'resultados': resultados, 
        'titulo_seccion': titulo
    })

def populares_view(request, media_type="tv"):
    from .tmdb_service import obtener_populares
    tipo_str = "Series" if media_type == "tv" else "Películas"
    return _lista_series_view(request, f"Populares ({tipo_str})", lambda: obtener_populares(media_type))

def estrenos_view(request, media_type="tv"):
    from .tmdb_service import obtener_estrenos
    tipo_str = "Series" if media_type == "tv" else "Películas"
    return _lista_series_view(request, f"Estrenos ({tipo_str})", lambda: obtener_estrenos(media_type))

def prontas_estrenar_view(request, media_type="tv"):
    from .tmdb_service import obtener_trailers_prontas_estrenar
    resultados = obtener_trailers_prontas_estrenar(media_type)
    tipo_str = "Series" if media_type == "tv" else "Películas"
    return render(request, 'reviews/trailers.html', {
        'resultados': resultados,
        'titulo_seccion': f"Próximamente ({tipo_str})"
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

def buscar_serie_view(request):
    from .tmdb_service import buscar_series
    query = request.GET.get('q', '')
    resultados = []
    if query:
        resultados = buscar_series(query)
        
        # Verificar cuáles ya están en la BD local
        tmdb_ids_locales = Serie.objects.filter(
            tmdb_id__in=[r['tmdb_id'] for r in resultados]
        ).values_list('tmdb_id', flat=True)
        
        guardadas_usuario = []
        if request.user.is_authenticated:
            guardadas_usuario = Serie.objects.filter(
                usuarios_que_guardaron=request.user, 
                tmdb_id__in=[r['tmdb_id'] for r in resultados]
            ).values_list('tmdb_id', flat=True)
            
        for r in resultados:
            r['en_bd'] = r['tmdb_id'] in tmdb_ids_locales
            r['guardada_por_usuario'] = r['tmdb_id'] in guardadas_usuario
            
    return render(request, 'reviews/resultados_busqueda.html', {'resultados': resultados, 'query': query})

def _obtener_o_crear_serie_tmdb(tmdb_id):
    serie = Serie.objects.filter(tmdb_id=tmdb_id).first()
    if not serie:
        from .tmdb_service import obtener_detalle_serie
        detalle = obtener_detalle_serie(tmdb_id)
        if detalle:
            serie = Serie.objects.create(
                tmdb_id=detalle['tmdb_id'],
                titulo=detalle['titulo'],
                descripcion=detalle['descripcion'],
                fecha_estreno=detalle['fecha_estreno'],
                imagen_url=detalle['imagen_url']
            )
    return serie

def agregar_desde_tmdb(request, tmdb_id):
    # This acts as the "Dejar reseña" action: prepares DB and redirects to detail
    serie = _obtener_o_crear_serie_tmdb(tmdb_id)
    if serie:
        return redirect('detalle_serie', serie_id=serie.id)
    return redirect('home')

@login_required
def agregar_catalogo_personal(request, tmdb_id):
    serie = _obtener_o_crear_serie_tmdb(tmdb_id)
    if serie:
        serie.usuarios_que_guardaron.add(request.user)
    
    # Redirect back
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('home')

@login_required
def perfil_usuario_view(request):
    series_guardadas = request.user.series_guardadas.all()
    resenas = request.user.resena_set.all()
    return render(request, 'reviews/perfil.html', {
        'series_guardadas': series_guardadas,
        'resenas': resenas
    })

