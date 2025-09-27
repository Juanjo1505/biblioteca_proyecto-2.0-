# Proyecto: Análisis de Datos - Biblioteca

Este proyecto es una plantilla lista para ejecutar que cumple con el reto del Integrador Nivel 3.
Incluye:
- Módulo `preprocesamiento.py` con funciones para cargar y limpiar datos.
- Script principal `analisis.py` que responde preguntas analíticas.
- Datos de ejemplo en `data/libros.csv` y `data/prestamos.csv` (cada uno con >= 20 registros).
- `requirements.txt` con dependencias.

## Requisitos
- Python 3.8+
- pip

## Instalación rápida (Linux / macOS / Windows WSL)
```bash
python -m venv env
# activar el entorno:
# Linux/macOS: source env/bin/activate
# Windows: .\env\Scripts\activate
pip install -r requirements.txt
python analisis.py
```

## Qué hace el script `analisis.py`
1. Carga y limpia los datos de `data/libros.csv` y `data/prestamos.csv`.
2. Realiza:
   - Análisis de frecuencia (libro más prestado).
   - Promedio de días de préstamo por categoría.
   - Conteo de libros de un autor específicos que están prestados.
   - Conteos y filtros adicionales para mostrar múltiples resultados.
3. Imprime los resultados en consola.

## Estructura del proyecto
```
biblioteca_proyecto/
├─ data/
│  ├─ libros.csv
│  └─ prestamos.csv
├─ preprocesamiento.py
├─ analisis.py
├─ requirements.txt
└─ README.md
```

Si quieres, también puedo preparar un repositorio Git con Git Flow (branches, PR templates) — dime si lo quieres.
