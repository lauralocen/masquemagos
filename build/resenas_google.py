#!/usr/bin/env python3
"""Inserta las reseñas de Google (Places API, New) en index.html entre marcadores.

Uso:
  GOOGLE_PLACES_KEY=... GOOGLE_PLACE_ID=... python3 build/resenas_google.py

Sin variables de entorno no toca nada (el bloque queda vacío y no se muestra).
"""
import html, json, os, re, sys, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INDEX = os.path.join(ROOT, "index.html")
START, END = "<!-- RESENAS:START -->", "<!-- RESENAS:END -->"

key = os.environ.get("GOOGLE_PLACES_KEY", "").strip()
place = os.environ.get("GOOGLE_PLACE_ID", "").strip()
if not key or not place:
    print("Sin GOOGLE_PLACES_KEY o GOOGLE_PLACE_ID: no se cambia index.html")
    sys.exit(0)

req = urllib.request.Request(
    f"https://places.googleapis.com/v1/places/{place}",
    headers={
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": "displayName,rating,userRatingCount,googleMapsUri,reviews",
    },
)
with urllib.request.urlopen(req, timeout=20) as r:
    data = json.load(r)

reviews = sorted(data.get("reviews", []), key=lambda x: x.get("publishTime", ""), reverse=True)
e = html.escape
stars = lambda n: "★" * int(round(n or 0)) + "☆" * (5 - int(round(n or 0)))
cards = []
for rv in reviews:
    author = rv.get("authorAttribution", {})
    foto = author.get("photoUri", "")
    cards.append(f"""
      <article class="res-card">
        <header class="res-head">
          {'<img src="' + e(foto) + '" alt="" width="36" height="36" loading="lazy">' if foto else ''}
          <div><strong>{e(author.get('displayName', ''))}</strong>
          <span class="res-when">{e(rv.get('relativePublishTimeDescription', ''))}</span></div>
        </header>
        <div class="res-stars" aria-label="{rv.get('rating', '')} de 5">{stars(rv.get('rating'))}</div>
        <p>{e(rv.get('text', {}).get('text', ''))}</p>
        <a href="{e(rv.get('googleMapsUri', data.get('googleMapsUri', '#')))}" target="_blank" rel="noopener">Ver en Google</a>
      </article>""")

nota = data.get("rating")
total = data.get("userRatingCount", 0)
bloque = f"""{START}
<section class="resenas-google" aria-labelledby="res-title">
  <div class="res-wrap">
    <h2 id="res-title">Lo que dicen nuestros clientes</h2>
    <p class="res-resumen"><span class="res-stars">{stars(nota)}</span> {nota} de 5 · {total} reseñas en Google</p>
    <div class="res-grid">{''.join(cards)}
    </div>
    <p class="res-pie"><a href="{e(data.get('googleMapsUri', '#'))}" target="_blank" rel="noopener">Ver todas las reseñas en Google</a></p>
  </div>
</section>
<style>
.resenas-google{{padding:64px 16px;background:#fff}}
.res-wrap{{max-width:1120px;margin:0 auto}}
.resenas-google h2{{font-family:Fraunces,serif;font-size:clamp(26px,3.2vw,36px);margin:0 0 8px}}
.res-resumen{{margin:0 0 28px;color:#555}}
.res-stars{{color:#e0a100;letter-spacing:2px}}
.res-grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.res-card{{border:1px solid #e6e1d8;border-radius:12px;padding:18px;display:flex;flex-direction:column;gap:10px}}
.res-head{{display:flex;gap:10px;align-items:center}}
.res-head img{{border-radius:50%}}
.res-when{{display:block;font-size:13px;color:#777}}
.res-card p{{margin:0;font-size:15px;line-height:1.5}}
.res-card a,.res-pie a{{font-size:14px;color:#1a73e8}}
.res-pie{{margin-top:24px;text-align:center}}
</style>
{END}"""

with open(INDEX, encoding="utf-8") as f:
    src = f.read()
if START not in src:
    src = src.replace('<section class="cta" id="contacto">', START + END + '\n<section class="cta" id="contacto">', 1)
src = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: bloque, src, flags=re.S)
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Reseñas insertadas: {len(reviews)}")
