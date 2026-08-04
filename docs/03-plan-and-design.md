# Plan & design direction

## The idea

> ## One car a day.

Everything hangs off this. It is true, it is verifiable, it is the reason the price is what it is, and no competitor in Kent can copy it without halving their revenue. The award, the 29 five-star reviews, the premium products and the female-owned advantage are all *evidence* for it — not competing headlines.

Supporting line: **Mobile detailing across Kent. Yours is the only car I touch that day.**

## Voice

Confident, plain, specific. First person (it *is* one person) but edited — no "i", no "Dependant", no shouting. Numbers over adjectives: "3–12 hours on one car" beats "meticulous attention to detail". Never apologise for the price; explain it once, well, and move on.

---

## Information architecture

Flat, shallow, and built so every page has an obvious next step toward booking.

```
/                          Home
/services/                 Hub — all packages, tiered
  /services/exterior-detail/
  /services/interior-detail/
  /services/interior-exterior-detail/
  /services/ceramic-coating/
  /services/paint-correction/
  /services/ultimate-experience/
  /services/maintenance-plan/
  /services/smart-repair/          scratch · alloy · badge · vinyl
/pricing/                  Full canonical price list, one page
/book/                     Guided enquiry → slot confirmed → 20% deposit
/gallery/                  Recent work
/reviews/                  All reviews + aggregate rating
/about/                    Ash's story — the differentiator
/faq/                      Objection handling
/contact/                  NAP, map, form
/areas/                    Hub
  /areas/canterbury/  /areas/maidstone/  /areas/medway/
  /areas/sittingbourne/  /areas/ashford/  /areas/tonbridge/
  /areas/tunbridge-wells/  /areas/whitstable/  /areas/london-outskirts/
```

**Header nav** (nothing hidden behind a `···`): Services · Pricing · Gallery · Reviews · About · Contact — plus a permanent **call button** and a **Book** button.
**Mobile:** sticky bottom bar — `Call` | `WhatsApp` | `Book` — visible on every page, always.

### Fixes this IA delivers
- Contact and FAQ out of the overflow menu (U1)
- Phone in the header on every page, tap-to-call (U2)
- An About page finally exists (U10)
- Nine location pages where there were none (S6)
- Every terminal page (gallery, reviews, FAQ) ends in a booking CTA (C8)

---

## Design system

### Palette

Deep automotive black — the colour of a car under studio lighting — with an ice-blue accent carried over from the logo, and gold reserved *only* for stars and the award.

| Token | Hex | Use |
|---|---|---|
| `--ink-900` | `#0A0C0F` | Page base |
| `--ink-800` | `#10141A` | Alternate sections |
| `--ink-700` | `#171D25` | Cards, panels |
| `--ink-600` | `#212932` | Raised surfaces |
| `--line` | `#262E38` | Hairlines, borders |
| `--text` | `#F5F2EC` | Primary text (warm white, not harsh) |
| `--muted` | `#A8AEB6` | Secondary text |
| `--faint` | `#6B7178` | Captions, meta |
| `--accent` | `#4DB8FF` | Primary accent, links, focus |
| `--accent-deep` | `#0E7FD4` | Gradients, hover, button depth |
| `--gold` | `#E8B84B` | Stars and the award badge **only** |

Fixes B1 (no more underlined blue H1) and B2 (a real system, not builder defaults).

### Type

**System font stack — zero webfont bytes, zero layout shift, instant first paint.** SF Pro on Apple, Segoe UI Variable on Windows, Roboto on Android. All three are excellent; the craft comes from the scale and tracking, not from a downloaded file.

Fluid scale via `clamp()`:

| Role | Size | Weight / tracking |
|---|---|---|
| Display | `clamp(2.75rem, 1.6rem + 5.2vw, 5.5rem)` | 750 · `-0.035em` · lh 0.98 |
| H1 | `clamp(2.25rem, 1.5rem + 3.2vw, 4rem)` | 700 · `-0.03em` |
| H2 | `clamp(1.75rem, 1.3rem + 2vw, 2.75rem)` | 700 · `-0.02em` |
| H3 | `clamp(1.25rem, 1.1rem + .7vw, 1.5rem)` | 650 · `-0.01em` |
| Lead | `clamp(1.06rem, 1rem + .4vw, 1.25rem)` | 400 · lh 1.65 |
| Body | `1.0625rem` | 400 · lh 1.7 |
| Meta | `0.875rem` | 500 · `0.02em` |

Measure capped at 66ch. Numerals tabular in price tables.

### Space & shape

Scale `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128`. Content max-width 1200px, gutter `clamp(1.25rem, 4vw, 3rem)`. Radii kept tight and mechanical — `6px` / `10px` / `16px`, pills only for badges.

### Motion

Scroll-reveal at 8px translate / 400ms, staggered. Before-after sliders drag at 1:1. Everything inside `@media (prefers-reduced-motion: reduce)` guards.

---

## Page designs

### Home — the sequence

The current homepage is seven identical 50/50 slabs (B4). This one changes rhythm every section and asks for the booking four times.

1. **Hero** — full-bleed photograph, dark gradient scrim, `ONE CAR A DAY` display type, one-line subhead, **two buttons** (`Book your detail` / `See the work`), and a trust row directly beneath: `29 × 5★` · `Award winner` · `Fully insured` · `Mobile across Kent`. *Fixes C1, C2.*
2. **Next available slot** — a single line, high contrast: "Next available: [date] — one car a day, so slots go quickly." *Fixes U6, turns the constraint into urgency.*
3. **The work** — full-bleed before/after strip. Biggest images on the page. *Fixes B5.*
4. **Three tiers** — Exterior £100 · **Interior + Exterior £180 (most popular)** · Ceramic from £340. Middle tier raised, bordered in accent, badged. *Fixes C3, U3.*
5. **Why one car a day** — asymmetric, image bleeding off the left edge, tight copy right. The manifesto section.
6. **Reviews** — three real reviews, gold stars, aggregate `5.0 from 29`, link to Google. *Fixes U7.*
7. **Service areas** — nine linked towns, not a plain text list. *Fixes S6.*
8. **Objections** — four FAQs inline, including "Why are you more expensive than a car wash?" *Fixes C6.*
9. **Book** — the form, with the 20% deposit framed as reassurance. *Fixes C5.*

### Services hub & detail pages
Cards with real photography (her service images map 1:1 to services). Each detail page: what's included as a checklist, who it's for, how long it takes, the price table for that service's variants, gallery strip, FAQs, CTA. `Service` + `BreadcrumbList` schema each.

### Pricing
The whole canonical list on one page, grouped, with surcharges and discounts stated plainly. This is the page that ends the £100-vs-£140 confusion for good.

### Book
Guided, typed fields — **not** a free-text "contact details" textarea (U5): name · email · phone · postcode · vehicle make/model · package · condition notes · preferred dates. Progressive, validated, with the deposit and what-happens-next spelled out. **Order corrected: choose → Ash confirms the slot → 20% deposit.** *Fixes C4.*

### Gallery
Optimised WebP grid, lightbox, captions naming the vehicle and the package. YouTube videos behind click-to-load facades. *Fixes U8, U9, P5.*

### Area pages
Each genuinely differentiated — travel notes, local context, which packages are most booked there, area-specific FAQs. **Not** nine copies of one template with the town name swapped; that earns a doorway-page penalty rather than rankings.

---

## SEO plan

| Fix | Detail |
|---|---|
| Titles (S1) | Every page geo-targeted. Home: `Mobile Car Detailing Canterbury & Kent \| Ash's Vehicle Valet & Detailing` |
| Descriptions (S2) | Hand-written per page — location, differentiator, CTA. No boilerplate. |
| Schema (S3, S5) | `AutoDetailing` (not generic `LocalBusiness`) with real `geo`/`GeoCoordinates`, `postalCode`, `areaServed`, `priceRange`, `image`, populated `sameAs`, proper `openingHoursSpecification`. Plus `Service` per package, `FAQPage`, `AggregateRating` + `Review`, `BreadcrumbList`, `VideoObject`. |
| Hours (S4) | Real hours, not 00:00–24:00 seven days. |
| Headings (S7) | One H1 per page, clean hierarchy, no `&nbsp;` padding, stats are not H3s. |
| Open Graph (S8) | Full OG + Twitter card on every page with a proper 1200×630 image. Fixes blank shares on TikTok/Facebook/WhatsApp. |
| Copy (S9) | Everything rewritten and edited. |
| NAP (B6) | One name everywhere: **Ash's Vehicle Valet and Detailing Ltd**. |
| Plumbing | Canonicals, `sitemap.xml`, `robots.txt`, semantic landmarks, skip link. |

## Performance budget

| Metric | Target |
|---|---|
| HTML per page | < 30 KB (from 350 KB — P1) |
| LCP | < 1.5 s |
| CLS | < 0.02 (explicit `width`/`height` on every image) |
| JS shipped | < 6 KB, vanilla, deferred |
| Webfonts | **0 bytes** |
| Hero image | < 60 KB AVIF/WebP responsive (from 617 KB — P3) |
| Lighthouse | 95+ Performance · 100 SEO · 100 Best Practices · 100 Accessibility |

Every image goes through a Pillow pipeline at build time → WebP at 400/800/1200/1600 with correct `srcset`/`sizes`, `loading="lazy"` and `decoding="async"` on everything below the fold, `fetchpriority="high"` on the hero only. *Fixes P2, P3, P4, P6.*

## Architecture

Zero runtime dependencies. `build.py` (Python 3, Pillow) renders HTML partials + JSON data to a flat `dist/` folder that deploys anywhere — Netlify, Cloudflare Pages, or straight to IONOS.

```
build.py              generator + image pipeline
src/
  data/               site · pricing · services · areas · faqs · reviews · gallery
  templates/          base + page partials
  styles/main.css
  scripts/main.js
  images/             source photography
dist/                 deployable output
```

Prices, services and areas all live in JSON. **Changing a price is a one-line edit in one file** — which is precisely what caused the £120-vs-£140 problem in the first place.
