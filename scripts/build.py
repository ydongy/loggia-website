#!/usr/bin/env python3
"""Build the Loggia website pages from i18n/*.json and changelog.json.

Run from the repo root after changing copy, languages or the changelog: python3 scripts/build.py

Shared structure (head, header, footer, FAQ, changelog, 404, sitemap, lang.js) lives in scripts/sitekit
(vendored from ydongy's sitekit repository, see scripts/sitekit/VERSION). This file holds what is
specific to Loggia: the site settings and the home page (the chain graphic and the screenshot carousel).
- i18n/languages.json lists the languages: URL path, HTML lang and the browser language prefixes that
  redirect to it. Each language needs public/img/app-<code>-<scene>-{light,dark}.webp (exported by the
  app repo's scripts/export-website-shots.sh). A language is built only if i18n/<code>.json exists.
- i18n/<code>.json holds the copy. Strings may contain HTML; "{{root}}" in links becomes the
  language's path prefix.
- Every page has exactly one address. The output is committed; the site itself has no build step.
"""
from pathlib import Path

from sitekit import Page, Site, attr, build
from sitekit.core import DEFAULT_PAGES, load

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SITE = Site(
    root=ROOT,
    url="https://useloggia.com",
    name="Loggia",
    contact="support@useloggia.com",
    theme=(("#f7f8f7", "light"), ("#0e1211", "dark")),
    og_image=("/og.png", 1200, 630),
    pages={**DEFAULT_PAGES, "support": "/support"},
)

# The live Dodo checkout of Loggia Pro (docs/content.md, Copy sources). The price, tax and key delivery are set on the product there.
CHECKOUT_URL = "https://checkout.dodopayments.com/buy/pdt_0NpQI1RCtsxAnPDY5N5xH"

ICON = {
    "mac": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><rect x="3" y="3.5" width="10" height="7" rx="1.3"/><path d="M 1.5 12.5h13"/></svg>',
    "arch": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><path d="M 2.5 13V8a5.5 5.5 0 0 1 11 0v5"/><path d="M 6 13V9a2 2 0 0 1 4 0v4"/></svg>',
    "cloud": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M 4.6 12.5h6.9a2.9 2.9 0 0 0 .3-5.8A4 4 0 0 0 4.1 7.3a2.6 2.6 0 0 0 .5 5.2z"/></svg>',
    "globe": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="8" cy="8" r="6"/><path d="M 2 8h12M8 2c2 2 2 10 0 12M8 2c-2 2-2 10 0 12"/></svg>',
}
NODE_ICONS = ["mac", "arch", "cloud", "globe"]
SCENES = ["main", "link", "publish", "access", "panel"]



def webp_size(path):
    """Width and height of a WebP file (VP8, VP8L or VP8X), read from its header."""
    data = path.read_bytes()[:30]
    kind = data[12:16]
    if kind == b"VP8X":
        return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
    if kind == b"VP8L":
        bits = int.from_bytes(data[21:25], "little")
        return 1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF)
    if kind == b"VP8 ":
        return int.from_bytes(data[26:28], "little") & 0x3FFF, int.from_bytes(data[28:30], "little") & 0x3FFF
    raise SystemExit(f"{path}: not a WebP file")



class LoggiaPage(Page):
    def lang_summary(self):
        return f'<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.25"/><path d="M 1.75 8h12.5M8 1.75c1.7 1.8 2.5 3.9 2.5 6.25S9.7 12.45 8 14.25C6.3 12.45 5.5 10.35 5.5 8S6.3 3.55 8 1.75z"/></svg><span>{self.t["name"]}</span>'

    def tagline(self):
        # Chinese and Japanese headlines are written without spaces between the parts.
        return ("" if self.l["code"] in ("zh", "zh-hant", "ja") else " ").join(self.t["home"]["h1"])

    def contact_link(self):
        return (f"mailto:{self.site.contact}", self.site.contact.replace("@", "<wbr>@"))

    def footer(self, page):
        """The shared footer with "Contact support" first in the Support column (`/support` is this site's own page)."""
        n, p = self.t["nav"], self.p
        faq = f'<a href="{p}/faq">{n["faq"]}</a>'
        return super().footer(page).replace(faq, f'<a href="{p}/support">{n["contact_support"]}</a>{faq}', 1)

    def support(self):
        """How to reach us: the address, what to write, how to send diagnostics (`docs/content.md`)."""
        s = self.t["support"]
        secs = "\n\n".join(f'<h2>{x["h"]}</h2>\n{self.root(x["body"])}' for x in s["sections"])
        return self.article("support", f'<h1>{s["h1"]}</h1>\n<p class="lead">{s["lead"]}</p>\n\n{secs}')

    def chain(self, nodes, states, wires, label):
        out = [f'<div class="chain" role="img" aria-label="{attr(label)}">']
        for i, node in enumerate(nodes):
            out.append(f'<div class="node {states[i]}"><span class="ring">{ICON[NODE_ICONS[i]]}</span><b>{node["name"]}</b><small>{node["detail"]}</small></div>')
            if i < 3:
                out.append(f'<span class="wire {wires[i]}"></span>')
        out.append("</div>")
        return "\n".join(out)

    def home(self):
        t, h = self.t, self.t["home"]
        p = self.p
        spans = lambda parts: parts[0] if len(parts) == 1 else "".join(f"<span>{x}</span>" for x in parts)
        js = t["download_js"]
        lamps = "\n".join(f'<div><span class="lamp {c}"></span><h3>{x["title"]}</h3><p>{x["text"]}</p></div>'
                          for c, x in zip(["on", "warn", "error", "off"], h["lamps"]))
        facts = "\n".join(f'<div><h3>{x["title"]}</h3><p>{self.root(x["text"])}</p></div>' for x in h["facts"])
        steps = "\n".join(f'<li><h3>{x["title"]}</h3><p>{x["text"]}</p></li>' for x in h["steps"])
        rows = "\n".join(
            f'<tr><th scope="row">{r["label"]}</th>'
            + "".join(f'<td>{(f"<span aria-label={chr(34)}{attr(h["not_included"])}{chr(34)}>-</span>" if v == "-" else v)}</td>' for v in (r["free"], r["pro"]))
            + "</tr>" for r in h["plans"])
        app_langs = f'\n<p class="note">{h["app_languages"]}</p>' if h.get("app_languages") else ""
        body = f'''{self.header("index")}
<main id="main">
<section class="hero wrap">
<h1>{spans(h["h1"])}</h1>
<p class="lead">{spans(h["lead"])}</p>
<a class="button" href="#download">{h["download_cta"]}</a>
<p class="state"><span class="lamp on breathe"></span>{h["state"]}</p>
{self.chain(h["nodes"], ["on"] * 4, ["lit"] * 3, h["chain_label"])}
</section>

{self.carousel()}

<section class="section wrap" id="lamps">
<h2>{h["lamps_h"]}</h2>
<p class="lead">{h["lamps_lead"]}</p>
<div class="lamps">
{lamps}
</div>
</section>


<section class="section wrap" id="account">
<h2>{h["facts_h"]}</h2>
<div class="facts">
{facts}
</div>
</section>

<section class="section wrap" id="how">
<h2>{h["steps_h"]}</h2>
<ol class="steps">
{steps}
</ol>
</section>

<section class="section wrap download" id="download" data-version="{attr(js["version"])}" data-version-no-os="{attr(js["version_no_os"])}" data-button="{attr(js["button"])}" data-error="{attr(js["error"])}">
<h2>{h["download_h"]}</h2>
<p class="lead">{h["download_lead"]}</p>
<p class="status" id="status">{h["status_default"]}</p>{app_langs}
<div class="actions">
<a class="button" id="download-button" href="#" hidden>{h["download_button"]}</a>
<a class="button secondary" id="buy-button" href="{CHECKOUT_URL}" rel="noopener">{h["buy_button"]}</a>
</div>
<p class="official"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M 8 1.5 2.5 3.5v4c0 3.3 2.3 6 5.5 7 3.2-1 5.5-3.7 5.5-7v-4z"/><path d="m5.5 8 1.8 1.8L10.7 6.4"/></svg><span>{t["nav"]["official"]}</span></p>
<noscript><p class="note">{h["noscript"]}</p></noscript>
<p class="note">{h["purchase_note"]}</p>
<p class="checksum" id="checksum" hidden><span id="sha"></span><br>{h["checksum_hint"]}</p>

<div class="plans-wrap" id="pricing">
<table class="plans">
<thead><tr><th scope="col"><span class="visually-hidden">{h["plan_feature"]}</span></th><th scope="col">{h["plan_free"]}</th><th scope="col">{h["plan_pro"]}</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
<p class="terms">{self.root(h["terms"])}</p>
</div>

<p class="install">{self.root(h["install"])}</p>
</section>
</main>
'''
        return self.head("index", t["meta"]["home_title"], t["meta"]["home_desc"], '\n<script src="/download.js" defer></script>\n<script src="/carousel.js" defer></script>') + body + self.footer("index")

    def carousel(self):
        """Screenshots of the app in this language; scroll-snap slides, enhanced by carousel.js."""
        c, code = self.t["home"]["carousel"], self.l["code"]
        chevron = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="{}"/></svg>'
        slides, dots = [], []
        for i, (scene, slide) in enumerate(zip(SCENES, c["slides"])):
            light, dark = f"/img/app-{code}-{scene}-light.webp", f"/img/app-{code}-{scene}-dark.webp"
            w, h = webp_size(PUBLIC / light.lstrip("/"))
            dw, dh = webp_size(PUBLIC / dark.lstrip("/"))
            lazy = "" if i == 0 else ' loading="lazy"'
            slides.append(
                f'<figure class="slide {scene}" id="shot-{scene}" aria-roledescription="slide" aria-label="{i + 1} / {len(SCENES)}">'
                f'<div class="frame"><picture><source srcset="{dark}" media="(prefers-color-scheme: dark)" width="{dw}" height="{dh}">'
                f'<img src="{light}" width="{w}" height="{h}" alt="{attr(slide["alt"])}"{lazy} decoding="async"></picture></div>'
                f'<figcaption><b>{slide["title"]}</b> {slide["text"]}</figcaption></figure>')
            dots.append(f'<a href="#shot-{scene}" aria-label="{attr(slide["title"])}"{" aria-current=\"true\"" if i == 0 else ""}></a>')
        return (f'<section class="carousel wrap" aria-roledescription="carousel" aria-label="{attr(c["label"])}">\n'
                f'<div class="slides" tabindex="0">\n' + "\n".join(slides) + '\n</div>\n'
                f'<div class="carousel-nav"><button type="button" class="prev" aria-label="{attr(c["prev"])}" hidden>{chevron.format("M 10 3 5 8l5 5")}</button>'
                f'<span class="dots">{"".join(dots)}</span>'
                f'<button type="button" class="next" aria-label="{attr(c["next"])}" hidden>{chevron.format("m6 3 5 5-5 5")}</button></div>\n</section>')


def build_support():
    """`build()` writes the shared pages; `/support` is Loggia's own, written beside them in every language."""
    langs, copy = load(SITE)
    for lang in langs:
        out = PUBLIC / lang["path"].lstrip("/")
        (out / "support.html").write_text(LoggiaPage(SITE, lang, langs, copy).support(), encoding="utf-8")


if __name__ == "__main__":
    build(SITE, LoggiaPage)
    build_support()
