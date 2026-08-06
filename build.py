#!/usr/bin/env python3
"""
Static site generator for Ash's Vehicle Valet and Detailing Ltd.

Zero runtime dependencies beyond Pillow. Reads JSON data + HTML partials from
src/ and writes a flat, deployable site to dist/.

    python3 build.py            build once
    python3 build.py --serve    build, then serve dist/ on :8000
    python3 build.py --clean    wipe caches and rebuild from scratch
    python3 build.py --preview  build a share-safe copy (noindex) for review
    python3 build.py --preview --zip
                                ...and package it as a zip ready to drop on Netlify

Everything price-related comes from src/data/pricing.json. Nothing is
hard-coded in a template, so changing a price is a one-line edit in one file.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install pillow")

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DATA = SRC / "data"
TPL = SRC / "templates"
DIST = ROOT / "dist"

# Responsive widths. Never upscales past the source width — the supplied
# photography is low-resolution web copies, and upscaling only wastes bytes.
WIDTHS = [400, 700, 1000, 1400, 1900]
WEBP_QUALITY = 78

# `--preview` builds a share-safe copy: search engines are told to stay away so
# a preview URL can never be indexed and compete with the real site.
PREVIEW = "--preview" in sys.argv


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------

def load(name: str):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


SITE = load("site")
PRICING = load("pricing")
SERVICES = load("services")
AREAS = load("areas")
FAQS = load("faqs")
REVIEWS = load("reviews")
GALLERY = load("gallery")
REDIRECTS = load("redirects")
HEADERS = load("headers")
BEFOREAFTER = load("beforeafter")
REDACTIONS = load("redactions")["images"]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}


# --------------------------------------------------------------------------
# tiny template engine
#   {{ key }}          -> escaped substitution
#   {{{ key }}}        -> raw substitution (pre-built HTML)
#   {{> partial }}     -> include src/templates/_partial.html
# --------------------------------------------------------------------------

_PARTIAL_CACHE: dict[str, str] = {}


def partial(name: str) -> str:
    if name not in _PARTIAL_CACHE:
        _PARTIAL_CACHE[name] = (TPL / f"_{name}.html").read_text(encoding="utf-8")
    return _PARTIAL_CACHE[name]


def render(template: str, ctx: dict) -> str:
    for _ in range(6):  # resolve nested includes
        new = re.sub(r"\{\{>\s*([\w-]+)\s*\}\}", lambda m: partial(m.group(1)), template)
        if new == template:
            break
        template = new

    def raw(m):
        return str(ctx.get(m.group(1).strip(), ""))

    def esc(m):
        return html.escape(str(ctx.get(m.group(1).strip(), "")), quote=True)

    template = re.sub(r"\{\{\{\s*([\w.-]+)\s*\}\}\}", raw, template)
    template = re.sub(r"\{\{\s*([\w.-]+)\s*\}\}", esc, template)
    return template


def e(text) -> str:
    return html.escape(str(text), quote=True)


def money(v) -> str:
    """£100 not £100.00 — whole pounds throughout."""
    if isinstance(v, (int, float)):
        v = int(v)
        return f"£{v:,}"
    return str(v)


def markdown_lite(text: str) -> str:
    """Bold, links and paragraphs. Deliberately not a full markdown parser."""
    out = []
    for para in text.split("\n\n"):
        para = e(para).replace("\n", "<br>")
        para = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", para)
        para = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', para)
        out.append(f"<p>{para}</p>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# image pipeline
# --------------------------------------------------------------------------

@dataclass
class Img:
    srcset: str
    fallback: str
    width: int
    height: int


_IMG_CACHE: dict[str, Img] = {}


def process_image(rel: str) -> Img | None:
    """Generate responsive WebP derivatives and return srcset data."""
    if rel in _IMG_CACHE:
        return _IMG_CACHE[rel]

    source = SRC / "images" / rel
    if not source.exists():
        print(f"  ! missing image: {rel}")
        return None

    stem = Path(rel).with_suffix("").as_posix().replace("/", "__")
    outdir = DIST / "img"
    outdir.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as im:
        im = _redact(im.convert("RGB"), rel)
        ow, oh = im.size
        targets = [w for w in WIDTHS if w < ow] + [ow]  # never upscale
        entries = []
        for w in targets:
            h = round(oh * w / ow)
            path = outdir / f"{stem}-{w}.webp"
            if not path.exists():
                im.resize((w, h), Image.LANCZOS).save(
                    path, "WEBP", quality=WEBP_QUALITY, method=6
                )
            entries.append(f"/img/{path.name} {w}w")

    img = Img(", ".join(entries), f"/img/{stem}-{targets[-1]}.webp", ow, oh)
    _IMG_CACHE[rel] = img
    return img


def cropped(rel: str, ratio: float, widths: list[int], quality: int, tag: str,
            focus: float = 0.42) -> tuple[str, str] | None:
    """Center-crop to `ratio` (w/h) and emit derivatives. Returns (srcset, fallback).

    Used for the hero: the source is a portrait photo displayed as a landscape
    band, so cropping at build time avoids shipping pixels the browser throws
    away. `focus` is the vertical centre of interest, 0 = top, 1 = bottom.
    """
    source = SRC / "images" / rel
    if not source.exists():
        return None
    stem = Path(rel).with_suffix("").as_posix().replace("/", "__")
    outdir = DIST / "img"
    outdir.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as im:
        im = _redact(im.convert("RGB"), rel)
        ow, oh = im.size
        # largest crop of this ratio that fits inside the source
        cw, ch = (ow, round(ow / ratio)) if ow / oh < ratio else (round(oh * ratio), oh)
        left = (ow - cw) // 2
        top = max(0, min(oh - ch, round(oh * focus - ch / 2)))
        base = im.crop((left, top, left + cw, top + ch))

        entries = []
        targets = [w for w in widths if w < cw] + [min(max(widths), cw)]
        targets = sorted(set(targets))
        for w in targets:
            path = outdir / f"{stem}-{tag}{w}.webp"
            if not path.exists():
                base.resize((w, round(ch * w / cw)), Image.LANCZOS).save(
                    path, "WEBP", quality=quality, method=6
                )
            entries.append(f"/img/{path.name} {w}w")

    return ", ".join(entries), f"/img/{stem}-{tag}{targets[-1]}.webp"


def _redact(im: "Image.Image", rel: str) -> "Image.Image":
    """Blur out any declared regions (customer number plates) before resizing."""
    boxes = REDACTIONS.get(rel)
    if not boxes:
        return im
    from PIL import ImageFilter
    w, h = im.size
    for x0, y0, x1, y1 in boxes:
        box = (int(w * x0), int(h * y0), int(w * x1), int(h * y1))
        region = im.crop(box)
        # Enough to destroy the characters, not so much that it reads as a
        # censor bar — it should still look like a plate, just unreadable.
        # Scales with region height, so it survives every downscale.
        r = max(4, int(region.height * 0.16))
        im.paste(region.filter(ImageFilter.GaussianBlur(r)), box)
    return im


def _trim_letterbox(im: "Image.Image") -> "Image.Image":
    """Strip near-black bars from screenshots that were padded to a fixed frame."""
    from PIL import ImageChops
    bg = Image.new("RGB", im.size, (0, 0, 0))
    mask = ImageChops.difference(im, bg).convert("L").point(lambda p: 255 if p > 18 else 0)
    box = mask.getbbox()
    return im.crop(box) if box else im


def ba_image(rel: str, crop: list[float], aspect: float, tag: str,
             widths: list[int] | None = None) -> tuple[str, str, int, int] | None:
    """One half of a before/after pair, normalised to a shared aspect ratio.

    `crop` is a fractional box on the source; `aspect` is width/height. The two
    halves of a pair must come out identically shaped or the slider looks broken.
    """
    source = SRC / "images" / rel
    if not source.exists():
        print(f"  ! missing image: {rel}")
        return None
    widths = widths or [500, 800, 1200, 1600]
    stem = Path(rel).with_suffix("").as_posix().replace("/", "__")
    outdir = DIST / "img"
    outdir.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as im:
        im = _trim_letterbox(_redact(im.convert("RGB"), rel))
        w, h = im.size
        im = im.crop((int(w * crop[0]), int(h * crop[1]),
                      int(w * crop[2]), int(h * crop[3])))
        w, h = im.size
        # centre-crop to the shared aspect
        if w / h > aspect:
            nw = int(h * aspect)
            im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / aspect)
            im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        cw, ch = im.size

        entries = []
        targets = sorted({min(x, cw) for x in widths})
        for tw in targets:
            path = outdir / f"{stem}-{tag}{tw}.webp"
            if not path.exists():
                im.resize((tw, round(ch * tw / cw)), Image.LANCZOS).save(
                    path, "WEBP", quality=76, method=6
                )
            entries.append(f"/img/{path.name} {tw}w")

    return ", ".join(entries), f"/img/{stem}-{tag}{targets[-1]}.webp", cw, ch


def booking_options(svc: dict) -> list[dict]:
    """Every option a customer can actually book for a service.

    Ash's original site sold Basic/Premium and the ceramic year tiers as
    selectable variants; Premium was her best seller. They live in
    pricing.json, so this surfaces them rather than re-stating any price.
    """
    key = svc.get("priceKey")
    if key:
        return [
            {"label": v["label"], "price": v["total"], "popular": bool(v.get("popular"))}
            for v in PRICING["packages"][key]["variants"]
        ]
    if svc.get("priceNotes"):
        out = []
        for p in svc["priceNotes"]:
            n = re.sub(r"[^0-9]", "", p["price"])
            out.append({"label": p["label"], "price": int(n) if n else None, "popular": False})
        return out
    if svc.get("items"):
        return [{"label": i["name"], "price": None, "popular": False} for i in svc["items"]]
    flat = next((f for f in PRICING["flagship"] if f["slug"] == svc["slug"]), None)
    if flat:
        return [{"label": svc["name"], "price": flat["price"],
                 "unit": flat.get("unit", ""), "popular": False}]
    return []


def options_map() -> dict:
    """Service -> bookable options, embedded once on /book/ for the dependent select."""
    return {s["slug"]: {"name": s["name"], "unit": s.get("unit", ""),
                        "options": booking_options(s)} for s in SERVICES}


def configurator(svc: dict) -> str:
    """Option picker on a service page. One choice, live price, one button —
    the choice is carried into the booking form so nothing is asked twice."""
    opts = booking_options(svc)
    if not opts:
        return ""
    quoted = all(o["price"] is None for o in opts)
    default = next((o for o in opts if o["popular"]), opts[0])
    rows = []
    for o in opts:
        price = f" &mdash; {money(o['price'])}{o.get('unit','')}" if o["price"] else " &mdash; quoted"
        flag = " &middot; most booked" if o["popular"] else ""
        sel = " selected" if o is default else ""
        rows.append(f'<option value="{e(o["label"])}" data-price="{o["price"] or ""}"{sel}>'
                    f'{e(o["label"])}{price}{flag}</option>')
    dp = f"{money(default['price'])}{default.get('unit','')}" if default["price"] else "Quoted"
    return f"""<form class="cfg" data-cfg data-slug="{svc['slug']}" action="/book/" method="get">
  <input type="hidden" name="service" value="{svc['slug']}">
  <div class="cfg__row">
    <label class="cfg__label" for="cfg-{svc['slug']}">
      {'Which one do you need?' if not quoted else 'What do you need?'}
    </label>
    <select class="cfg__select" id="cfg-{svc['slug']}" name="option">{''.join(rows)}</select>
  </div>
  <div class="cfg__foot">
    <p class="cfg__price"><span>{'Price' if not quoted else ''}</span><b data-cfg-price>{dp}</b></p>
    <button class="btn btn--primary btn--lg" type="submit">Book this &rarr;</button>
  </div>
  <p class="cfg__note">Your choice carries through to the booking form &mdash; you won&rsquo;t be asked twice.</p>
</form>"""


def before_after(pair: dict, sizes: str = "(min-width:900px) 46vw, 92vw") -> str:
    """Draggable comparison slider. Works without JS as a plain stacked pair."""
    a = pair["aspect"]
    bef = ba_image(pair["before"]["src"], pair["before"]["crop"], a, "ba")
    aft = ba_image(pair["after"]["src"], pair["after"]["crop"], a, "ba")
    if not bef or not aft:
        return ""
    slug = pair["slug"]
    return f"""<figure class="ba" data-ba style="--ba-aspect:{a}">
  <div class="ba__stage">
    <img class="ba__img ba__img--after" src="{aft[1]}" srcset="{aft[0]}" sizes="{e(sizes)}"
         width="{aft[2]}" height="{aft[3]}" loading="lazy" decoding="async"
         alt="{e(pair['title'])} after detailing by {SITE['shortName']}">
    <div class="ba__before" aria-hidden="true">
      <img class="ba__img" src="{bef[1]}" srcset="{bef[0]}" sizes="{e(sizes)}"
           width="{bef[2]}" height="{bef[3]}" loading="lazy" decoding="async" alt="">
    </div>
    <span class="ba__tag ba__tag--b">Before</span>
    <span class="ba__tag ba__tag--a">After</span>
    <div class="ba__handle" aria-hidden="true"><span></span></div>
    <input class="ba__range" type="range" min="0" max="100" value="50" step="0.1"
           aria-label="Reveal before and after: {e(pair['title'])}"
           id="ba-{slug}">
  </div>
  <figcaption class="ba__cap">
    <strong>{e(pair['title'])}</strong>
    <span>{e(pair['note'])}</span>
  </figcaption>
</figure>"""


def hero_picture(rel: str, alt: str) -> str:
    """Desktop-only hero photograph.

    On mobile the hero shows Ash's logo instead (the landscape crop of a car
    doesn't work in a tall frame), so the <img> fallback is a 1x1 transparent
    pixel — the photo is never downloaded on a phone.
    """
    wide = cropped(rel, 16 / 9, [1000, 1400, 1900], quality=58, tag="hw", focus=0.62)
    # Portrait crop for phones — a landscape band looks wrong in a tall frame,
    # and these sources are natively 3:4 so they crop to it without loss.
    tall = cropped(rel, 3 / 4, [500, 800, 1100], quality=62, tag="hp", focus=0.5)
    if not wide or not tall:
        return picture(rel, alt, "100vw", priority=True)
    return (
        f'<picture>'
        f'<source media="(min-width:760px)" srcset="{wide[0]}" sizes="100vw" type="image/webp">'
        f'<source srcset="{tall[0]}" sizes="100vw" type="image/webp">'
        f'<img src="{tall[1]}" alt="{e(alt)}" width="1200" height="1600" '
        f'fetchpriority="high" decoding="async">'
        f"</picture>"
    )


def picture(rel: str, alt: str, sizes: str = "100vw", cls: str = "",
            priority: bool = False, ratio: str | None = None) -> str:
    img = process_image(rel)
    if not img:
        return ""
    loading = "eager" if priority else "lazy"
    fetch = ' fetchpriority="high"' if priority else ""
    style = f' style="--ratio:{ratio}"' if ratio else ""
    return (
        f'<img class="{e(cls)}" src="{img.fallback}" srcset="{img.srcset}" '
        f'sizes="{e(sizes)}" width="{img.width}" height="{img.height}" '
        f'alt="{e(alt)}" loading="{loading}" decoding="async"{fetch}{style}>'
    )


# --------------------------------------------------------------------------
# structured data
# --------------------------------------------------------------------------

def business_schema() -> dict:
    social = [v for v in SITE["social"].values() if v]
    return {
        "@context": "https://schema.org",
        "@type": "AutoDetailing",
        "@id": f"{SITE['url']}/#business",
        "name": SITE["name"],
        "alternateName": SITE["shortName"],
        "url": SITE["url"] + "/",
        "telephone": SITE["phone"],
        "email": SITE["email"],
        "founder": {"@type": "Person", "name": SITE["owner"]},
        "foundingDate": SITE["foundingDate"],
        "priceRange": SITE["priceRange"],
        "currenciesAccepted": "GBP",
        "paymentAccepted": "Cash, Bank transfer",
        "image": f"{SITE['url']}/img/og.jpg",
        "logo": f"{SITE['url']}/img/home__ash-logo-400.webp",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SITE["street"],
            "addressLocality": SITE["locality"],
            "addressRegion": SITE["region"],
            "postalCode": SITE["postcode"],
            "addressCountry": SITE["country"],
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": SITE["lat"],
            "longitude": SITE["lng"],
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": h["days"],
                "opens": h["opens"],
                "closes": h["closes"],
            }
            for h in SITE["hours"]
        ],
        "areaServed": [
            {"@type": "City", "name": a["name"]} for a in AREAS
        ],
        "sameAs": social,
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": REVIEWS["aggregate"]["rating"],
            "reviewCount": REVIEWS["aggregate"]["count"],
            "bestRating": "5",
            "worstRating": "1",
        },
        "award": SITE["award"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Detailing services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {"@type": "Service", "name": s["name"]},
                    "price": s["from"],
                    "priceCurrency": "GBP",
                    "url": f"{SITE['url']}/services/{s['slug']}/",
                }
                for s in SERVICES
            ],
        },
    }


def breadcrumbs(trail: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": SITE["url"] + href,
            }
            for i, (name, href) in enumerate(trail)
        ],
    }


def faq_schema(items) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": re.sub(r"[*\[\]()]|\(/[\w/-]+\)", "", f["a"]).strip(),
                },
            }
            for f in items
        ],
    }


def review_schema(limit: int | None = None) -> dict:
    """Only mark up the reviews actually rendered on the page — Google expects
    structured data to match visible content."""
    shown = REVIEWS["items"][:limit] if limit else REVIEWS["items"]
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "Review",
                    "author": {"@type": "Person", "name": r["name"]},
                    "reviewRating": {
                        "@type": "Rating",
                        "ratingValue": r["rating"],
                        "bestRating": "5",
                    },
                    "reviewBody": r["text"],
                    "itemReviewed": {"@id": f"{SITE['url']}/#business"},
                },
            }
            for i, r in enumerate(shown)
        ],
    }


def video_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "VideoObject",
                    "name": v["title"],
                    "description": f"{v['title']} — mobile car detailing in Kent by {SITE['shortName']}.",
                    "thumbnailUrl": f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg",
                    "uploadDate": "2026-03-01",
                    "contentUrl": f"https://www.youtube.com/watch?v={v['id']}",
                    "embedUrl": f"https://www.youtube.com/embed/{v['id']}",
                },
            }
            for i, v in enumerate(GALLERY["videos"])
        ],
    }


def service_schema(svc) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": svc["name"],
        "serviceType": svc["name"],
        "description": svc["intro"].split("\n")[0],
        "provider": {"@id": f"{SITE['url']}/#business"},
        "areaServed": [{"@type": "City", "name": a["name"]} for a in AREAS],
        "offers": {
            "@type": "Offer",
            "price": svc["from"],
            "priceCurrency": "GBP",
            "url": f"{SITE['url']}/services/{svc['slug']}/",
            "availability": "https://schema.org/InStock",
        },
    }


# --------------------------------------------------------------------------
# page shell
# --------------------------------------------------------------------------

PAGES: list[dict] = []


def phead_bg(rel: str, focus: float = 0.5) -> str:
    """Wide, dark-scrimmed band behind a page header. Uses Ash's own work
    rather than stock or generated imagery — it's the strongest asset she has."""
    wide = cropped(rel, 21 / 9, [900, 1400, 1900], quality=60, tag="ph", focus=focus)
    if not wide:
        return ""
    return (f'<div class="phead__bg" aria-hidden="true">'
            f'<img src="{wide[1]}" srcset="{wide[0]}" sizes="100vw" alt="" '
            f'loading="lazy" decoding="async"></div>')


def write_page(path: str, *, title: str, description: str, body: str,
               schemas: list | None = None, og_image: str = "og.jpg",
               nav_key: str = "", priority: str = "0.6",
               body_class: str = "", noindex: bool = False,
               in_sitemap: bool = True) -> None:
    """path: '' for home, 'services/exterior-detail' otherwise.

    noindex/in_sitemap exist for pages that must not rank — the post-enquiry
    thank-you page is only reachable after a form POST, so indexing it would
    put a dead-end page in search results.
    """
    url = f"{SITE['url']}/{path + '/' if path else ''}"
    blocks = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>'
        for s in (schemas or [])
    )
    out = render(
        (TPL / "base.html").read_text(encoding="utf-8"),
        {
            "title": title,
            "description": description,
            "canonical": url,
            "og_image": f"{SITE['url']}/img/{og_image}",
            "body": body,
            "schema": blocks,
            "site_name": SITE["name"],
            # Phone comes from site.json so there is one source of truth. The
            # partials (_header, _footer, _mobilebar) are inlined by render()
            # before substitution, so they read these too. wa.me is derived
            # rather than stored — a second copy of the number would drift.
            "phone": SITE["phone"],
            "phone_display": SITE["phoneDisplay"],
            "whatsapp": f"https://wa.me/{SITE['phone'].lstrip('+')}",
            "body_class": body_class,
            "nav": nav_html(nav_key),
            "mnav": mobile_nav_html(nav_key),
            "mega": mega_html(),
            "logo": picture(SITE["logo"], SITE["name"] + " logo", "50px",
                            cls="brand__mark", priority=True),
            # header mark is 50px; the hero mark is up to 236px on phones
            "year": "2026",
            "robots": ("noindex, nofollow" if (PREVIEW or noindex)
                       else "index, follow, max-image-preview:large"),
            "preview_banner": (
                '<div class="pvw">Preview for review &mdash; not the live site. '
                'Spot something? Tell Tyler.</div>' if PREVIEW else ""),
            "css_v": ASSET_V.get("main.css", "1"),
            "js_v": ASSET_V.get("main.js", "1"),
        },
    )
    target = DIST / path / "index.html" if path else DIST / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    if in_sitemap:
        PAGES.append({"loc": url, "priority": priority})


def nav_html(active: str) -> str:
    """Desktop nav. Services is a mega-menu button, rendered in the template."""
    out = []
    for item in SITE["nav"]:
        if item["href"] == "/services/":
            continue
        cur = ' aria-current="page"' if item["href"].strip("/") == active else ""
        out.append(f'<li><a href="{item["href"]}"{cur}>{e(item["label"])}</a></li>')
    return "\n".join(out)


def mobile_nav_html(active: str) -> str:
    out = []
    for item in SITE["nav"]:
        cur = ' aria-current="page"' if item["href"].strip("/") == active else ""
        hint = ""
        if item["href"] == "/services/":
            hint = f'<span>{len(SERVICES)}</span>'
        elif item["href"] == "/areas/":
            hint = f'<span>{len(AREAS)}</span>'
        elif item["href"] == "/reviews/":
            hint = f'<span>{REVIEWS["aggregate"]["count"]}</span>'
        out.append(f'<li><a href="{item["href"]}"{cur}>{e(item["label"])}{hint}</a></li>')
    return "\n".join(out)


def mega_html() -> str:
    """Services mega-menu: thumbnail, name, one line, price. Built from data."""
    out = []
    for s in SERVICES:
        img = process_image(s["image"])
        thumb = (f'<img class="mega__thumb" src="/img/{Path(img.fallback).name.replace(str(img.width), "400")}" '
                 f'alt="" width="58" height="58" loading="lazy" decoding="async">') if img else ""
        # use the smallest generated derivative for the thumbnail
        if img:
            small = img.srcset.split(",")[0].strip().split(" ")[0]
            thumb = (f'<img class="mega__thumb" src="{small}" alt="" width="58" height="58" '
                     f'loading="lazy" decoding="async">')
        out.append(
            f'<a class="mega__i" href="/services/{s["slug"]}/">{thumb}'
            f'<span class="mega__t"><b>{e(s["name"])}</b>'
            f'<span>{e(s["tagline"])}</span>'
            f'<em>from {money(s["from"])}{e(s.get("unit",""))}</em></span></a>'
        )
    return "".join(out)


# --------------------------------------------------------------------------
# reusable HTML fragments
# --------------------------------------------------------------------------

def stars(n: int = 5) -> str:
    star = ('<svg viewBox="0 0 20 19" aria-hidden="true"><path d="M10 0l2.6 6.3 6.8.5-5.2 4.4 1.6 6.6L10 14.3 '
            '4.2 17.8l1.6-6.6L.6 6.8l6.8-.5z"/></svg>')
    return f'<span class="stars" role="img" aria-label="{n} out of 5 stars">{star * n}</span>'


def price_table(key: str) -> str:
    pkg = PRICING["packages"][key]
    rows = []
    for v in pkg["variants"]:
        badge = ' <span class="tag">Most booked</span>' if v.get("popular") else ""
        add = "—" if v["add"] == 0 else f"+{money(v['add'])}"
        rows.append(
            f'<tr{" class=is-popular" if v.get("popular") else ""}>'
            f"<th scope=\"row\">{e(v['label'])}{badge}</th>"
            f'<td class="num" data-label="Extra">{add}</td>'
            f'<td class="num total" data-label="Total">{money(v["total"])}</td></tr>'
        )
    note = f'<p class="note">{e(pkg["note"])}</p>' if pkg.get("note") else ""
    return f"""<div class="table-wrap">
<table class="prices">
<caption class="vh">{e(pkg['name'])} prices</caption>
<thead><tr><th scope="col">Option</th><th scope="col" class="num">Extra</th><th scope="col" class="num">Total</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table></div>{note}"""


def cta_band(heading: str, sub: str, ) -> str:
    return f"""<section class="band">
  <div class="wrap band__inner">
    <div>
      <h2>{e(heading)}</h2>
      <p class="lead">{e(sub)}</p>
    </div>
    <div class="band__actions">
      <a class="btn btn--primary btn--lg" href="/book/">Book your detail</a>
      <a class="btn btn--ghost btn--lg" href="tel:{SITE['phone']}">Call {SITE['phoneDisplay']}</a>
    </div>
  </div>
</section>"""


def faq_list(items, open_first: bool = False) -> str:
    out = []
    for i, f in enumerate(items):
        op = " open" if (open_first and i == 0) else ""
        out.append(
            f'<details class="faq"{op}><summary><span>{e(f["q"])}</span></summary>'
            f'<div class="faq__body">{markdown_lite(f["a"])}</div></details>'
        )
    return f'<div class="faqs">{"".join(out)}</div>'


def service_card(svc, sizes="(min-width:1000px) 32vw, (min-width:640px) 45vw, 90vw") -> str:
    unit = svc.get("unit", "")
    tag = '<span class="card__flag">Most booked</span>' if svc.get("popular") else ""
    return f"""<a class="card{' card--pop' if svc.get('popular') else ''}" href="/services/{svc['slug']}/">
  <div class="card__media">{picture(svc['image'], svc['name'] + ' — ' + svc['tagline'], sizes)}{tag}</div>
  <div class="card__body">
    <h3>{e(svc['name'])}</h3>
    <p>{e(svc['tagline'])}</p>
    <span class="card__price">from <strong>{money(svc['from'])}</strong>{e(unit)}</span>
  </div>
</a>"""


def crumbs_html(trail: list[tuple[str, str]]) -> str:
    parts = []
    for i, (name, href) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<li><span aria-current="page">{e(name)}</span></li>')
        else:
            parts.append(f'<li><a href="{href}">{e(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol class="wrap">{"".join(parts)}</ol></nav>'


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------

ASSET_V: dict[str, str] = {}


def copy_static():
    (DIST / "img").mkdir(parents=True, exist_ok=True)
    import hashlib
    for src_rel, out in [("styles/main.css", "main.css"), ("scripts/main.js", "main.js")]:
        data = (SRC / src_rel).read_bytes()
        (DIST / out).write_bytes(data)
        # content hash so a deploy can never serve a stale stylesheet
        ASSET_V[out] = hashlib.sha256(data).hexdigest()[:8]
    fonts = DIST / "fonts"
    fonts.mkdir(exist_ok=True)
    for f in (SRC / "fonts").glob("*"):
        shutil.copy(f, fonts / f.name)

    # Social share image — 1200x630 crop of the hero.
    og = DIST / "img" / "og.jpg"
    if not og.exists():
        with Image.open(SRC / "images" / SITE["heroImage"]) as im:
            im = im.convert("RGB")
            tw, th = 1200, 630
            scale = max(tw / im.width, th / im.height)
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
            left = (im.width - tw) // 2
            top = max(0, (im.height - th) // 3)
            im.crop((left, top, left + tw, top + th)).save(og, "JPEG", quality=82, optimize=True)

    write_icons()

    if PREVIEW:
        (DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    else:
        (DIST / "robots.txt").write_text(
            f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8"
        )
    write_redirects()
    write_headers()


def write_icons():
    """Favicon + apple-touch-icon generated from Ash's own logo."""
    src = SRC / "images" / SITE["logo"]
    if not src.exists():
        print(f"  ! logo not found: {SITE['logo']}")
        return
    with Image.open(src) as im:
        im = im.convert("RGB")
        # The logo is a detailed badge: the "VEHICLE VALET AND DETAILING LTD"
        # banner is unreadable below ~64px and just adds noise. Crop to the
        # script + car so the small sizes stay recognisable.
        box = SITE.get("logoIconCrop", [0.06, 0.10, 0.94, 0.74])
        w, h = im.size
        sq = im.crop((int(w * box[0]), int(h * box[1]), int(w * box[2]), int(h * box[3])))
        side = max(sq.size)
        pad = Image.new("RGB", (side, side), (0, 0, 0))
        pad.paste(sq, ((side - sq.width) // 2, (side - sq.height) // 2))
        for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"),
                           (512, "icon-512.png")]:
            path = DIST / name
            if not path.exists():
                pad.resize((size, size), Image.LANCZOS).save(path, "PNG", optimize=True)


def write_headers():
    """Security and cache headers as dist/_headers.

    Netlify reads this file automatically, exactly as it does _redirects.
    They are NOT in netlify.toml: its header parser silently dropped
    Content-Security-Policy and Permissions-Policy while still reporting
    "header rules processed without errors". Verified on deploy preview #2.
    """
    lines = ["# Generated by build.py from src/data/headers.json — do not edit."]
    for rule in HEADERS["rules"]:
        lines.append("")
        lines.append(rule["for"])
        for key, value in rule["values"].items():
            lines.append(f"  {key}: {value}")
    (DIST / "_headers").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_redirects():
    """301s from the old IONOS URLs, in both common hosting formats."""
    rules = REDIRECTS["map"]

    (DIST / "_redirects").write_text(
        "# Netlify / Cloudflare Pages\n"
        + "".join(f"{old}  {new}  301\n" for old, new in rules.items()),
        encoding="utf-8",
    )

    lines = [
        "# Apache / IONOS",
        "RewriteEngine On",
        "",
        "# force https + non-www -> www to match the canonical",
        "RewriteCond %{HTTPS} off",
        "RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]",
        "",
        "# old page URLs",
    ]
    for old, new in rules.items():
        # A trailing '*' is Netlify splat syntax; Apache needs a real regex.
        if old.endswith("*"):
            lines.append(f"RedirectMatch 301 ^{old[:-1]}.*$ {new}")
        else:
            lines.append(f"RedirectMatch 301 ^{old}?$ {new}")
    (DIST / ".htaccess").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sitemap():
    entries = "\n".join(
        f"  <url><loc>{p['loc']}</loc><priority>{p['priority']}</priority></url>"
        for p in PAGES
    )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n",
        encoding="utf-8",
    )


def main():
    if "--clean" in sys.argv and DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(exist_ok=True)
    copy_static()

    # pages.py does `import build` — alias this module under that name so it
    # shares our globals (PAGES, caches) instead of re-importing a second copy.
    sys.modules.setdefault("build", sys.modules[__name__])
    import pages  # noqa: E402
    pages.build()

    write_sitemap()

    total = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file())
    htmls = list(DIST.rglob("index.html"))
    biggest = max(htmls, key=lambda f: f.stat().st_size)
    print(f"\n  {len(htmls)} pages · {len(list((DIST / 'img').glob('*')))} images")
    print(f"  largest HTML: {biggest.relative_to(DIST)} @ {biggest.stat().st_size / 1024:.1f} KB")
    print(f"  total dist:   {total / 1024 / 1024:.2f} MB\n")

    if "--zip" in sys.argv:
        # A single zip uploads far more reliably than dragging 160+ nested
        # files into a browser drop zone, which often loses subdirectories.
        import zipfile
        name = "ashs-website-preview.zip" if PREVIEW else "ashs-website.zip"
        out = ROOT / name
        if out.exists():
            out.unlink()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(DIST.rglob("*")):
                if f.is_file() and f.name != ".DS_Store":
                    z.write(f, f.relative_to(DIST))   # contents at zip root
        print(f"  zipped: {name}  ({out.stat().st_size / 1024 / 1024:.1f} MB)")
        print("  drag this file onto https://app.netlify.com/drop\n")

    if "--serve" in sys.argv:
        import http.server, socketserver, os
        os.chdir(DIST)
        with socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler) as s:
            print("  serving http://localhost:8000  (ctrl-c to stop)\n")
            s.serve_forever()


if __name__ == "__main__":
    main()
