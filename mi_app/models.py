from django.db import models
from django.utils import timezone

class WebPerformance(models.Model):
    # Información básica
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de medición")
    url = models.URLField(max_length=500, verbose_name="URL analizada")
    
    # Tiempo de carga y desglose
    tiempo_carga = models.FloatField(verbose_name="Tiempo de Carga (ms)")
    
    # Desglose de tiempos (almacenado como JSON)
    desglose_tiempos = models.JSONField(verbose_name="Desglose de Tiempos", default=dict)
    
    # Uso de memoria
    uso_memoria = models.FloatField(verbose_name="Uso de Memoria (MB)")
    
    # Solicitudes HTTP por tipo
    solicitudes_html = models.IntegerField(verbose_name="Solicitudes HTML", default=0)
    solicitudes_css = models.IntegerField(verbose_name="Solicitudes CSS", default=0)
    solicitudes_js = models.IntegerField(verbose_name="Solicitudes JavaScript", default=0)
    solicitudes_imagenes = models.IntegerField(verbose_name="Solicitudes de Imágenes", default=0)
    solicitudes_fuentes = models.IntegerField(verbose_name="Solicitudes de Fuentes", default=0)
    solicitudes_otros = models.IntegerField(verbose_name="Otras Solicitudes", default=0)
    
    class Meta:
        verbose_name = "Métrica de Rendimiento"
        verbose_name_plural = "Métricas de Rendimiento"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.url} - {self.tiempo_carga}ms - {self.fecha.strftime('%Y-%m-%d')}"
    
    @property
    def total_solicitudes(self):
        """Calcula el total de solicitudes HTTP"""
        return (
            self.solicitudes_html +
            self.solicitudes_css +
            self.solicitudes_js +
            self.solicitudes_imagenes +
            self.solicitudes_fuentes +
            self.solicitudes_otros
        )
