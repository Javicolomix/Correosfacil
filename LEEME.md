# Correos Lexy Deudor

Plantillas HTML de los correos al cliente de Lexy Deudor. Proyecto separado del
Portal del Cliente.

## Qué hay en esta carpeta

| Carpeta o archivo | Para qué sirve |
|---|---|
| `modelo-generales.html` | Plantilla en blanco con el header **oscuro** (correos generales). |
| `modelo-tramitacion.html` | Plantilla en blanco con el header **claro** (correos de tramitación). |
| `ejemplos/` | Los 4 correos de ejemplo (cuota, etapa, pago, bienvenida) con cada header. |
| `revision/` | La página para revisar los correos en el celular o el computador, y el generador (`revision/generador.html`). |
| `herramientas/` | Lo necesario para rearmar todo. No hace falta abrirla. |
| `Opciones descartadas/` | Headers y versiones anteriores, por si se quieren volver a ver. |

Los modelos y ejemplos son los que se pegan en la herramienta de envío.

## Decisiones

- **Headers** (en el bucket S3 `imagenes-perfi-abg-eje`):
  - Oscuro, correos generales: `Header_Correos_Generales_LEXY.png`
  - Claro, correos de tramitación: `Header_blanco_marcado_tramitacion.png`
- **Cuerpo:** igual con los dos headers. Saludo «Hola, {{nombre cliente}}:» a 20 px,
  con el nombre en negrita y subrayado naranja. Recuadro lavanda para el dato
  clave y botón índigo.
- **Pie:** el que pasó la diseñadora. Fondo `#fafafa`, íconos de Brevo de 24 px
  (Instagram, Facebook y sitio web) y «Lexy - Todos los derechos reservados».
  - Instagram: https://instagram.com/lexydeudor
  - Facebook: https://web.facebook.com/profile.php?id=100089769037935
  - Web: https://lexy.cl/
- **Responsivo:** 600 px en computador, ancho completo en celular. Incluye un
  ajuste para Outlook de escritorio y estilos de modo oscuro para Mail de Apple.

## Generador de correos

Página con tres secciones: **Crear correo** (escribes el contexto, eliges el tipo y el
header, y entrega el HTML listo para montar), **Objetivos básicos** (la guía) y
**Probar mi correo** (el tester, código `lexy123`).

- Publicada en Claude, con redacción automática: https://claude.ai/artifact/TLc8JdSmemZbtYMgwwzn3C
- En Vercel, para el equipo (sin redacción automática; se actualiza solo con cada `git push`):
  https://correos-facil.vercel.app
- Local, sin redacción automática (se escribe el borrador a mano):
  `http://localhost:5181/generador.html` con el servidor de abajo.

Se edita en `herramientas/generador.html`. Después de `construir.py`, para actualizar la
versión publicada hay que volver a publicar `herramientas/generador-publicar.html`.

## Cómo revisar en el celular

En la Terminal, desde esta carpeta:

```
python3 herramientas/serve_nocache.py revision
```

Después abre en el celular `http://<IP del computador>:5181`. El celular tiene que
estar en el mismo wifi. La IP se ve con `ipconfig getifaddr en0`.

## Cómo cambiar algo

Los textos y estilos salen de `herramientas/build_emails.py` (los correos) y de
`herramientas/pagina.html` (la página de revisión). Después de editarlos:

```
python3 herramientas/construir.py
```

Eso rearma los modelos, los ejemplos y la página de revisión.
