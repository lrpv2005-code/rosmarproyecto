import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from reviews.models import Serie
from django.contrib.auth.models import User

def populate():
    if Serie.objects.count() == 0:
        print("Poblando Base de Datos...")
        series = [
            {
                'titulo': 'Breaking Bad',
                'descripcion': 'Un profesor de química diagnosticado con cáncer inoperable de pulmón se asocia con un antiguo alumno para cocinar y vender metanfetamina para asegurar el futuro financiero de su familia antes de su muerte.',
                'fecha_estreno': date(2008, 1, 20),
                'imagen_url': 'https://m.media-amazon.com/images/I/71X1EVoN0DL._AC_SL1200_.jpg'
            },
            {
                'titulo': 'Stranger Things',
                'descripcion': 'Cuando un niño desaparece, un pequeño pueblo descubre un misterio que involucra experimentos secretos, fuerzas sobrenaturales aterradoras y a una niña extraña.',
                'fecha_estreno': date(2016, 7, 15),
                'imagen_url': 'https://m.media-amazon.com/images/M/MV5BMDZkYmVhNjMtNWU4MC00MDQxLWE3MjYtZGMzZWI1ZjhlOWJmXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg'
            },
            {
                'titulo': 'Dark',
                'descripcion': 'Una saga familiar con un toque sobrenatural, situada en un pueblo alemán, donde la desaparición de dos niños pequeños expone las relaciones rotas entre cuatro familias.',
                'fecha_estreno': date(2017, 12, 1),
                'imagen_url': 'https://m.media-amazon.com/images/M/MV5BMzA2NDkwODAwM15BMl5BanBnXkFtZTgwODk5MTgzMDI@._V1_.jpg'
            },
            {
                'titulo': 'The Office',
                'descripcion': 'Un documental falso sobre un grupo de oficinistas típicos, donde la jornada laboral consiste en choques de ego, comportamiento inapropiado y tedio.',
                'fecha_estreno': date(2005, 3, 24),
                'imagen_url': 'https://m.media-amazon.com/images/M/MV5BMDNkOTE4NDQtMTNmYi00MWE0LWE4ZTktYTc0NzhhNWIzNzQ4XkEyXkFqcGdeQXVyMzgwMTE1NTQ@._V1_FMjpg_UX1000_.jpg'
            }
        ]
        
        for s in series:
            Serie.objects.create(**s)
        print("¡Series creadas exitosamente!")

if __name__ == '__main__':
    populate()
