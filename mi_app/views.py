from django.shortcuts import render
from .models import WebPerformance
import json

def upload_json(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']
        
        try:
            data = json.loads(json_file.read().decode('utf-8'))
            
            metric = WebPerformance(
                url=data.get('url', ''),
                tiempo_carga=data.get('loadTime', 0),
                desglose_tiempos=data.get('timingBreakdown', {}),
                uso_memoria=data.get('memoryUsage', 0),
                solicitudes_html=data.get('requestTypes', {}).get('HTML', 0),
                solicitudes_css=data.get('requestTypes', {}).get('CSS', 0),
                solicitudes_js=data.get('requestTypes', {}).get('JavaScript', 0),
                solicitudes_imagenes=data.get('requestTypes', {}).get('Imagenes', 0),
                solicitudes_fuentes=data.get('requestTypes', {}).get('Fuentes', 0),
                solicitudes_otros=data.get('requestTypes', {}).get('Otros', 0)
            )
            metric.save()
            
            # Preparar los datos para el gráfico (formato compatible con script.js)
            json_data = json.dumps({
                'url': metric.url,
                'tiempo_carga': metric.tiempo_carga,
                'desglose_tiempos': metric.desglose_tiempos,
                'solicitudes': {
                    'html': metric.solicitudes_html,
                    'css': metric.solicitudes_css,
                    'js': metric.solicitudes_js,
                    'imagenes': metric.solicitudes_imagenes,
                    'fuentes': metric.solicitudes_fuentes,
                    'otros': metric.solicitudes_otros
                }
            })

            return render(request, 'index.html', {
                'metrics': [metric],
                'json_data': json_data,
                'success': 'Archivo JSON procesado correctamente'
            })
        
        except json.JSONDecodeError:
            return render(request, 'index.html', {
                'error': 'El archivo no es un JSON válido',
                'metrics': WebPerformance.objects.all().order_by('-fecha')[:10]
            })
        
        except Exception as e:
            return render(request, 'index.html', {
                'error': f'Error procesando el archivo: {str(e)}',
                'metrics': WebPerformance.objects.all().order_by('-fecha')[:10]
            })
    
    # Si es GET o no se subió archivo
    return render(request, 'index.html', {
        'metrics': WebPerformance.objects.all().order_by('-fecha')[:10]
    })




