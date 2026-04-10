#!/usr/bin/env python3
"""
GenioAI - Daily Article Generator
Genera un articulo HTML nuevo cada dia usando Claude API
"""

import os
import json
import anthropic
from datetime import datetime
from pathlib import Path

# ─── CONFIGURACION ───────────────────────────────────────────
BLOG_DIR = Path(__file__).parent.parent / "blog"
TOPICS_FILE = Path(__file__).parent / "topics.json"
BLOG_INDEX = Path(__file__).parent.parent / "blog.html"
INDEX_HTML = Path(__file__).parent.parent / "index.html"

MONTHS_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def get_next_topic():
    """Selecciona el proximo tema que aun no tiene articulo publicado."""
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics = json.load(f)

    published = {p.stem for p in BLOG_DIR.glob("*.html")}

    for topic in topics:
        if topic["slug"] not in published:
            return topic

    # Si todos estan publicados, reiniciar con el primero
    print("Todos los temas publicados. Reiniciando lista...")
    return topics[0]


def generate_article_content(topic: dict, client: anthropic.Anthropic) -> str:
    """Usa Claude para generar el contenido del articulo en HTML."""

    today = datetime.now()
    date_str = f"{today.day} de {MONTHS_ES[today.month]} {today.year}"

    prompt = f"""Eres un experto en inteligencia artificial y redactor de blog en español.
Escribe un artículo de blog completo y detallado sobre el siguiente tema:

**Título:** {topic['title']}
**Palabras clave:** {topic['keywords']}
**Descripción breve:** {topic['description']}

REGLAS IMPORTANTES:
1. El artículo debe tener mínimo 1200 palabras en español
2. Usa un tono conversacional pero profesional, como si explicaras a un amigo inteligente
3. Incluye secciones claras con encabezados H2 y H3
4. Incluye ejemplos prácticos y concretos
5. Menciona precios reales y actualizados de 2025
6. Incluye al menos 3 consejos o tips prácticos
7. Al final incluye una conclusión clara
8. NO uses markdown, devuelve SOLO el contenido HTML del artículo

Devuelve ÚNICAMENTE el contenido HTML interior del artículo (sin <html>, <head>, <body>).
Usa estas etiquetas:
- <h2 id="seccion"> para secciones principales
- <h3> para subsecciones
- <p> para párrafos
- <ul><li> para listas
- <ol><li> para listas numeradas
- <strong> para énfasis
- Usa esta clase para cajas de tips: <div class="tip-box"><strong>💡 Tip:</strong><p>contenido</p></div>
- Usa esta clase para herramientas: <div class="tool-card"><div class="tool-card-icon">EMOJI</div><div class="tool-card-info"><h3>Nombre</h3><p>descripción</p><span class="badge">GRATIS / $precio</span></div></div>

El artículo debe ser útil, honesto y basado en información real de 2025."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def build_article_html(topic: dict, content: str) -> str:
    """Construye el HTML completo del articulo."""

    today = datetime.now()
    date_str = f"{today.day} de {MONTHS_ES[today.month]} {today.year}"
    read_time = str(max(5, len(content.split()) // 200))

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{topic['title']} | GenioAI</title>
  <meta name="description" content="{topic['description']}" />
  <meta name="keywords" content="{topic['keywords']}" />
  <meta property="og:title" content="{topic['title']}" />
  <meta property="og:description" content="{topic['description']}" />
  <meta property="og:type" content="article" />
  <link rel="stylesheet" href="../css/style.css" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧠</text></svg>" />
  <style>
    #readingProgress {{
      position: fixed; top: 0; left: 0;
      height: 3px; background: linear-gradient(90deg,#7c3aed,#06b6d4);
      z-index: 9999; width: 0; transition: width 0.1s;
    }}
    .article-sidebar {{
      position: sticky; top: 90px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 24px;
      font-size: 0.88rem;
    }}
    .article-sidebar h4 {{ font-weight: 700; margin-bottom: 16px; color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; }}
    .article-sidebar ul {{ display: flex; flex-direction: column; gap: 10px; }}
    .article-sidebar ul li a {{ color: var(--text-muted); transition: color 0.2s; }}
    .article-sidebar ul li a:hover {{ color: var(--primary-light); }}
    .article-layout {{ display: grid; grid-template-columns: 1fr 260px; gap: 40px; max-width: 1100px; margin: 0 auto; padding: 60px 24px; }}
    @media (max-width: 900px) {{ .article-layout {{ grid-template-columns: 1fr; }} .article-sidebar {{ display: none; }} }}
  </style>
</head>
<body>
<div id="readingProgress"></div>

<nav class="navbar" id="navbar">
  <a href="../index.html" class="nav-logo">
    <div class="logo-icon">🧠</div>
    <span>GenioAI</span>
  </a>
  <ul class="nav-links" id="navLinks">
    <li><a href="../index.html">Inicio</a></li>
    <li><a href="../blog.html">Blog</a></li>
    <li><a href="../herramientas.html">Herramientas</a></li>
    <li><a href="../about.html">Nosotros</a></li>
    <li><a href="../blog.html" class="nav-cta">Empezar →</a></li>
  </ul>
  <div class="nav-toggle" id="navToggle"><span></span><span></span><span></span></div>
</nav>

<div class="article-hero">
  <span class="article-tag">{topic['cat_label']}</span>
  <h1>{topic['title']}</h1>
  <div class="article-meta">
    <span>📅 {date_str}</span>
    <span>⏱️ {read_time} min lectura</span>
    <span>✍️ Equipo GenioAI</span>
  </div>
</div>

<div style="max-width:800px;margin:0 auto;padding:0 24px;">
  <div class="ad-zone"><span>Publicidad</span></div>
</div>

<div class="article-layout">
  <article class="article-body">
    {content}

    <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:28px;margin-top:48px;text-align:center;">
      <div style="font-size:2rem;margin-bottom:12px;">📺</div>
      <h3 style="margin-bottom:8px;">¿Prefieres verlo en video?</h3>
      <p style="color:var(--text-muted);margin-bottom:20px;font-size:0.9rem;">Encuentra tutoriales visuales en nuestro canal de YouTube.</p>
      <a href="https://youtube.com/@canalblx" target="_blank" rel="noopener" class="btn-primary">Ver en YouTube →</a>
    </div>
  </article>

  <aside>
    <div class="article-sidebar">
      <h4>📰 Artículos Recientes</h4>
      <ul>
        <li><a href="mejores-herramientas-ia-imagenes-2025.html">10 Mejores herramientas IA para imágenes</a></li>
        <li><a href="midjourney-guia-completa-espanol.html">Midjourney: Guía completa</a></li>
        <li><a href="como-usar-chatgpt-gratis-2025.html">ChatGPT gratis: Guía 2025</a></li>
      </ul>
    </div>
    <div style="margin-top:20px;">
      <div class="ad-zone" style="margin:0;"><span>Publicidad</span></div>
    </div>
  </aside>
</div>

<section class="newsletter">
  <div class="container">
    <div class="newsletter-box">
      <div style="font-size:2.5rem;margin-bottom:16px;">🧠</div>
      <h2>Recibe Tutoriales Nuevos Cada Semana</h2>
      <p>Sin spam. Solo los mejores artículos de IA directamente en tu email.</p>
      <form class="newsletter-form" id="newsletterForm">
        <input type="email" placeholder="tu@email.com" required />
        <button type="submit">Suscribirse</button>
      </form>
    </div>
  </div>
</section>

<footer>
  <div class="footer-grid">
    <div class="footer-brand">
      <a href="../index.html" class="nav-logo"><div class="logo-icon">🧠</div><span>GenioAI</span></a>
      <p>El blog de inteligencia artificial en español.</p>
    </div>
    <div class="footer-col"><h4>Contenido</h4><ul><li><a href="../blog.html">Blog</a></li><li><a href="../herramientas.html">Herramientas</a></li></ul></div>
    <div class="footer-col"><h4>Legal</h4><ul><li><a href="../privacy.html">Privacidad</a></li><li><a href="../terms.html">Términos</a></li><li><a href="../contact.html">Contacto</a></li></ul></div>
    <div class="footer-col"><h4>Nosotros</h4><ul><li><a href="../about.html">Quiénes somos</a></li><li><a href="../disclaimer.html">Aviso Legal</a></li></ul></div>
  </div>
  <div class="footer-bottom">
    <span>© 2025 GenioAI. Todos los derechos reservados.</span>
    <span>Hecho con ❤️ para la comunidad hispanohablante</span>
  </div>
</footer>
<script src="../js/main.js"></script>
</body>
</html>"""


def add_card_to_blog_index(topic: dict, date_str: str):
    """Inserta la nueva tarjeta de articulo al inicio del grid en blog.html"""

    card_html = f"""
      <a href="blog/{topic['slug']}.html" class="article-card" data-cat="{topic['category']}">
        <div class="article-card-image {topic['bg']}">{topic['icon']}</div>
        <div class="article-card-body">
          <span class="article-tag">{topic['cat_label']}</span>
          <h3>{topic['title']}</h3>
          <p>{topic['description']}</p>
          <div class="card-footer">
            <span>📅 {date_str}</span>
            <span class="read-more">Leer →</span>
          </div>
        </div>
      </a>
"""

    content = BLOG_INDEX.read_text(encoding="utf-8")
    # Inserta despues de la etiqueta de apertura del grid
    marker = '<div class="articles-grid" id="articlesGrid">'
    content = content.replace(marker, marker + card_html, 1)
    BLOG_INDEX.write_text(content, encoding="utf-8")
    print(f"  ✓ Tarjeta añadida a blog.html")


def update_homepage_featured(topic: dict, date_str: str):
    """Actualiza el articulo destacado en index.html con el mas reciente."""

    content = INDEX_HTML.read_text(encoding="utf-8")

    new_featured = f"""    <a href="blog/{topic['slug']}.html" class="featured-card">
      <div class="featured-image">
        <div class="featured-image-icon">{topic['icon']}</div>
      </div>
      <div class="featured-content">
        <span class="article-tag">{topic['cat_label']}</span>
        <h2>{topic['title']}</h2>
        <p>{topic['description']}</p>
        <div class="article-meta">
          <span>📅 {date_str}</span>
          <span>⏱️ 8 min lectura</span>
        </div>
        <span class="read-more">Leer artículo completo →</span>
      </div>
    </a>"""

    import re
    pattern = r'<a href="blog/[^"]+\.html" class="featured-card">.*?</a>'
    content = re.sub(pattern, new_featured, content, flags=re.DOTALL)
    INDEX_HTML.write_text(content, encoding="utf-8")
    print(f"  ✓ Artículo destacado actualizado en index.html")


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY no encontrada en variables de entorno")

    client = anthropic.Anthropic(api_key=api_key)

    today = datetime.now()
    date_str = f"{today.day} de {MONTHS_ES[today.month]} {today.year}"

    print("🧠 GenioAI — Generador de Artículos Diarios")
    print("=" * 50)

    # Seleccionar tema
    topic = get_next_topic()
    print(f"📝 Tema seleccionado: {topic['title']}")

    # Generar contenido con Claude
    print("⚡ Generando contenido con Claude API...")
    content = generate_article_content(topic, client)
    print(f"  ✓ Contenido generado ({len(content.split())} palabras aprox.)")

    # Construir HTML completo
    article_html = build_article_html(topic, content)

    # Guardar archivo
    output_path = BLOG_DIR / f"{topic['slug']}.html"
    output_path.write_text(article_html, encoding="utf-8")
    print(f"  ✓ Artículo guardado: blog/{topic['slug']}.html")

    # Actualizar blog.html con nueva tarjeta
    add_card_to_blog_index(topic, date_str)

    # Actualizar articulo destacado en index.html
    update_homepage_featured(topic, date_str)

    print(f"\n✅ COMPLETADO: '{topic['title']}'")
    print(f"   URL: blog/{topic['slug']}.html")
    print(f"   Fecha: {date_str}")


if __name__ == "__main__":
    main()
