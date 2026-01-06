# Proyecto: Extracción de cédula y vencimiento desde imagen

Descripción
- Este script procesa una imagen que contiene una cédula de identidad, aplica eliminación de ruido y extrae texto mediante OCR (Tesseract). A partir del texto detectado intenta identificar el número de cédula y el año de vencimiento, indicando si está vigente o vencido.

Archivos principales
- [index.py](index.py): script principal que realiza la lectura de imagen, preprocesado y extracción de cédula y fecha de vencimiento.
- [requirements.txt](requirements.txt): dependencias Python que el proyecto utiliza.

Requisitos
- Python 3.8+.
- Instalar Tesseract OCR en el sistema (motor nativo). En Windows puedes descargarlo desde: https://github.com/tesseract-ocr/tesseract
- Instalar dependencias Python:

```bash
pip install -r requirements.txt
```

Uso
- Edita `index.py` y reemplaza la variable `image_file` por la ruta de tu imagen.
- Ejecuta:

```bash
python index.py
```

Salida esperada
- El script imprimirá el texto extraído por OCR y, bajo `--- RESULTADOS ---`, mostrará la cédula detectada, el año de vencimiento (si se encuentra) y su estado (`Vigente` o `Vencido`).

Notas sobre el código y atribución
- Parte de los fundamentos y técnicas de preprocesado y uso básico de Tesseract (por ejemplo la función de preprocesado/noise_removal y la llamada a `pytesseract.image_to_string`) se basaron en la siguiente playlist didáctica para los fundamentos de OCR e imagen: https://www.youtube.com/playlist?list=PL2VXyKi-KpYuTAZz__9KVl1jQz74bDG7i
- El resto del código corresponde a la lógica de extracción y heurísticas de identificación de cédula y año implementada en `index.py`.

Mejoras sugeridas
- Ajustar el preprocesado (kernels, umbrales) para la calidad específica de tus imágenes.
- Añadir manejo de múltiples formatos de fecha y formatos locales de cédula.
- Guardar resultados en un archivo CSV o base de datos para procesado en lote.
