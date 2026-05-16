from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Serie(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_estreno = models.DateField(null=True, blank=True)
    imagen_url = models.URLField(blank=True, null=True, help_text="URL de la imagen de portada")
    imagen_respaldo = models.CharField(max_length=200, blank=True, null=True, help_text="Ruta a imagen local de respaldo")
    tmdb_id = models.IntegerField(null=True, blank=True, help_text="ID de TMDB")
    tipo = models.CharField(max_length=10, default='tv', help_text="tv o movie")
    usuarios_que_guardaron = models.ManyToManyField(User, related_name='series_guardadas', blank=True)

    class Meta:
        unique_together = ('tmdb_id', 'tipo')

    def __str__(self):
        return self.titulo
    
    @property
    def promedio_calificacion(self):
        promedio = self.resenas.aggregate(models.Avg('calificacion'))['calificacion__avg']
        if promedio:
            return round(promedio, 1)
        return 0

class Resena(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Calificación del 1 al 10"
    )
    comentario = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('serie', 'usuario') # Un usuario sólo puede reseñar una vez una misma serie
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.username} - {self.serie.titulo} ({self.calificacion}/10)"
