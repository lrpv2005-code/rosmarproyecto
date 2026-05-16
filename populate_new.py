import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from reviews.models import Serie, Resena
from django.contrib.auth.models import User

def populate():
    print("Borrando base de datos antigua...")
    Serie.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    print("Insertando series nuevas con imágenes locales...")
    series = [
        {
            'titulo': 'Breaking Bad',
            'descripcion': 'Un profesor de química diagnosticado con cáncer inoperable de pulmón se asocia con un antiguo alumno para cocinar y vender metanfetamina.',
            'fecha_estreno': date(2008, 1, 20),
            'imagen_url': '/static/imagenes/breaking.jpg'
        },
        {
            'titulo': 'Brooklyn Nine-Nine',
            'descripcion': 'Jake Peralta, un inmaduro pero talentoso detective del precinto 99 de la policía de Nueva York, entra en conflicto con su nuevo oficial al mando.',
            'fecha_estreno': date(2013, 9, 17),
            'imagen_url': '/static/imagenes/brooklyn99.jpg'
        },
        {
            'titulo': 'Dark',
            'descripcion': 'Una saga familiar con un toque sobrenatural, situada en un pueblo alemán, sobre la desaparición de dos niños.',
            'fecha_estreno': date(2017, 12, 1),
            'imagen_url': '/static/imagenes/dark.jpg'
        },
        {
            'titulo': 'The Amazing Digital Circus',
            'descripcion': 'Una mujer, junto con otros cincos humanos, queda atrapada en un mundo virtual disparatado comandado por una IA rebelde.',
            'fecha_estreno': date(2023, 10, 13),
            'imagen_url': '/static/imagenes/digitalcircus.jpg'
        },
        {
            'titulo': 'Your Lie in April',
            'descripcion': 'Un prodigio del piano pierde su habilidad para tocar tras una tragedia familiar hasta que conoce a una misteriosa violinista.',
            'fecha_estreno': date(2014, 10, 9),
            'imagen_url': '/static/imagenes/lie inapril.jpg'
        },
        {
            'titulo': 'La Reina del Flow',
            'descripcion': 'Tras pasar diecisiete años en la cárcel injustamente, una talentosa compositora de reguetón busca vengarse de los hombres que la hundieron.',
            'fecha_estreno': date(2018, 6, 12),
            'imagen_url': '/static/imagenes/reinadelflow.jpg'
        },
        {
            'titulo': 'Shameless',
            'descripcion': 'La cruda, loca e hilarante vida de la familia obrera Gallagher, donde el patriarca Frank es un alcohólico desastroso.',
            'fecha_estreno': date(2011, 1, 9),
            'imagen_url': '/static/imagenes/shameless.jpg'
        },
        {
            'titulo': 'Better Call Saul',
            'descripcion': 'Las pruebas y tribulaciones del abogado criminalista Jimmy McGill en el tiempo previo al establecimiento de su destartalada oficina en Albuquerque.',
            'fecha_estreno': date(2015, 2, 8),
            'imagen_url': '/static/imagenes/soulgoodman.jpg'
        },
        {
            'titulo': 'Suits',
            'descripcion': 'Mike Ross, un joven brillante que abandonó la universidad, empieza a trabajar con el exitoso abogado de Manhattan, Harvey Specter, y finge haberse graduado de Harvard.',
            'fecha_estreno': date(2011, 6, 23),
            'imagen_url': '/static/imagenes/suits.jpg'
        },
        {
            'titulo': 'The Office',
            'descripcion': 'Un falso documental sobre el día a día de unos mediocres pero divertidos oficinistas, en Dunder Mifflin.',
            'fecha_estreno': date(2005, 3, 24),
            'imagen_url': '/static/imagenes/theofice.jpg'
        }, 
    ]
    
    for s in series:
        Serie.objects.create(**s)
    print("¡Las 10 nuevas series fueron agregadas al catálogo/menú exitosamente!")

if __name__ == '__main__':
    populate()
