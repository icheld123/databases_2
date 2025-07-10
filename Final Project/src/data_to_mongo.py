import os
import json
import base64
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

libros_txt_path = os.path.join(os.getcwd(), "libros_formateados.txt")
output_dir = os.path.join(os.getcwd(), "libros")
os.makedirs(output_dir, exist_ok=True)

# Leer el archivo libros.txt y parsear cada línea usando regex para extraer los campos entre comillas
books = []
with open(libros_txt_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        # Ignorar líneas de comentarios (por ejemplo, que comienzan con "//")
        if line.startswith("//"):
            continue
        if line:
            # Extrae todos los contenidos entre comillas
            fields = re.findall(r'"([^"]+)"', line)
            if len(fields) >= 3:
                id_value = fields[0]
                name_value = fields[1]
                has_audio = fields[2].lower() == "true"
                books.append({
                    "id": id_value,
                    "name": name_value,
                    "has_audio": has_audio
                })

# Función para generar un nombre de archivo seguro reemplazando espacios y caracteres especiales por guion bajo
def generar_nombre_seguro(nombre):
    nombre = nombre.replace(" ", "_")
    nombre_seguro = re.sub(r'[^A-Za-z0-9_]+', '_', nombre)
    return nombre_seguro

# Para cada libro, se crea un PDF
for book in books:
    safe_name = generar_nombre_seguro(book["name"])
    pdf_file_name = safe_name + ".pdf"
    pdf_file_path = os.path.join(output_dir, pdf_file_name)
    
    # Crear PDF usando ReportLab
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, f"ID: {book['id']}")
    c.drawString(100, height - 120, f"Nombre: {book['name']}")
    c.save()
    print(f"PDF '{pdf_file_path}' creado con éxito.")

# Cargar el contenido Base64 del MP3 fijo desde el archivo base64amp3.txt
audio_base64_path = r"base64amp3.txt"
with open(audio_base64_path, 'r', encoding='utf-8') as af:
    audio_base64 = af.read().strip()

# Generar JSON con la estructura que incluya ambos formatos bajo la misma id
books_data = []
for book in books:
    safe_name = generar_nombre_seguro(book["name"])
    pdf_file_name = safe_name + ".pdf"
    pdf_file_path = os.path.join(output_dir, pdf_file_name)
    with open(pdf_file_path, 'rb') as f:
        pdf_content = f.read()
    encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

    entry = {
        "id": book["id"],
        "name": book["name"],
        "formats": {
            "pdf": {
                "fileName": pdf_file_name,
                "content": encoded_pdf,
                "format": "pdf"
            }
        }
    }
    
    # Si el libro tiene audiolibro, usar siempre el contenido Base64 cargado
    if book["has_audio"]:
        audio_file_name = safe_name + ".mp3"
        entry["formats"]["audio"] = {
            "fileName": audio_file_name,
            "content": audio_base64,
            "format": "mp3"
        }
    
    books_data.append(entry)

json_file_path = os.path.join(os.getcwd(), "libros_completo.json")
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(books_data, json_file, indent=4, ensure_ascii=False)
print(f"Archivo JSON '{json_file_path}' creado con éxito.")