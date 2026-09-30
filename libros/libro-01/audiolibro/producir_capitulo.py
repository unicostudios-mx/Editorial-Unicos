#!/usr/bin/env python3
"""Demo audiolibro — cap. 10 «La confesión», voz Piper es_MX-claude-high.
Sigue la guía de narración de mercado-audiolibro.md:
- separador «—» entre secciones = pausa larga (2.8 s)
- ritmo más lento que el default (length_scale)
- cursivas sin marcas; rayas de diálogo limpiadas para la fonemización
"""
import re, wave, subprocess, sys
from pathlib import Path

SCRATCH = Path("/tmp/claude-0/-home-user-Editorial-Unicos/700fea4c-d8f4-5bba-b717-6f40135ea580/scratchpad")
SRC = Path("/home/user/Editorial-Unicos/libros/libro-01/03-manuscrito/cap-10.md")
MODEL = SCRATCH / "piper-voices" / "es_MX-claude-high.onnx"
OUT_WAV = SCRATCH / "cap-10-demo.wav"

raw = SRC.read_text(encoding="utf-8")
lines = raw.splitlines()

# Título -> anuncio narrado
body_lines = []
for ln in lines:
    if ln.startswith("# "):
        continue
    body_lines.append(ln)

body = "\n".join(body_lines).strip()

# Secciones separadas por una raya sola en su propia línea
sections = re.split(r"\n\s*—\s*\n", body)

def clean(text: str) -> str:
    t = text
    t = t.replace("*", "")                      # cursivas: sin marca
    t = re.sub(r"^—", "", t, flags=re.M)        # raya de apertura de diálogo
    t = t.replace(" —", ", ").replace("— ", ", ")  # incisos: coma = respiración
    t = t.replace("—", ", ")
    t = t.replace("«", "").replace("»", "")
    t = re.sub(r"\"(.+?)\"", r"\1", t)
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()

INTRO = ("La escribana de los dioses. Los cuadernos de la escribana, cuaderno uno. "
         "Escrito por Albertoni. Capítulo diez. La confesión.")

segments = [INTRO] + [clean(s) for s in sections if s.strip()]

from piper import PiperVoice
try:
    from piper import SynthesisConfig
    SYN = SynthesisConfig(length_scale=1.08)   # ~más lento que default: ritmo literario
except ImportError:
    SYN = None
voice = PiperVoice.load(str(MODEL))

# Sintetiza cada segmento y concatena con silencios
SR = None
frames = []

def synth(text):
    global SR
    chunks = []
    it = voice.synthesize(text, SYN) if SYN else voice.synthesize(text)
    for ch in it:
        if SR is None:
            SR = ch.sample_rate
        chunks.append(ch.audio_int16_bytes)
    return b"".join(chunks)

def silence(seconds):
    return b"\x00\x00" * int(SR * seconds)

audio = synth(segments[0])
frames.append(audio)
frames.append(silence(2.0))          # tras créditos
for i, seg in enumerate(segments[1:]):
    # párrafo a párrafo para pausas de respiración
    paras = [p.strip() for p in seg.split("\n") if p.strip()]
    for j, p in enumerate(paras):
        frames.append(synth(p))
        frames.append(silence(0.65)) # respiración entre párrafos
    if i < len(segments[1:]) - 1:
        frames.append(silence(2.8))  # separador «—»: pausa larga
frames.append(silence(3.0))          # cola final (ACX 1–5 s)

data = b"".join(frames)
with wave.open(str(OUT_WAV), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data)

dur = len(data) / 2 / SR
print(f"OK: {OUT_WAV}  {dur/60:.1f} min  {SR} Hz")
