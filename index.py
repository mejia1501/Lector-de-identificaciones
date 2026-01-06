import cv2
from PIL import Image
from matplotlib import pyplot as plt
import pytesseract
from datetime import datetime
import re

def noise_removal(image):
  import numpy as np
  kernel = np.ones((1,1),np.uint8)
  image = cv2.dilate(image,kernel,iterations=1)
  kernel = np.ones((1, 1),np.uint8)
  image = cv2.erode(image,kernel,iterations=1)
  image = cv2.morphologyEx(image,cv2.MORPH_CLOSE,kernel)
  image = cv2.medianBlur(image,3)
  return (image)

image_file = 'path_to_your_image.jpg'  # Reemplaza con la ruta de tu imagen
img = cv2.imread(image_file)
no_noise = noise_removal( img )

ocr_result = pytesseract.image_to_string(no_noise)

caracteres_a_eliminar = "."
tabla_traduccion = str.maketrans(' ', ' ', caracteres_a_eliminar)
nuevo_texto = ocr_result.translate(tabla_traduccion)
print(nuevo_texto)

anio_actual = datetime.now().year
limite_superior = anio_actual + 10


def extraer_cedula_y_vencimiento(texto, min_year, max_year):
    """Extrae la cédula (preferentemente tras 'V') y el año de vencimiento.

    Parámetros:
    - texto: str
    - min_year, max_year: rango absoluto aceptable para años.

    Retorna (cedula, año_str, estado) donde:
      - año_str: texto con el año encontrado o None
      - estado: 'Vencido' si el año < año actual, 'Vigente' si está entre el año actual y max_year,
                o None si no se encontró año válido (o era > max_year).
    """
    anio_actual = datetime.now().year

    # 1) Priorizar patrón "V 12345678" o "V12345678" (acepta 'V', 'V.' y separadores variados)
    m = re.search(r"\bV\.?[:\s\-]*?(\d{6,9})\b", texto, re.I)
    if m:
        cedula = m.group(1)
        rest = texto[m.end(1):]
    else:
        # 2) Luego intentar etiquetas comunes (incluye variantes como IDENTIDAD y CEBULA)
        m2 = re.search(r"\b(?:ID|IDENTIDAD|C[ée]dula|CEDULA|CEBULA)[:\s]*?(\d{6,9})\b", texto, re.I)
        if m2:
            cedula = m2.group(1)
            rest = texto[m2.end(1):]
        else:
            # 3) Fallback: cualquier secuencia de 6-9 dígitos en el texto
            m3 = re.search(r"\b(\d{6,9})\b", texto)
            if not m3:
                return None, None, None
            cedula = m3.group(1)
            rest = texto[m3.end(1):]

    # Buscar cualquier secuencia de 4 dígitos en el texto restante (ventanas superpuestas)
    fe_vencimiento = None
    estado = None
    for mm in re.finditer(r'(?=(\d{4}))', rest):
        s = mm.group(1)
        try:
            posible = int(s)
        except ValueError:
            continue
        print(f'Año posible: {posible}')

        # Ignorar años fuera del rango absoluto
        if not (posible <= max_year):
            continue

        # Si el año es menor al actual -> vencido
        if posible < anio_actual:
            fe_vencimiento = s
            estado = 'Vencido'
            continue

        # Año entre actual y max_year -> vigente
        if anio_actual <= posible <= max_year:
            fe_vencimiento = s
            estado = 'Vigente'
            break

    # Si no se encontró en el resto, buscar en todo el texto como fallback
    if fe_vencimiento is None:
        for mm in re.finditer(r'(?=(\d{4}))', texto):
            s = mm.group(1)
            try:
                posible = int(s)
            except ValueError:
                continue
            if not (posible <= max_year):
                continue
            if posible < anio_actual:
                fe_vencimiento = s
                estado = 'Vencido'
                continue
            if anio_actual <= posible <= max_year:
                fe_vencimiento = s
                estado = 'Vigente'
                break

    return cedula, fe_vencimiento, estado


ced, venc, estado = extraer_cedula_y_vencimiento(nuevo_texto, anio_actual, limite_superior)
print('--- RESULTADOS ---')
print(f'Cédula: {ced}')
if venc is None:
    print('Año de Vencimiento: No encontrado o fuera de rango')
else:
    print(f'Año de Vencimiento: {venc} ({estado})')