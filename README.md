# DASHBOARD DE MÉTRICAS DE RENDIMIENTO WEB

## Descripción del Proyecto

Este es pequeño proyecto donde desarrollamos un app web de métricas sobre otras app web que devuelve estadísticas de rendimiento al ingresar un archivo .json. Aplicamos metodologías ágiles como **Scrum** y **Extreme Programming (XP)**, usamos **GitHub** para el control de versiones y colaboración, y configuramos **Integración Continua (CI)** para ejecutar pruebas automáticamente con cada cambio.

---

## Integrantes del equipo y roles Scrum

| Nombre            |    Rol Scrum               |
|-------------------|  --------------------------|
| Jorge Huillca     |   PO y Scrum Master        |
| Fernando Julca    |   Developer BackEnd        |
| Dayana Carrión    |   Developer FrontEnd       |
| Diego Galiano     | Developer FrontEnd         |

---

## Instalación y ejecución del proyecto

  ### Requisitos
  - Python 3.12.10
  - Django 5.2.4
  - asgiref==3.9.1
  - colorama==0.4.6
  - iniconfig==2.1.0
  - packaging==25.0
  - pluggy==1.6.0
  - Pygments==2.19.2
  - pytest==8.4.1
  - sqlparse==0.5.3
  - tzdata==2025.2


  ## Instalación
  ```bash
  git clone https://github.com/fernando-jp14/Dashboard-metricas-rendimientoweb.git
  cd "nombre de tu carpeta"/Dashboard-metricas-redimientoweb
  python -m venv venv
  .\venv\Scripts\activate
  pip install -r requirements.txt
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  ```
## Evidencias de Scrum
- Desarrollado en TRELLO:
https://trello.com/invite/b/687e68fb88aab73bfebe3f70/ATTI7159094debcb426c4b3179655b6800cbB52F11BD/scrum-xp-grupo-1

## Estrcutura del Repositorio:

  -.github/workflows
  -config
  -mi_app
  -.gitignore
  -README.md
  -manage.py
  -requirements.txt

