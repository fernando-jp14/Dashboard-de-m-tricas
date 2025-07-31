from django.shortcuts import render
from .models import WebPerformance
import json
import logging
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

def parse_json_file(file):
    try:
        content = file.read().decode('utf-8')
        return json.loads(content)
    except UnicodeDecodeError:
        raise ValueError("El archivo no está codificado en UTF-8.")
    except json.JSONDecodeError:
        raise ValueError("El contenido del archivo no es un JSON válido.")

def create_metric_from_data(data):
    request_types = data.get('requestTypes', {})
    return WebPerformance(
        url=data.get('url', ''),
        tiempo_carga=data.get('loadTime', 0),
        desglose_tiempos=data.get('timingBreakdown', {}),
        uso_memoria=data.get('memoryUsage', 0),
        solicitudes_html=request_types.get('HTML', 0),
        solicitudes_css=request_types.get('CSS', 0),
        solicitudes_js=request_types.get('JavaScript', 0),
        solicitudes_imagenes=request_types.get('Imagenes', 0),
        solicitudes_fuentes=request_types.get('Fuentes', 0),
        solicitudes_otros=request_types.get('Otros', 0)
    )

@require_http_methods(["GET", "POST"])
def upload_json(request):
    context = {
        'metrics': WebPerformance.objects.all().order_by('-fecha')[:10]
    }

    if request.method == 'POST':
        json_file = request.FILES.get('json_file')

        if not json_file:
            context['error'] = "⚠️ Por favor, selecciona un archivo JSON."
            return render(request, 'index.html', context)

        try:
            data = parse_json_file(json_file)
            metric = create_metric_from_data(data)
            metric.save()

            # Calcular total de solicitudes
            total_solicitudes = (
                metric.solicitudes_html +
                metric.solicitudes_css +
                metric.solicitudes_js +
                metric.solicitudes_imagenes +
                metric.solicitudes_fuentes +
                metric.solicitudes_otros
            )

            context.update({
                'success': '✅ Archivo JSON procesado correctamente.',
                'metrics': [metric],
                'json_data': json.dumps({
                    'url': metric.url,
                    'tiempo_carga': metric.tiempo_carga,
                    'uso_memoria': metric.uso_memoria,
                    'solicitudes': {
                        'html': metric.solicitudes_html,
                        'css': metric.solicitudes_css,
                        'js': metric.solicitudes_js,
                        'imagenes': metric.solicitudes_imagenes,
                        'fuentes': metric.solicitudes_fuentes,
                        'otros': metric.solicitudes_otros,
                        'total': total_solicitudes
                    },
                    'desglose_tiempos': metric.desglose_tiempos
                }, indent=2)
            })

        except ValueError as ve:
            context['error'] = f"⚠️ {str(ve)}"
        except Exception as e:
            logger.error(f"❌ Error inesperado al procesar el archivo JSON: {e}")
            context['error'] = "❌ Ocurrió un error inesperado al procesar el archivo."

    return render(request, 'index.html', context)
