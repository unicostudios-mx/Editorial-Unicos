# Audiolibro — «La escribana de los dioses» (Ruta A, producción local)

**Rama de trabajo:** `claude/audiolibro-demo` — separada de `claude/hola-ngngrf` (edición) a pedido de Nico (2026-09-30).

## Estado

- **2026-09-30 — Demo producido: capítulo 10, «La confesión»** (`cap-10-la-confesion-demo.mp3`, 9.4 min). Elegido por Nico en lugar del cap. 1 propuesto.
- Motor: Piper (`es_MX-claude-high`, descargado de huggingface.co tras habilitar la red). Guía de narración aplicada desde `../mercado-audiolibro.md`.

## Cómo se produjo (reproducible)

`producir_capitulo.py` — síntesis con Piper + masterizado en Python (sin ffmpeg en este entorno; `soundfile`/libsndfile 1.2.2 escribe el MP3):

1. Créditos de apertura (título, cintillo, «escrito por Albertoni», número y nombre del capítulo).
2. Texto limpio: cursivas sin marca; rayas de diálogo e incisos convertidos a respiraciones (comas); separador «—» entre secciones = **2.8 s de silencio**; 0.65 s entre párrafos; cola final de 3 s.
3. Ritmo: `length_scale 1.08` (≈150 ppm, registro literario).
4. Master: 22050→44100 Hz, mono, normalización RMS de voz a **-20 dBFS** (rango ACX -18/-23), techo de picos -3 dB, MP3 192 kbps.

Requisitos: `pip install piper-tts soundfile` + modelo de voz (`python3 -m piper.download_voices es_MX-claude-high`).

## Decisión operativa (pasar a `decisiones.md` como D-027 al fusionar)

**TOMADA — Demo con voz `es_MX-claude-high` y pipeline local descrito arriba.** Porqué: única voz es_MX de calidad *high* disponible en Piper; el masterizado en Python evita depender de ffmpeg ausente en el entorno. Se registra aquí y no en `decisiones.md` para no divergir la rama de edición.

## Siguiente paso

Con visto bueno de Nico al demo: producir los 40 capítulos + `00-creditos` en esta rama (los WAV/MP3 completos ~500 MB **no** se versionan en git; se entregan por archivos), aplicando además: pausa de 5 s tras el corte a media palabra del cap. 39 y 4 s de silencio por la página en blanco tras el cap. 11.
