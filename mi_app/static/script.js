// Función para inicializar gráficos
function initializeCharts(data) {
    // Gráfico de Tiempo de Carga
    new Chart(document.getElementById('loadTimeChart'), {
        type: 'bar',
        data: {
            labels: [data.url || 'Sitio web'],
            datasets: [{
                label: 'Tiempo de carga (ms)',
                data: [data.tiempo_carga],
                backgroundColor: 'rgba(54, 162, 235, 0.7)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfico de Solicitudes HTTP
    new Chart(document.getElementById('requestsChart'), {
        type: 'pie',
        data: {
            labels: ['HTML', 'CSS', 'JavaScript', 'Imágenes', 'Fuentes', 'Otros'],
            datasets: [{
                data: [
                    data.solicitudes.html,
                    data.solicitudes.css,
                    data.solicitudes.js,
                    data.solicitudes.imagenes,
                    data.solicitudes.fuentes,
                    data.solicitudes.otros
                ],
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                ]
            }]
        },
        options: {
            responsive: true
        }
    });

    // Gráfico de Desglose de Tiempos
    if (data.desglose_tiempos) {
        new Chart(document.getElementById('timingBreakdownChart'), {
            type: 'doughnut',
            data: {
                labels: Object.keys(data.desglose_tiempos),
                datasets: [{
                    data: Object.values(data.desglose_tiempos),
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                    ]
                }]
            },
            options: {
                responsive: true
            }
        });
    }
}

// Cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si hay datos para mostrar
    const rawData = document.getElementById('chart-data')?.textContent || 'null';
    
    if (rawData && rawData !== 'null') {
        try {
            const data = JSON.parse(rawData);
            initializeCharts(data);
        } catch (e) {
            console.error('Error al parsear datos:', e);
        }
    }

    // Validación del formulario
    document.getElementById('uploadForm')?.addEventListener('submit', function(e) {
        const fileInput = document.getElementById('jsonFile');
        if (fileInput.files.length === 0) {
            alert('Por favor selecciona un archivo JSON');
            e.preventDefault();
        }
    });
});