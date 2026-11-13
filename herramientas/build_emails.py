"""Genera el HTML para enviar (tablas + estilos en línea) de cada correo con cada header.
Uso: python3 -I build_emails.py <carpeta_salida>
Escribe emails.json (para el botón Copiar HTML de la página) y un .html por combinación.
"""
import sys, os, json

out = sys.argv[1]
FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif"

S3 = "https://imagenes-perfi-abg-eje.s3.us-east-1.amazonaws.com/"

# clave interna -> (nombre, archivo de salida, URL pública del header)
HEADERS = {
    "navy": ("Correos generales", "generales", S3 + "Header_Correos_Generales_LEXY.png"),
    "claro": ("Correos de tramitación", "tramitacion", S3 + "Header_blanco_marcado_tramitacion.png"),
}

# Íconos del pie: se suben al mismo bucket con estos nombres exactos.
ICON_FILE = {"instagram": "Icono_correos_instagram.png",
             "facebook": "Icono_correos_facebook.png",
             "web": "Icono_correos_web.png"}

# Redes y sitio de Lexy Deudor.
BREVO = "https://creative-assets.mailinblue.com/editor/social-icons/rounded_colored/"
SOCIAL = [
    ("instagram", "Instagram", "https://instagram.com/lexydeudor"),
    ("facebook", "Facebook", "https://web.facebook.com/profile.php?id=100089769037935"),
    ("website", "Sitio Web", "https://lexy.cl/"),
]

def hi(name="Javiera"):
    return ('<p class="txt hi" style="margin:0 0 10px;font-size:20px;line-height:1.4;color:#4f5157;">Hola, '
            f'<span class="name" style="font-weight:700;color:#0b013c;border-bottom:3px solid #f0a23b;padding-bottom:1px;">{name}</span>:</p>')

def h1(t):
    return f'<h1 class="h1" style="margin:0 0 14px;font-size:28px;line-height:1.15;font-weight:700;letter-spacing:-0.5px;color:#0b013c;">{t}</h1>'

def em(t):
    return f'<span class="em" style="color:#4429cc;">{t}</span>'

def p(t):
    return f'<p class="txt" style="margin:0 0 16px;color:#4f5157;">{t}</p>'

def note(t):
    return f'<p class="txt" style="margin:0 0 16px;font-size:13px;color:#7a7d87;">{t}</p>'

def box(k, v, m, small=False):
    size = "20px" if small else "32px"
    return f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:22px 0;">
        <tr><td class="box" style="background:#f0f0fb;border-radius:12px;padding:18px 20px;">
          <div class="k" style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#4429cc;">{k}</div>
          <div class="v" style="font-size:{size};font-weight:700;line-height:1.25;color:#0b013c;margin:2px 0;">{v}</div>
          <div class="m" style="font-size:14px;color:#4f5157;">{m}</div>
        </td></tr>
      </table>'''

def button(label, href="https://lexy.cl/"):
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 20px;">
        <tr><td class="btn" style="background:#4429cc;border-radius:10px;">
          <a href="{href}" style="display:inline-block;padding:13px 24px;font-family:{FONT};font-size:16px;font-weight:700;color:#ffffff;text-decoration:none;">{label}</a>
        </td></tr>
      </table>'''

def steps(items):
    rows = []
    for i, (t, s) in enumerate(items, 1):
        border = "" if i == len(items) else "border-bottom:1px solid #e3e3e8;"
        rows.append(f'''<tr>
          <td class="row" width="48" style="padding:12px 0;{border}vertical-align:middle;">
            <div class="num" style="width:36px;height:36px;line-height:36px;border-radius:10px;background:#f0f0fb;color:#4429cc;font-weight:700;font-size:14px;text-align:center;">{i}</div>
          </td>
          <td class="row" style="padding:12px 0;{border}vertical-align:middle;">
            <div class="lt" style="font-weight:700;color:#202124;">{t}</div>
            <div class="ls" style="font-size:14px;color:#7a7d87;">{s}</div>
          </td>
        </tr>''')
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:18px 0 22px;">'
            + "".join(rows) + "</table>")

def sign():
    return ('<p class="txt" style="margin:8px 0 28px;font-size:15px;color:#4f5157;">'
            '<strong class="lt" style="display:block;color:#202124;">Tu equipo Lexy</strong>'
            'Si tienes dudas, escríbenos por WhatsApp.</p>')

MAILS = {
    "cuota": ("Tu cuota 4 vence el 10 de diciembre",
              "Te lo recordamos con tiempo para que pagues sin apuro.",
              hi() + h1("Tu cuota vence el " + em("10 de diciembre"))
              + p("Te lo recordamos con tiempo para que pagues sin apuro. Puedes hacerlo en línea o por transferencia.")
              + box("Próxima cuota", "$89.900", "Cuota 4 de 12 · Vence el 10 de diciembre")
              + button("Pagar mi cuota")
              + note("¿Ya pagaste? Tu pago puede tardar hasta 48 horas en verse en el portal.")),
    "etapa": ("Tu caso avanzó de etapa",
              "Tu equipo terminó de revisar tus antecedentes.",
              hi() + h1("Tu caso avanzó de etapa")
              + p("Tu equipo terminó de revisar tus antecedentes. Ahora estamos ordenando tu documentación para el siguiente paso.")
              + box("Renegociación · Etapa actual", "Gestionando tu documentación", "Qué viene: preparar tu propuesta de renegociación.", small=True)
              + button("Ver mi caso") + sign()),
    "pago": ("Recibimos tu pago",
             "Tu cuota 3 quedó pagada. Gracias por estar al día.",
             hi() + h1("Recibimos tu pago")
             + p("Tu cuota 3 quedó pagada. Gracias por estar al día: eso nos ayuda a avanzar con tu caso.")
             + box("Pago recibido", "$89.900", "Cuota 3 de 12 · Pagada el 2 de noviembre de 2026")
             + p("Tu próxima cuota vence el 10 de diciembre. Te avisaremos unos días antes.")
             + button("Ver mis pagos")),
    "bienvenida": ("Bienvenida a tu Portal del Cliente",
                   "Desde hoy puedes ver en qué va tu caso, en un solo lugar.",
                   hi() + h1("Ya tienes tu " + em("Portal del Cliente"))
                   + p("Desde hoy puedes ver en qué va tu caso, cuándo pagar y cómo hablar con tu equipo, todo en un solo lugar.")
                   + steps([("Consultar mi servicio", "Qué hacemos por ti y a qué resultado apuntamos"),
                            ("Pagar mis honorarios", "Tu próxima cuota y cómo pagarla"),
                            ("Hablar con mi equipo", "Tu ejecutiva y tu abogado, por WhatsApp")])
                   + button("Entrar a mi portal")),
}

MODELO = ("[Asunto del correo]", "[Texto de vista previa que se ve en la bandeja]",
    "\n      <!-- EDITA: nombre del cliente -->\n      " + hi("{{nombre cliente}}")
    + "\n      <!-- EDITA: título, una sola idea. Lo que va en <span class=\"em\"> sale en índigo -->\n      "
    + h1("[Título del correo con una " + em("palabra destacada") + "]")
    + "\n      <!-- EDITA: párrafo. Qué pasó y qué significa para el cliente, en dos o tres líneas -->\n      "
    + p("[Párrafo principal del correo.]")
    + "\n      <!-- OPCIONAL: recuadro con el dato clave (monto, fecha, etapa). Borra la tabla completa si no lo usas -->\n      "
    + box("[Rótulo]", "[Dato clave]", "[Detalle del dato]")
    + "\n      <!-- EDITA: botón. Cambia el texto y el href -->\n      "
    + button("[Acción]")
    + "\n      <!-- OPCIONAL: nota final -->\n      "
    + note("[Nota opcional en gris.]"))

def footer():
    icons = "".join(
        f'<a href="{href}" target="_blank" style="display:inline-block;text-decoration:none;margin:0 6px;">'
        f'<img src="{BREVO}{k}_32px.png" width="24" height="24" alt="{name}" style="width:24px;height:24px;border:0;"></a>'
        for k, name, href in SOCIAL)
    return f'''<tr><td class="foot" align="center" style="background:#fafafa;border-top:1px solid #eeeeee;padding:28px 20px;font-family:{FONT};font-size:12px;color:#888888;text-align:center;">
      <div style="text-align:center;margin-bottom:16px;">{icons}</div>
      <p style="margin:0;color:#999999;font-size:11px;">Lexy - Todos los derechos reservados</p>
    </td></tr>'''

TPL = '''<!DOCTYPE html>
<html lang="es" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="x-apple-disable-message-reformatting">
<meta name="format-detection" content="telephone=no,address=no,email=no,date=no">
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
<title>__TITLE__</title>
<!--[if mso]><style>body,table,td,p,a,h1{font-family:Arial,sans-serif !important;}</style><![endif]-->
<style>
  body{margin:0;padding:0;width:100% !important;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}
  table{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}
  img{border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;}
  a[x-apple-data-detectors]{color:inherit !important;text-decoration:none !important;}
  /* Celular */
  @media only screen and (max-width:620px){
    .outer{padding:14px 10px !important;}
    .pad{padding:28px 22px 8px !important;}
    .padf{padding:26px 22px !important;}
    .h1{font-size:24px !important;}
    .hi{font-size:18px !important;}
    .v{font-size:28px !important;}
  }
  /* Modo oscuro (Mail de iPhone y Mac, Outlook de Mac) */
  @media (prefers-color-scheme: dark){
    .bg{background:#000000 !important;}
    .card{background:#141317 !important;}
    .h1,.name,.lt{color:#ffffff !important;}
    .em,.lk{color:#9d90fc !important;}
    .txt,.ls{color:#c3c2cc !important;}
    .box,.num{background:#221b4a !important;}
    .k,.num{color:#9d90fc !important;}
    .v{color:#ffffff !important;}
    .m{color:#cdc8f0 !important;}
    .row{border-color:#2b2a32 !important;}
    .btn{background:#9d90fc !important;}
    .btn a{color:#0b013c !important;}
    .foot{background:#0c0b0f !important;color:#8e8d98 !important;}
  }
</style>
</head>
<body style="margin:0;padding:0;background:#f1f1f3;">
<!-- Texto de vista previa en la bandeja -->
<div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all;">__PRE__</div>
<table role="presentation" class="bg" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f1f1f3;">
<tr><td class="outer" align="center" style="padding:24px 12px;">
  <!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td><![endif]-->
  <table role="presentation" class="card" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;margin:0 auto;background:#ffffff;">
    <!-- HEADER: __HNAME__ -->
    <tr><td style="padding:0;font-size:0;line-height:0;">
      <img src="__SRC__" width="600" alt="Lexy Deudor" style="display:block;width:100%;max-width:600px;height:auto;">
    </td></tr>
    <!-- CUERPO -->
    <tr><td class="pad" style="padding:40px 48px 12px;font-family:__FONT__;font-size:16px;line-height:1.6;color:#4f5157;">
      __BODY__
    </td></tr>
    <!-- PIE -->
    __FOOT__
  </table>
  <!--[if mso]></td></tr></table><![endif]-->
</td></tr>
</table>
</body>
</html>
'''

data = {}
for hk, (hname, fname, src) in HEADERS.items():
    data[hk] = {}
    items = dict(MAILS); items["modelo"] = MODELO
    for mk, (title, pre, body) in items.items():
        html = (TPL.replace("__TITLE__", title).replace("__PRE__", pre).replace("__HNAME__", hname)
                .replace("__SRC__", src).replace("__FONT__", FONT).replace("__BODY__", body)
                .replace("__FOOT__", footer()))
        data[hk][mk] = html
        name = f"modelo-{fname}.html" if mk == "modelo" else f"ejemplo-{fname}-{mk}.html"
        open(os.path.join(out, name), "w").write(html)

json.dump(data, open(os.path.join(out, "emails.json"), "w"), ensure_ascii=False)
print("ok", sum(len(v) for v in data.values()))
