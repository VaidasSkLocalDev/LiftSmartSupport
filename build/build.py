#!/usr/bin/env python3
"""Generate the LiftSmart site: root = English, one folder per other language.
Usage: python3 build/build.py   (run from the repo root)"""
import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "liftsmartsupport@gmail.com"
STORE = "https://apps.apple.com/app/id6741731118"
LANGS = {  # code: (folder, html lang, hreflang, native label, English label)
  "en": ("", "en", "en", "English", "English"),
  "de": ("de/", "de", "de", "Deutsch", "German"),
  "es": ("es/", "es", "es", "Español", "Spanish"),
  "fr": ("fr/", "fr", "fr", "Français", "French"),
  "ja": ("ja/", "ja", "ja", "日本語", "Japanese"),
  "pt-BR": ("pt-BR/", "pt-BR", "pt-BR", "Português (Brasil)", "Portuguese"),
}
PAGES = ["index.html", "TermsAndConditions.html", "PrivacyPolicy.html", "DeleteInstructions.html"]
APPLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.05 20.28c-.96.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8.79-.16 2.09-.86 3.51-.73 1.35.11 2.5.61 3.29 1.62-3.03 1.86-2.55 5.79.54 6.98-.61 1.57-1.4 3.11-2.42 4.3zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>'

def e(s): return html.escape(s, quote=True)

def head(S, lang, rel, page, title, desc):
    alts = "".join(f'\n  <link rel="alternate" hreflang="{LANGS[l][2]}" href="https://vaidassklocaldev.github.io/LiftSmartSupport/{LANGS[l][0]}{page}">' for l in LANGS)
    alts += f'\n  <link rel="alternate" hreflang="x-default" href="https://vaidassklocaldev.github.io/LiftSmartSupport/{page}">'
    return f"""<!DOCTYPE html>
<html lang="{LANGS[lang][1]}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">{alts}
  <link rel="icon" type="image/png" href="{rel}assets/img/favicon.png" media="(prefers-color-scheme: light)">
  <link rel="icon" type="image/png" href="{rel}assets/img/favicon-dark.png" media="(prefers-color-scheme: dark)">
  <link rel="icon" type="image/png" href="{rel}assets/img/favicon.png">
  <link rel="apple-touch-icon" href="{rel}assets/img/appicon.png">
  <link rel="stylesheet" href="{rel}assets/css/site.css?v=23">
  <script src="{rel}assets/js/site.js?v=20"></script>
</head>
<body>
"""

def store_btn(S, cls=""):
    return f'<a class="store {cls}" href="{STORE}" target="_blank" rel="noopener">{APPLE}<span><small>{e(S["nav"]["store_small"])}</small><b>{e(S["nav"]["store_big"])}</b></span></a>'

def lang_menu(lang, rel, page):
    items = []
    for l, (folder, _, _, native, _) in LANGS.items():
        href = f"{rel}{folder}{page}"
        cur = ' class="current"' if l == lang else ""
        items.append(f'<a href="{href}" data-lang="{l}" hreflang="{LANGS[l][2]}"{cur}>{e(native)}<small>{l.upper() if l != "pt-BR" else "PT"}</small></a>')
    return f'<details class="lang"><summary aria-label="Language">🌐 {lang.upper() if lang != "pt-BR" else "PT"}</summary><div class="lang-menu">{"".join(items)}</div></details>'

def nav(S, lang, rel, page, home):
    n = S["nav"]
    links = (f'<a href="{rel}index.html#guided">{e(n["features"])}</a><a href="{rel}index.html#free">{e(n["free"])}</a><a href="{rel}index.html#faq">{e(n["faq"])}</a>'
             f'<a href="{rel}{LANGS[lang][0]}PrivacyPolicy.html">{e(n["privacy"])}</a><a href="{rel}{LANGS[lang][0]}TermsAndConditions.html">{e(n["terms"])}</a>')
    return f"""<nav class="nav"><div class="nav-inner">
  <a class="brand" href="{home}"><img class="brand-mark brand-mark-light" src="{rel}assets/img/appicon.png" alt=""><img class="brand-mark brand-mark-dark" src="{rel}assets/img/appicon-dark.png" alt="">LiftSmart</a>
  <div class="nav-links">{links}</div>
  <div class="nav-spacer"></div>
  {lang_menu(lang, rel, page)}
  <button class="icon-btn" onclick="toggleTheme()" aria-label="{e(n["theme"])}"><span class="icon-moon" aria-hidden="true">☾</span><span class="icon-sun" aria-hidden="true">☀︎</span></button>
  {store_btn(S)}
</div></nav>
"""

def footer(S, lang, rel):
    f = S["footer"]; folder = LANGS[lang][0]
    return f"""<footer class="footer"><div class="container footer-inner">
  <span>&copy; 2026 LiftSmart. {e(f["rights"])}</span>
  <div class="footer-links"><a href="{rel}{folder}index.html">{e(f["home"])}</a><a href="{rel}{folder}PrivacyPolicy.html">{e(f["privacy"])}</a><a href="{rel}{folder}TermsAndConditions.html">{e(f["terms"])}</a><a href="{rel}{folder}DeleteInstructions.html">{e(f["delete"])}</a><a href="mailto:{EMAIL}">{e(f["support"])}</a></div>
</div></footer>
</body>
</html>
"""

def phone(rel, lang, shot, cls="", alt=""):
    return f'<div class="phone {cls}"><img src="{rel}assets/img/shots/{lang}/{shot}.jpg" alt="{e(alt)}" loading="lazy"></div>'

def index(S, lang):
    rel = "../" if lang != "en" else ""; folder = LANGS[lang][0]
    h = S["hero"]; out = head(S, lang, rel, "index.html", S["meta"]["index_title"], S["meta"]["index_description"])
    out += nav(S, lang, rel, "index.html", f"{rel}{folder}index.html")
    out += f"""<header class="hero"><div class="container">
  <div class="kicker">{e(h["kicker"])}</div>
  <h1>{e(h["h1_a"])} <span class="accent">{e(h["h1_b"])}</span></h1>
  <p class="lede">{e(h["lede"])}</p>
  <div class="hero-actions">{store_btn(S, "lg")}<a class="btn-ghost" href="#guided">{e(h["cta_ghost"])}</a></div>
  <p class="hero-note">{e(h["note"])}</p>
  <div class="hero-phones">
    {phone(rel, lang, "plans", "p-left", h["alt_left"])}
    {phone(rel, lang, "home", "p-main", h["alt_main"])}
    {phone(rel, lang, "history", "p-right", h["alt_right"])}
  </div>
</div></header>
"""
    # feature blocks
    out += '<section class="section" id="guided"><div class="container">'
    sh = S["features_head"]
    out += f'<div class="section-head"><div class="kicker">{e(sh["kicker"])}</div><h2><span>{e(sh["h_a"])}</span><span class="accent">{e(sh["h_b"])}</span></h2><p>{e(sh["p"])}</p></div>'
    for i, b in enumerate(S["blocks"], 1):
        cls = " ".join(x for x in ["block", "flip" if b.get("flip") else "", "accent-block" if b.get("accent") else ""] if x)
        bullets = "".join(f"<li>{e(x)}</li>" for x in b.get("bullets", []))
        out += f"""<div class="{cls}" id="{b['id']}"><div class="block-text"><div class="kicker">{i:02d} / {e(b["kicker"])}</div><h2><span>{e(b["h_a"])}</span><span class="accent">{e(b["h_b"])}</span></h2><p>{e(b["p"])}</p><ul>{bullets}</ul></div>{phone(rel, lang, b["shot"], "", b.get("alt", ""))}</div>"""
    out += "</div></section>"
    # free grid
    fr = S["free"]
    cards = "".join(f'<div class="card"><div class="num">{i:02d}</div><h3>{e(c["t"])}</h3><p>{e(c["p"])}</p></div>' for i, c in enumerate(fr["cards"], 1))
    chips = "".join(f'<span class="chip">{e(c)}</span>' for c in fr.get("chips", []))
    out += f'<section class="section" id="free"><div class="container"><div class="section-head"><div class="kicker">{e(fr["kicker"])}</div><h2><span>{e(fr["h_a"])}</span><span class="accent">{e(fr["h_b"])}</span></h2><p>{e(fr["p"])}</p></div><div class="grid">{cards}</div><div class="chips">{chips}</div></div></section>'
    # faq
    fq = S["faq"]
    items = "".join(f'<details><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p></details>' for q in fq["items"])
    out += f'<section class="section" id="faq"><div class="container faq"><div><div class="kicker">{e(fq["kicker"])}</div><h2><span>{e(fq["h_a"])}</span><span class="accent">{e(fq["h_b"])}</span></h2></div><div class="faq-list">{items}</div></div></section>'
    # cta
    c = S["cta"]
    out += f'<section class="cta"><div class="container"><div class="kicker">{e(c["kicker"])}</div><h2>{e(c["h_a"])} <span class="accent">{e(c["h_b"])}</span></h2><p>{e(c["p"])}</p>{store_btn(S, "lg")}<p class="fine">{e(c["fine"])}</p></div></section>'
    out += footer(S, lang, rel)
    return out

def legal(S, lang, key, page):
    rel = "../" if lang != "en" else ""; folder = LANGS[lang][0]; L = S["legal"]; D = L[key]
    out = head(S, lang, rel, page, f'{D["title"]} — LiftSmart', D["description"])
    out += nav(S, lang, rel, page, f"{rel}{folder}index.html")
    toc = "".join(f'<li><a href="#{s["id"]}">{e(s["title"])}</a></li>' for s in D["sections"])
    body = "".join(f'<h2 id="{s["id"]}">{e(s["title"])}</h2>{s["html"]}' for s in D["sections"])
    body = body.replace("{{EMAIL}}", EMAIL)
    governs = f'<div class="governs">{e(L["governs"])}</div>' if lang != "en" and L.get("governs") else ""
    out += f"""<main class="container legal-wrap">
  <aside class="legal-side"><div class="toc"><strong>{e(L["contents"])}</strong><ul>{toc}</ul></div></aside>
  <article class="legal">
    <h1>{e(D["title"])}</h1>
    <p class="updated">{e(L["updated_label"])}: {e(D["updated"])}</p>
    {governs}
    {D["intro"].replace("{{EMAIL}}", EMAIL)}
    {body}
  </article>
</main>
"""
    out += footer(S, lang, rel)
    return out

def main():
    for lang, (folder, *_ ) in LANGS.items():
        p = os.path.join(ROOT, "build", "strings", f"{lang}.json")
        if not os.path.exists(p): print("skip", lang, "(no strings)"); continue
        S = json.load(open(p, encoding="utf-8"))
        outdir = os.path.join(ROOT, folder) if folder else ROOT
        os.makedirs(outdir, exist_ok=True)
        open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(index(S, lang))
        for key, page in [("terms", "TermsAndConditions.html"), ("privacy", "PrivacyPolicy.html"), ("delete", "DeleteInstructions.html")]:
            open(os.path.join(outdir, page), "w", encoding="utf-8").write(legal(S, lang, key, page))
        print("built", lang, "->", folder or "/")

if __name__ == "__main__": main()
