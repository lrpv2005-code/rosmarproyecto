import requests
from django.conf import settings

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def get_headers():
    return {
        'Authorization': f'Bearer {settings.TMDB_ACCESS_TOKEN}',
        'accept': 'application/json'
    }

def buscar_series(query):
    """Busca series y películas en TMDB por nombre."""
    if not query:
        return []
    
    url = f"{TMDB_BASE_URL}/search/multi"
    params = {
        'query': query,
        'language': 'es-ES', # Prefer Spanish results
        'page': 1
    }
    
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        response.raise_for_status()
        data = response.json()
        
        resultados = []
        for item in data.get('results', []):
            if item.get('media_type') not in ['tv', 'movie']:
                continue
            # Formatear la imagen si existe
            poster_path = item.get('poster_path')
            imagen_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None
            
            titulo = item.get('name') if item.get('media_type') == 'tv' else item.get('title')
            fecha_estreno = item.get('first_air_date') if item.get('media_type') == 'tv' else item.get('release_date')
            
            ultima_fecha_estreno = None
            if item.get('media_type') == 'tv':
                detalles = obtener_detalle_serie(item.get('id'), 'tv')
                if detalles and detalles.get('seasons'):
                    seasons = detalles['seasons']
                    if seasons:
                        ultima_fecha_estreno = seasons[-1].get('fecha_estreno')
            
            resultados.append({
                'tmdb_id': item.get('id'),
                'titulo': titulo,
                'descripcion': item.get('overview'),
                'fecha_estreno': fecha_estreno,
                'ultima_fecha_estreno': ultima_fecha_estreno,
                'imagen_url': imagen_url,
                'media_type': item.get('media_type')
            })
        return resultados
    except requests.RequestException as e:
        print(f"Error al buscar en TMDB: {e}")
        return []

def obtener_detalle_serie(tmdb_id, media_type='tv'):
    """Obtiene los detalles completos de una serie o película desde TMDB."""
    url = f"{TMDB_BASE_URL}/{media_type}/{tmdb_id}"
    params = {
        'language': 'es-ES'
    }
    
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        response.raise_for_status()
        item = response.json()
        
        poster_path = item.get('poster_path')
        imagen_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None
        
        # Some TMDB responses have empty dates
        fecha_estreno = item.get('first_air_date')
        if not fecha_estreno:
            fecha_estreno = None
            
        # Parse seasons for tv shows
        seasons = []
        if media_type == 'tv':
            for season in item.get('seasons', []):
                # Skip season 0 (Specials) if preferred, or include it
                season_poster = season.get('poster_path')
                seasons.append({
                    'nombre': season.get('name'),
                    'episodios': season.get('episode_count'),
                    'fecha_estreno': season.get('air_date'),
                    'descripcion': season.get('overview'),
                    'imagen_url': f"{TMDB_IMAGE_BASE_URL}{season_poster}" if season_poster else None,
                    'calificacion': season.get('vote_average')
                })
            
        return {
            'tmdb_id': item.get('id'),
            'titulo': item.get('name') if media_type == 'tv' else item.get('title'),
            'descripcion': item.get('overview', 'Sin descripción.'),
            'fecha_estreno': fecha_estreno if media_type == 'tv' else item.get('release_date'),
            'imagen_url': imagen_url,
            'seasons': seasons
        }
    except requests.RequestException as e:
        print(f"Error al obtener detalle en TMDB: {e}")
        return None

def _fetch_media_list(endpoint, media_type):
    url = f"{TMDB_BASE_URL}{endpoint}"
    params = {'language': 'es-ES', 'page': 1}
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        response.raise_for_status()
        data = response.json()
        
        resultados = []
        for item in data.get('results', [])[:10]: # Limitar a 10 para no saturar la API
            poster_path = item.get('poster_path')
            imagen_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None
            
            ultima_fecha_estreno = None
            if media_type == 'tv':
                detalles = obtener_detalle_serie(item.get('id'), 'tv')
                if detalles and detalles.get('seasons'):
                    seasons = detalles['seasons']
                    if seasons:
                        ultima_fecha_estreno = seasons[-1].get('fecha_estreno')
                        
            resultados.append({
                'tmdb_id': item.get('id'),
                'titulo': item.get('name') if media_type == 'tv' else item.get('title'),
                'descripcion': item.get('overview'),
                'fecha_estreno': item.get('first_air_date') if media_type == 'tv' else item.get('release_date'),
                'ultima_fecha_estreno': ultima_fecha_estreno,
                'imagen_url': imagen_url,
                'media_type': media_type
            })
        return resultados
    except requests.RequestException as e:
        print(f"Error al obtener lista {endpoint} en TMDB: {e}")
        return []

def obtener_populares(media_type="tv"):
    return _fetch_media_list(f"/{media_type}/popular", media_type)

def obtener_estrenos(media_type="tv"):
    endpoint = "/tv/airing_today" if media_type == "tv" else "/movie/now_playing"
    return _fetch_media_list(endpoint, media_type)

def obtener_prontas_estrenar(media_type="tv"):
    endpoint = "/tv/on_the_air" if media_type == "tv" else "/movie/upcoming"
    return _fetch_media_list(endpoint, media_type)

def obtener_trailers_prontas_estrenar(media_type="tv"):
    endpoint = "/tv/on_the_air" if media_type == "tv" else "/movie/upcoming"
    url = f"{TMDB_BASE_URL}{endpoint}"
    params = {'language': 'es-ES', 'page': 1}
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        response.raise_for_status()
        data = response.json()
        
        resultados = []
        for item in data.get('results', [])[:10]: # Limitar a 10 para no saturar la API
            tmdb_id = item.get('id')
            
            # Obtener videos para el item
            videos_url = f"{TMDB_BASE_URL}/{media_type}/{tmdb_id}/videos"
            v_params = {'language': 'es-ES'}
            
            trailer_key = None
            try:
                v_resp = requests.get(videos_url, headers=get_headers(), params=v_params)
                v_resp.raise_for_status()
                v_data = v_resp.json()
                
                # Buscar trailer en español
                for v in v_data.get('results', []):
                    if v.get('site') == 'YouTube' and v.get('type') == 'Trailer':
                        trailer_key = v.get('key')
                        break
                
                # Si no hay trailer en español, buscar en inglés
                if not trailer_key:
                    v_params_en = {'language': 'en-US'}
                    v_resp_en = requests.get(videos_url, headers=get_headers(), params=v_params_en)
                    v_data_en = v_resp_en.json()
                    for v in v_data_en.get('results', []):
                        if v.get('site') == 'YouTube' and v.get('type') == 'Trailer':
                            trailer_key = v.get('key')
                            break
            except requests.RequestException:
                pass # Si falla al obtener el trailer, ignorar
                
            # Preferir backdrop_path para un aspecto de trailer horizontal
            backdrop_path = item.get('backdrop_path')
            poster_path = item.get('poster_path')
            imagen_url = f"{TMDB_IMAGE_BASE_URL}{backdrop_path}" if backdrop_path else (f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None)
            
            resultados.append({
                'tmdb_id': tmdb_id,
                'titulo': item.get('name') if media_type == 'tv' else item.get('title'),
                'descripcion': item.get('overview'),
                'fecha_estreno': item.get('first_air_date') if media_type == 'tv' else item.get('release_date'),
                'imagen_url': imagen_url,
                'media_type': media_type,
                'trailer_key': trailer_key
            })
        return resultados
    except requests.RequestException as e:
        print(f"Error al obtener trailers {endpoint} en TMDB: {e}")
        return []
