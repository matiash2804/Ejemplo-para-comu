from pathlib import Path
import shutil
from datetime import datetime

# ============================================================
# CMSFJ - PREPARAR SITIO PARA GITHUB PAGES
#
# Este script:
# 1. NO modifica Images/
# 2. NO elimina Archivos/
# 3. Hace backup de los archivos originales
# 4. Copia las páginas a la raíz
# 5. Inicio.html pasa a llamarse index.html
# 6. Corrige ../Images/ por Images/
# ============================================================

ROOT = Path(__file__).resolve().parent
ARCHIVOS = ROOT / "Archivos"

# ------------------------------------------------------------
# ARCHIVOS QUE ESPERAMOS ENCONTRAR
# ------------------------------------------------------------

esperados = [
    "Inicio.html",
    "Mision.html",
    "Comunidad.html",
    "Oraciones.html",
    "style.css",
]

# ------------------------------------------------------------
# VERIFICACIONES ANTES DE TOCAR NADA
# ------------------------------------------------------------

print("\n============================================")
print(" CMSFJ - PREPARANDO GITHUB PAGES")
print("============================================\n")

print(f"Carpeta raíz:\n{ROOT}\n")

if not ARCHIVOS.exists():
    raise SystemExit(
        "ERROR: No existe la carpeta 'Archivos'.\n"
        "No se realizó ningún cambio."
    )

faltantes = [
    nombre
    for nombre in esperados
    if not (ARCHIVOS / nombre).exists()
]

if faltantes:
    print("ERROR: faltan archivos necesarios:\n")

    for archivo in faltantes:
        print(f" - {archivo}")

    raise SystemExit(
        "\nNo se realizó ningún cambio."
    )

# ------------------------------------------------------------
# CREAR BACKUP
# ------------------------------------------------------------

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

BACKUP = ROOT / f"BACKUP_ANTES_GITHUB_{timestamp}"
BACKUP.mkdir()

print("Creando backup...\n")

for nombre in esperados:
    origen = ARCHIVOS / nombre
    destino = BACKUP / nombre

    shutil.copy2(origen, destino)

    print(f"BACKUP: {nombre}")

print(f"\nBackup creado en:\n{BACKUP}\n")

# ------------------------------------------------------------
# FUNCIÓN PARA CORREGIR RUTAS
# ------------------------------------------------------------

def preparar_html(origen: Path, destino: Path):

    contenido = origen.read_text(encoding="utf-8")

    # Al mover el HTML desde /Archivos a la raíz:
    #
    # ../Images/xxxxx
    #
    # debe convertirse en:
    #
    # Images/xxxxx

    contenido = contenido.replace(
        "../Images/",
        "Images/"
    )

    # También contemplamos rutas Windows accidentales

    contenido = contenido.replace(
        "..\\Images\\",
        "Images/"
    )

    destino.write_text(
        contenido,
        encoding="utf-8"
    )

# ------------------------------------------------------------
# COPIAR HTML A LA RAÍZ
# ------------------------------------------------------------

mapa_html = {
    "Inicio.html": "index.html",
    "Mision.html": "Mision.html",
    "Comunidad.html": "Comunidad.html",
    "Oraciones.html": "Oraciones.html",
}

print("Preparando páginas...\n")

for origen_nombre, destino_nombre in mapa_html.items():

    origen = ARCHIVOS / origen_nombre
    destino = ROOT / destino_nombre

    preparar_html(origen, destino)

    print(
        f"{origen_nombre}  ->  {destino_nombre}"
    )

# ------------------------------------------------------------
# COPIAR CSS
# ------------------------------------------------------------

shutil.copy2(
    ARCHIVOS / "style.css",
    ROOT / "style.css"
)

print("style.css      ->  style.css")

# ------------------------------------------------------------
# CREAR .NOJEKYLL
# ------------------------------------------------------------

(ROOT / ".nojekyll").touch()

print(".nojekyll creado")

# ------------------------------------------------------------
# COMPROBAR IMAGES
# ------------------------------------------------------------

IMAGES = ROOT / "Images"

print("\nVerificando imágenes...\n")

if IMAGES.exists():

    cantidad = sum(
        1
        for archivo in IMAGES.rglob("*")
        if archivo.is_file()
    )

    print(f"Images encontrada correctamente.")
    print(f"Archivos de imagen encontrados: {cantidad}")

else:

    print("ADVERTENCIA:")
    print("No encontré la carpeta Images.")

# ------------------------------------------------------------
# RESULTADO
# ------------------------------------------------------------

print("\n============================================")
print(" LISTO")
print("============================================\n")

print("Ahora la raíz debería contener:\n")

print("Página Oficial Cmsfj/")
print("│")
print("├── index.html")
print("├── Mision.html")
print("├── Comunidad.html")
print("├── Oraciones.html")
print("├── style.css")
print("├── .nojekyll")
print("│")
print("├── Images/")
print("│   ├── Capillas/")
print("│   ├── Misiones/")
print("│   └── Nosotros/")
print("│")
print("└── Archivos/   <-- SE CONSERVA INTACTA")

print("\nIMPORTANTE:")
print("Todavía NO se hizo ningún commit ni push.")
print("Primero abrí index.html localmente y comprobá que se vea bien.")