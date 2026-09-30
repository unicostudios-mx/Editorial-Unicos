# Estudio de producción — Audiolibro de «La escribana de los dioses» (agente mercado, 2026-09-30)

**Encargo de Nico:** ¿podemos hacer un audiolibro del Libro 1?
**Respuesta corta:** sí. 66,224 palabras ≈ **7–8 horas de audio** (a ~150 ppm de narración literaria). Tres rutas, de gratis a profesional. El texto fuente es el manuscrito español aprobado; la voz objetivo es la de Edna según la guía de estilo (contención, calidez seca, sin solemnidad).

## Ruta A — Producción local en el estudio (gratis; el texto no sale del repo)
Motor neuronal **Piper** (open source, ya instalado en el entorno) con voz es_MX. Calidad: buena para demo y uso personal; por debajo del estándar comercial de Audible.
- **Bloqueo actual:** la política de red del entorno deniega `huggingface.co` (donde viven los modelos de voz). **Para habilitarla:** en la barra de título de la sesión → menú del entorno cloud → *Edit* → *Network access* → añadir `huggingface.co` (y su CDN) a los dominios permitidos, o subir el nivel de acceso. Niveles descritos en code.claude.com/docs/en/claude-code-on-the-web.
- Con eso: el estudio produce **demo del cap. 1** el mismo día y, con visto bueno, el libro completo por capítulos (WAV/OGG; ~1 GB total, se entrega por archivos, no se versiona completo en git).

## Ruta B — TTS premium (calidad casi-narrador) ★ recomendada para lanzamiento
ElevenLabs / Azure Neural / Google — voces es-MX de nivel comercial, control de pausas y pronunciación.
- **Freno §3.4 doble:** gasta dinero **y** envía el manuscrito a un servicio externo → solo con tu autorización explícita y tu cuenta. Orden de magnitud (verificar precios vigentes): ~400–450k caracteres ≈ decenas–pocas centenas de USD según plan/proveedor.
- Flujo si autorizas: guardas la API key en los *secrets* del entorno → el estudio produce los 40 capítulos con la guía de narración de abajo, QA de escucha por muestreo, y masteriza a specs de ACX (192kbps MP3, -18 a -23 LUFS) hasta donde las herramientas del entorno lo permitan.

## Ruta C — Narrador humano o Virtual Voice
- **Narrador profesional** (ACX/Findaway/local): la mejor calidad y la más cara (tarifa por hora terminada). Todo el trato es tuyo (freno).
- **KDP Virtual Voice** (beta de Amazon, ligada a publicar el ebook en KDP): costo cero, pero disponibilidad para español **sin verificar** — comprobarlo en tu consola KDP antes de contar con ella.

## Veredicto
**A** para escucharlo esta semana (solo requiere permitir `huggingface.co` en el entorno); **B** para la versión de lanzamiento; **C-narrador** si el Cuaderno I encuentra público y lo amerita. La guía de abajo sirve idéntica para las tres.

---

# Guía de narración (para cualquier voz, humana o sintética)

## Dirección de voz — Edna
- **Registro:** mujer madura, grave-media, México neutro culto con calidez capitalina. Jamás solemne: es una profesional contando su trabajo. La emoción se da por contención, no por temblor.
- **Ritmo:** más lento que noticiario (~145–155 ppm); los dos puntos y rayas de Edna son respiraciones, no carreras.
- **Los separadores «—» entre secciones:** pausa larga (2.5–3 s), sin música.
- **Diálogo de dioses:** cambios mínimos de color, nunca "voces caricatura": Kulla terroso y risueño; Hestia abuela sin dulzor falso; el Lar seco y cariñoso; Tláloc lento y mineral; Śakra precisión de rey con ironía fina; Māra la voz más *descansada* del libro (jamás siniestra: amable, sin prisa); Santa Muerte muchacha de barrio, respetuosa; Isis elegancia de quien tiene las cuentas hechas.
- **Los tres renglones de actas en cursiva** (entradas del Registro): medio tono más bajo, más lento — se están *escribiendo*.
- **Cap. 39:** el final se corta a media palabra: se narra exactamente así, sin cerrar la frase, y la pausa que sigue es la más larga del libro (5 s) antes del cap. 40.
- **La página en blanco (post cap. 11):** en audio se honra con 4 s de silencio total tras el final del capítulo, sin anuncio.

## Léxico de pronunciación
| Término | Pronunciación |
|---|---|
| Enheduanna | en-je-du-Á-na (h aspirada suave; jamás "enedu-ana" plana) |
| Nin-me-šara | nin-me-SHÁ-ra |
| Śakra | SHÁ-kra |
| Erāvaṇa | e-RÁ-va-na |
| Māra | MÁ-ra (a larga suave) |
| Huehuetéotl | ue-ue-TÉ-otl |
| Tláloc / Tonantzin / Tepeyac | tradicional mexicana |
| Kulla | KÚ-la |
| Uruk / Eanna | Ú-ruk / e-Á-na |
| Vejayanta | ve-cha-YÁN-ta |
| Íslendingabók | ÍS-len-din-ga-bok |
| Thorgeir | TOR-gueir |
| granicero, cempasúchil, chiquihuite, atole, champurrado | naturales MX, sin subrayar |
| furoshiki / kamidana | fu-ROSH-ki / ka-mi-DA-na |
| Zao Jun | dsao-CHÚN (suave) |

## Estructura de entrega (cuando se produzca)
`audiolibro/00-creditos.wav` (título, cintillo, "escrito por Albertoni") · `01.wav … 40.wav` por capítulo · specs objetivo: 44.1kHz/16-bit master, MP3 192kbps mono para distribución, RMS -18 a -23 dB, cola de 1–5 s por archivo (estándar ACX).
