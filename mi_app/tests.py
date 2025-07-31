from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from .models import WebPerformance
from django.utils import timezone
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import json
#test model



class WebPerformanceModelTest(TestCase):

    def setUp(self):
        self.web_perf = WebPerformance.objects.create(
            url="https://ejemplo.com",
            tiempo_carga=1234.56,
            desglose_tiempos={
                "DOM Load": 400,
                "Page Load": 834.56
            },
            uso_memoria=75.3,
            solicitudes_html=1,
            solicitudes_css=2,
            solicitudes_js=3,
            solicitudes_imagenes=4,
            solicitudes_fuentes=1,
            solicitudes_otros=0
        )

    def test_str_representation(self):
        fecha_formateada = self.web_perf.fecha.strftime('%Y-%m-%d')
        esperado = f"https://ejemplo.com - 1234.56ms - {fecha_formateada}"
        self.assertEqual(str(self.web_perf), esperado)

    def test_total_solicitudes(self):
        self.assertEqual(self.web_perf.total_solicitudes, 11)

    def test_desglose_tiempos_is_dict(self):
        self.assertIsInstance(self.web_perf.desglose_tiempos, dict)
        self.assertIn("DOM Load", self.web_perf.desglose_tiempos)

    def test_creacion_exitosa(self):
        self.assertIsInstance(self.web_perf, WebPerformance)
        self.assertEqual(self.web_perf.url, "https://ejemplo.com")
        self.assertGreater(self.web_perf.uso_memoria, 0)



#test views.py
class UploadJsonViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('upload_json') 

        self.valid_data = {
            "url": "https://ejemplo.com",
            "loadTime": 1500,
            "memoryUsage": 80.2,
            "timingBreakdown": {
                "DOM Load": 500,
                "Page Load": 1000
            },
            "requestTypes": {
                "HTML": 1,
                "CSS": 2,
                "JavaScript": 3,
                "Imagenes": 4,
                "Fuentes": 0,
                "Otros": 1
            }
        }


    # uni
    def test_get_request_returns_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_post_valid_json_creates_metric(self):
        json_bytes = json.dumps(self.valid_data).encode('utf-8')
        json_file = SimpleUploadedFile("metric.json", json_bytes, content_type="application/json")

        response = self.client.post(self.url, {'json_file': json_file}, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, " Archivo JSON procesado correctamente.")
        self.assertEqual(WebPerformance.objects.count(), 1)

        metric = WebPerformance.objects.first()
        self.assertEqual(metric.url, self.valid_data['url'])
        self.assertEqual(metric.tiempo_carga, self.valid_data['loadTime'])
        self.assertEqual(metric.uso_memoria, self.valid_data['memoryUsage'])

    def test_post_empty_file_shows_error(self):
        response = self.client.post(self.url, {}, follow=True)
        self.assertContains(response, " Por favor, selecciona un archivo JSON.")
        self.assertEqual(WebPerformance.objects.count(), 0)

    def test_post_invalid_json_shows_error(self):
        invalid_file = SimpleUploadedFile("invalid.json", b"{no valido}", content_type="application/json")

        response = self.client.post(self.url, {'json_file': invalid_file}, follow=True)
        self.assertContains(response, "El contenido del archivo no es un JSON válido.")
        self.assertEqual(WebPerformance.objects.count(), 0)