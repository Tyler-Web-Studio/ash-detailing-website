# Ash's Vehicle Valet & Detailing — Discovery & Audit

**Date:** 31 July 2026
**Current site:** https://www.ashsautodetailingltd.co.uk/
**Platform:** IONOS "MyWebsite NOW" (WordPress under the hood) — `<meta name="generator" content="MyWebsite NOW">`, `IONOS Webserver`
**Pages indexed:** 11

---

## 1. The business

| | |
|---|---|
| **Trading name** | Ash's Vehicle Valet and Detailing Ltd |
| **Owner** | Ashleigh Loosemore ("Ash") — sole operator |
| **Base** | Pitman Road, Canterbury CT3 4FF (Hersden), Kent |
| **Model** | **Mobile** — travels to the customer. Needs parking, water and a power point within 30m |
| **Trading since** | Late December 2025 (~7 months, part-time) |
| **Phone** | +44 7907 019798 |
| **Email** | ashs_vvad_ltd@icloud.com |
| **VAT** | Not registered — quoted price is the price paid |
| **Insurance** | Fully insured, documents available |

**Service area:** Canterbury, Maidstone, Medway, Sittingbourne, Ashford, Tonbridge, Tunbridge Wells, wider Kent, London outskirts.

**Social:** YouTube (16 videos), TikTok (@ashs.vehicle.valet), Instagram (@ashsautodetailing), Facebook.

### What actually makes this business different

These are the assets. Everything in the rebuild should be in service of them.

1. **One detail per day.** No rushing, no double-booking. This is a genuine, defensible differentiator against every "full valet in 90 minutes" competitor in Kent.
2. **Female-owned and operated** in a male-dominated trade. For a service where a stranger comes to your home and sits in your car, this is a real trust and safety advantage — particularly with women booking, and with older customers.
3. **29 five-star reviews in 7 months, part-time.** A perfect record at meaningful volume.
4. **"Best Detailing Service in South England"** award.
5. **Genuinely strong before/after photography** — the single most under-used asset on the current site.
6. **Growing TikTok audience** — transformation content is the top of the funnel.

### Competitive set (Kent / Canterbury mobile detailing)

Ride & Shine, Devils in the Detail, YK Detailing, AA Car Detailing, Mahoney Valeting, Detailing In Style. Several are established with location-targeted pages. None of them can claim one-detail-per-day + female-owned + a perfect review record. **That is the wedge.**

---

## 2. Current service & price catalogue

Taken from the "Our Services and Prices" page.

### Core packages
| Service | Price |
|---|---|
| Exterior only detail | £100 |
| Interior only detail | £130 |
| Interior + Exterior detail | £180 |
| Premium Exterior detail | £120 |
| Premium Interior detail | £150 |
| Premium Interior + Exterior detail | £240 |
| Premium Exterior + 2-step machine polish | £250 |
| Premium Interior + Exterior + 2-step polish | £350 |
| **The Ultimate Experience** (2-day, drop-off) | £600 |
| Maintenance plan | £70/month |

### Add-ons & specialist work
| Service | Price |
|---|---|
| Ceramic coatings (1–5 yr) | £300+ (quote) |
| Headlight restoration | £50 (+£10/mile if standalone) |
| Ozone treatment | £50 (interior packages only) |
| Engine bay detail | £30 |
| Exterior metal polishing (on £350 pkg) | +£20 |
| SMART scratch / defect repair | £300 +/- (quote, 1 week lead time) |
| SMART alloy repair | £100 per alloy |
| Vinyl / sticker removal | £100–£500 (25% off detail when combined) |
| Badge removal | £100 |

### Surcharges
Excess dirt £20–40 · Mould £20–100 · Pet hair £20–50 · XL vehicles, vans, caravans, HGVs extra.

### Discounts
5% blue light & emergency services · £10 off next booking for leaving a review · Referral: friend gets £10 off, referrer gets £10 cashback.

### Pricing — resolved

Confirmed with Ash, 31 July 2026. The full matrix is in [02-pricing-canonical.md](02-pricing-canonical.md) and machine-readable in `src/data/pricing.json`.

Base prices are **Exterior £100 · Interior £130 · Interior+Exterior £180 · Ceramic £300** (the store's headline "£140" was simply a preselected *Premium* variant, not a separate price).

**Two genuine errors on the live services page:**

| Service | Services page says | Actually | Impact |
|---|---|---|---|
| Premium Exterior Detail | £120 | **£140** (£100 + £40) | Under-quoted by £20 |
| Ceramic Coatings | "£300+" | **£340 floor** (1-year) | The £300 price can never be bought |

**One suspected store data-entry slip:** *Premium Large Van (+£40)* prices out at £140 — identical to a standard car Premium, despite Large Van basic carrying a +£20 surcharge. Expected +£60. Flagged for Ash to confirm; not guessed at in the build.

---

## 3. Audit — what's wrong and why it costs money

### 3.1 Brand & creative

| # | Finding | Why it matters |
|---|---|---|
| B1 | H1 is bright blue, **underlined** text over a busy photo | Reads as a broken hyperlink, not a brand. Fails contrast against the light dashboard behind it. |
| B2 | No brand system — builder-default serif headings, sans body, generic link-blue accent | Nothing says "premium". The palette is the same one on ten thousand other IONOS sites. |
| B3 | Logo is a low-res JPG with a baked-in black box | Floats on the page as a rectangle instead of integrating. Needs a transparent PNG/SVG. |
| B4 | Every section is the same 50/50 image-left / text-right slab | Zero visual rhythm. The eye has nothing to lock onto over ~7,000px of page. |
| B5 | The best asset — before/after photography — is shown as postage stamps in an unlabelled grid | The work sells itself and is being hidden. |
| B6 | Inconsistent naming: "Ash's Auto Detailing Ltd" vs "Ash's Vehicle Valet and Detailing Ltd" | Confuses customers and splits local-SEO signal (NAP consistency). |

### 3.2 UX & information architecture

| # | Finding | Why it matters |
|---|---|---|
| U1 | **Contact** and **FAQ** are hidden behind a `···` overflow menu | The two highest-intent pages after booking are the two hardest to find. |
| U2 | **No phone number in the header** | For a local mobile trade, tap-to-call is the #1 mobile conversion. It's in the footer only. |
| U3 | 17 services as a flat grid of equal-weight cards | Textbook choice paralysis. No recommended option, no "most popular", no guided path. |
| U4 | Store dropdowns say "Basic" / "Premium (+£40)" with no explanation at the point of decision | The difference is explained on a *different page*. Customers guess or leave. |
| U5 | Contact form collects "your contact details" as a **free-text textarea** | No validation, no structured data, high friction. Should be typed name / email / phone / vehicle / postcode fields. |
| U6 | **Availability is never shown** | "One detail per day" is the core promise, yet the site never says when the next slot is. Biggest missed urgency lever on the site. |
| U7 | Reviews page shows **3 of 29** reviews, no stars, no aggregate, no link to Google profile | Under-selling a perfect record. |
| U8 | Gallery: 23 unlabelled thumbnails, no before/after pairing, no vehicle names, no filtering, no CTA out | Traffic arrives, admires, and leaves. |
| U9 | 16 YouTube embeds all captioned "1 March 2026 · Ash's Vehicle Valet and detailing ltd" | No context, no titles that mean anything to a visitor. |
| U10 | No **About** page | The founder story *is* the differentiator and there is nowhere to tell it. |

### 3.3 Conversion (CRO)

| # | Finding | Why it matters |
|---|---|---|
| C1 | **Hero has no CTA button at all.** First CTA is a contact form ~7,000px down | The highest-attention real estate on the site asks for nothing. |
| C2 | No trust signals above the fold — insured, 29×5★, award, service area all appear far down or not at all | Trust has to be established before the scroll, not after. |
| C3 | No three-tier package comparison with a highlighted middle option | Single highest-ROI change available. Anchoring + a recommended tier reliably lifts average order value. |
| C4 | **Customer pays in full *before* a date is confirmed** ("once you have paid, I will be in contact to arrange a date") | Backwards, and a severe conversion killer. Nobody pays £350 for an unscheduled service. Should be: choose → confirm slot → 20% deposit. |
| C5 | The 20% deposit is buried under a heading called "The small print?" | Framed as fine print rather than as reassurance ("secures your slot"). |
| C6 | No FAQ content on home or services pages | The "why are you more expensive than a car wash?" answer is excellent and almost nobody will ever find it. |
| C7 | Discounts (blue light, review, referral) hidden on the FAQ page | These are acquisition levers. They belong where people decide. |
| C8 | No exit path from gallery or reviews back to booking | Dead ends at peak intent. |

### 3.4 SEO

| # | Finding | Why it matters |
|---|---|---|
| S1 | Title: *"Professional Car Detailing Services \| Ash's Auto Detailing"* — **no location** | The single biggest miss. Local intent queries are "mobile car detailing canterbury", not "professional car detailing services". |
| S2 | Meta description is IONOS boilerplate — no location, no differentiator, no CTA | Kills click-through even when ranking. |
| S3 | LocalBusiness JSON-LD present but **thin and partly broken**: `sameAs` is seven empty strings; no `priceRange`, `areaServed`, `aggregateRating`, `image`, `postalCode`; lat/long are loose properties instead of a `GeoCoordinates` node; `openingHours` uses a non-standard shape instead of `openingHoursSpecification`; type is generic `LocalBusiness` rather than `AutoDetailing` | Rich results and map-pack signals left on the table. |
| S4 | Opening hours declared **00:00–24:00, seven days** | Implausible; unhelpful to both users and Google. |
| S5 | No `Service`, `FAQPage`, `Review`/`AggregateRating`, `BreadcrumbList` or `VideoObject` schema | There is a full FAQ page, 29 five-star reviews and 16 videos, all unmarked. |
| S6 | **Zero location landing pages.** Nine towns listed as plain text | This is precisely how local service businesses win. Competitors already have these pages. |
| S7 | Heading misuse — `<h2>&nbsp;&nbsp;My Service areas</h2>`; stat numbers "4", "Up to 15" marked as `<h3>` | Semantic noise weakens topical signals. |
| S8 | **No Open Graph / Twitter card tags** | Every link shared on TikTok, Facebook, Instagram or WhatsApp renders with no image. For a business whose growth engine *is* social, this is expensive. |
| S9 | Copy is thin, first-person and inconsistent — "What Services do i offer?", "Dependant", "i am NOT a body shop" | Reads as unedited. Undermines a premium price point. |
| S10 | No Google Business Profile link, no review-generation path on site | Local pack ranking depends heavily on review velocity. |

### 3.5 Performance

| # | Finding | Why it matters |
|---|---|---|
| P1 | **350 KB of HTML** on the homepage alone | Builder ships enormous inline markup before a single pixel renders. |
| P2 | **Zero `loading="lazy"`** across all 15 homepage images | Everything loads eagerly, including images 6,000px below the fold. |
| P3 | Hero background is a **617 KB JPEG** | Should be ~40–60 KB AVIF/WebP served responsively. Directly damages LCP. |
| P4 | Source images wildly unoptimised — gallery PNGs at 350–450 KB that should be ~30 KB WebP | `gallery 6.jpg` is the *same 617 KB hero file* reused as a thumbnail. |
| P5 | 16 YouTube iframes on Recent Work | ~1 MB+ of third-party JS and dozens of requests before any interaction. Needs a click-to-load facade. |
| P6 | Builder JS bundle + webfonts on every page | Nothing on this site requires a framework. |

**Rough estimate:** the homepage is shipping several megabytes to deliver what should be a sub-400 KB, sub-1.5s LCP page. On a mobile connection in rural Kent, that is lost bookings.

---

## 4. Strategy

### Positioning

> **The only detailer in Kent who does one car a day.**

Everything else — female-owned, award-winning, 29 five-star reviews, premium products — supports that single claim. It explains the price, justifies the wait, and makes every competitor's "3 cars a day" model look like the compromise it is.

### Target customers

1. **The proud owner** — new/prestige car, wants it kept immaculate. Buys Premium and ceramic. Highest value.
2. **The seller** — needs the car to photograph and present well before sale. Buys Interior+Exterior, sometimes 2-step polish. Fast decision, price-sensitive to ROI framing.
3. **The reclaimer** — family car, dogs, kids, spilled everything. Buys Premium Interior + ozone. Emotionally motivated by the before/after.
4. **The maintainer** — already had a detail, wants it kept up. £70/month. Highest lifetime value, currently marketed as an afterthought.

### The conversion job

Get from *"my car is a state"* to *"I've booked Ash"* in as few steps and as little doubt as possible:

**See the transformation → believe she's meticulous → understand which package I need → know it's affordable → know when she can come → book.**

The current site fails at steps 3, 4 and 5.

### Priorities, ranked by impact

1. **Fix the price contradiction** and publish one canonical price list.
2. **Three-tier package comparison** with a recommended middle tier, on both home and services.
3. **Sticky call/book bar and header phone number** — mobile-first.
4. **Rebuild the hero** — one clear promise, one CTA, trust signals visible without scrolling.
5. **Turn the gallery into real before/after sliders** with vehicle names and a CTA out.
6. **Show availability** — "next slot: [date]" — to convert the one-a-day constraint into urgency.
7. **Restructure the booking flow** — confirm the slot, then take a 20% deposit. Not full payment into the void.
8. **Location pages** for all nine service areas.
9. **Full schema stack** — AutoDetailing + Service + FAQPage + AggregateRating + VideoObject + BreadcrumbList.
10. **Rewrite every word** in a consistent, confident brand voice.
11. **Rebuild on a static stack** — target sub-1.5s LCP, 100 Lighthouse SEO/Best Practices.
