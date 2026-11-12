"""Rearma todo desde cero: los HTML para enviar y la página de revisión.
Uso (desde la carpeta «Correos Lexy Deudor»):  python3 herramientas/construir.py
"""
import base64, json, os, re, shutil, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALIDA = os.path.join(AQUI, "_salida")
REV = os.path.join(RAIZ, "revision")

if os.path.isdir(SALIDA):
    shutil.rmtree(SALIDA)
os.makedirs(SALIDA)
subprocess.run([sys.executable, "-I", os.path.join(AQUI, "build_emails.py"), SALIDA], check=True)

# 1. HTML para enviar: modelos en la raíz, ejemplos en ejemplos/
os.makedirs(os.path.join(RAIZ, "ejemplos"), exist_ok=True)
for f in os.listdir(SALIDA):
    if f.startswith("modelo-"):
        shutil.copy(os.path.join(SALIDA, f), os.path.join(RAIZ, f))
    elif f.startswith("ejemplo-"):
        shutil.copy(os.path.join(SALIDA, f), os.path.join(RAIZ, "ejemplos", f))

# 2. Página de revisión con los correos y las fuentes incrustadas
datos = json.load(open(os.path.join(SALIDA, "emails.json")))
js = json.dumps(datos, ensure_ascii=False).replace("<", "\\u003c")
pag = open(os.path.join(AQUI, "pagina.html")).read()
fuente = lambda n: base64.b64encode(open(os.path.join(AQUI, "fuentes", n), "rb").read()).decode()
pag = (pag.replace("__EMAILS__", js)
          .replace("__SWITZER__", fuente("switzer-variable.woff2"))
          .replace("__GEIST__", fuente("geist-sans-variable.woff2")))
open(os.path.join(REV, "index.html"), "w").write(pag)

# 3. Copias de los HTML para revisar sin internet (íconos locales)
BREVO = re.compile(r"https://creative-assets\.mailinblue\.com/editor/social-icons/rounded_colored/([a-z]+)_32px\.png")
for f in os.listdir(SALIDA):
    if f.endswith(".html"):
        html = BREVO.sub(r"img/brevo-\1.png", open(os.path.join(SALIDA, f)).read())
        open(os.path.join(REV, f), "w").write(html)

shutil.rmtree(SALIDA)

# 4. Generador de correos (guía + Crear correo), con las imágenes de la vista previa incrustadas
IMG = os.path.join(REV, "img")
b64 = lambda n: "data:image/png;base64," + base64.b64encode(open(os.path.join(IMG, n), "rb").read()).decode()
gen = open(os.path.join(AQUI, "generador.html")).read()
for clave, archivo in {"__IMG_NAVY__": "header-navy.png", "__IMG_CLARO__": "header-claro.png",
                       "__IMG_IG__": "brevo-instagram.png", "__IMG_FB__": "brevo-facebook.png",
                       "__IMG_WEB__": "brevo-website.png"}.items():
    gen = gen.replace(clave, b64(archivo))
# Versión para publicar en Claude (sin <html>/<head>: Claude los agrega)
open(os.path.join(AQUI, "generador-publicar.html"), "w").write(gen)
# Versión para abrir en el navegador o con el servidor local
open(os.path.join(REV, "generador.html"), "w").write(
    '<!doctype html>\n<html lang="es"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>\n'
    + gen + "\n</body></html>\n")
print("Listo: modelos, ejemplos y revision/ actualizados.")
