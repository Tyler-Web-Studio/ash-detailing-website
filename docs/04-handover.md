# Handover

**Built:** 31 July 2026 · 27 pages · zero runtime dependencies

## 0. What changed in the v2 design pass

| Area | Change |
|---|---|
| **Typography** | Archivo variable (100–900), self-hosted, latin subset, 34 KB, preloaded. Replaces the system stack. Display now runs at weight 850 with −0.05em tracking. |
| **Before/after sliders** | New component. Draggable anywhere on the image, keyboard accessible via a range input, and it self-demonstrates by easing off-centre when scrolled into view. Uses `clip-path` so both halves stay pixel-aligned. |
| **Navigation** | Services is now a mega-menu with thumbnails, one-liners and prices for all 8 services, plus a "not sure?" panel. Mobile is a full-screen overlay with staggered entry and item counts. Header hides on scroll down, returns on scroll up. |
| **Hero** | Rebuilt on the new Ford Focus RS photography. Slow drift, dual-axis scrim, gradient-filled display type, scroll cue. |
| **Process section** | New: six numbered stages with outlined numerals — the argument for why a detail takes hours. |
| **Motion** | View Transitions between pages, animated stat counters, staggered reveals, film-grain overlay, custom scrollbar and selection colour. All behind `prefers-reduced-motion`. |
| **Number plate redaction** | New build step. Declared regions in `src/data/redactions.json` are blurred before any derivative is generated; source files are untouched. Currently used on the Focus RS front shot. |

**Photography:** the 20 new `ba/*` files are 1536×2048 — about four times the resolution of the original `gallery/*` set. The build never upscales, so the older shots remain capped at their source size.

## 0b. Round three — client feedback applied

| Change | Detail |
|---|---|
| **Per-area pages removed** | The nine `/areas/<town>/` pages are gone. Site is now **18 pages**, not 27. The genuinely useful content (coverage list, what's needed on the day, "not on the list?") moved onto the single `/areas/` page; the rest was filler or already covered in the FAQs. Footer and homepage now link to the hub. |
| **Every duration removed** | No "3–12 hours", no "two days", no per-service timings. The FAQ that asked *"How long will it take?"* is now *"How does booking a day work?"* and answers without a number. Verified: **zero duration mentions across all 18 pages.** |
| **Google Business Profile linked** | Resolved from the CID in the share link to `google.com/maps?cid=5785657429822778322`. It's now in the `sameAs` schema, plus a designed Google panel on the reviews page and homepage with rating, count, "Read all on Google" and "Leave a review". |
| **H1 now carries the business name and keyword** | The display line is still "One car a day." but the `<h1>` also contains *"Mobile car detailing in Canterbury & Kent"*, and the eyebrow above it is the business name. Keeps the hook, fixes the SEO gap. |
| **Before/after sliders normalised** | All four pairs now share one 4:5 aspect ratio, so they no longer look ragged side by side. Grid is 2-up. |
| **Mobile hero rebuilt** | The scrim is now direction-aware — vertical on mobile (copy spans full width) and horizontal on desktop (copy sits left). The top third of the photo stays clear on mobile. |
| **Cache-busting added** | `main.css` and `main.js` now carry a content hash (`?v=…`), so a deploy can never serve a stale stylesheet. |

## 0c. Round four

| Change | Detail |
|---|---|
| **YouTube videos fixed** | They were broken because the `<iframe>` was being injected **inside** a `<button>` — interactive content nested in a button is invalid HTML and the player misbehaves. The iframe now *replaces* the button. Verified: 0 nested iframes, 0 iframes before click, 1 after. |
| **Price tables stack on mobile** | Every table below 620px becomes a stacked card (option name, then labelled Extra / Total rows) via `data-label` attributes. **All 13 pages now measure zero horizontal overflow at 375px.** |
| **Burger pinned top-right** | `.nav` is hidden on mobile, so nothing was pushing `.hdr__actions` across. Added `margin-left:auto`. Now sits 20px from the right edge on every device. |
| **Logo in the hero** | Added as a 74px brand mark above the headline, so the logo appears on the homepage as well as the header. |
| **Reviews moved up** | Now the first section after the hero — leaning into the 29 × 5★ as the main trust play, ahead of the before/afters. |
| **Reviews scale without cost** | The page renders the first 6 and holds the rest behind a "show the others" button. Adding 26 more costs nothing in load time. |

## 0d. Round five — reviews and the mobile hero

| Change | Detail |
|---|---|
| **28 real Google reviews added** | Transcribed from Ash's public profile. The 29th (Christian R.) left a star rating with no written text, so there is nothing to quote — hence 28 quoted against an aggregate of 29. That gap is correct, not an error. |
| **Names minimised** | Stored as first name + surname initial ("Helen G."). The reviewers published under full names, so republishing them would be lawful — but there's no need for this site to repeat them, and the shorter form reads better. |
| **Two reviews trimmed for special-category data** | One reviewer disclosed a health condition, another identified a wheelchair-accessible vehicle. Both are special-category personal data under UK GDPR and have no business being republished on a supplier's marketing site. The praise is quoted; the sensitive detail is not. No wording was altered — they're quoted as excerpts to a natural sentence break, the same as the reviews Google itself truncated behind "More". |
| **Mobile hero is now the logo** | The wide crop of the Focus RS works on desktop but reads badly in a tall phone frame. Mobile now gets a brand-led hero: the logo large and centred on a dark gradient with a blue bloom. Desktop keeps the car. |
| **The photo isn't downloaded on mobile at all** | The `<picture>` serves the car only above 760px; below that the `<img>` fallback is a 43-byte transparent GIF. Phones never fetch the hero photograph. |
| **Review schema now matches visible content** | Homepage renders 6 reviews and marks up 6; the reviews page renders 28 and marks up 28. Marking up 28 while showing 6 is a mismatch Google penalises. |

## 0e. Round six — accessibility, SEO and quality pass

| Fix | Detail |
|---|---|
| **Burger icon off-centre** | When the burger became a `<label>` (for the JS-free menu) it became a block box, so the first bar's margin collapsed out of it and pushed the icon upward. Now a flex container with `gap`, 48×48. Measured: bars centred to within 0.01px, and vertically aligned to the other header buttons to 0px. |
| **Colour contrast — `--faint`** | `#737A84` failed WCAG AA on cards, tables and notes (3.99:1 against `#161B22`). Raised to `#858C96`, which passes on every surface it's used on (4.61–5.91:1). |
| **Colour contrast — primary button** | The bottom of the button gradient (`#0B78CE`) gave 4.14:1 against the ink label. Lifted to `#1481D7` — now 4.64:1 at the darkest point, 10.88:1 at the lightest. |
| **Heading order** | Three pages skipped h1 → h3 (services, book, contact). Callout headings promoted to h2, and the services hub gained a proper section heading. Zero skips across all 18 pages. |
| **Tap targets** | Header controls now min 44px; footer, breadcrumb and inline banner links padded to ~44px. Inline links inside sentences deliberately left alone — padding those breaks line spacing, and Lighthouse excludes them. |
| **Titles too long for search results** | Every title exceeded 60 characters (worst: 103). The brand suffix alone was 33. Shortened to "\| Ash's Detailing" throughout. Longest is now 62, all descriptions ≤145. |
| **Hero logo `sizes` wrong** | Declared `74px` but renders up to 236px on phones, so the browser picked too small a file. Now `(max-width:759px) 236px, 74px`. |

### 🔴 Regression found and fixed: the availability band had no styling at all
The `.slot` band ("Taking bookings now…") **lost every one of its styles** in the v2 stylesheet rewrite — no background, no border, and the status dot had zero width. It had been rendering as plain unstyled text since then and I hadn't caught it. Restored with the gradient, border, pulsing dot and a 48px tap target.

### ⚠️ Lighthouse SEO on the preview build
The `--preview` build sets `noindex`, so **Lighthouse will report "Page is blocked from indexing" and the SEO score will not reach 100.** That is intentional and correct for a preview. To measure a true SEO score, deploy `ashs-website.zip` (the production build) instead.

### ⚠️ Copy I wrote that Ash never said — now corrected
The **process section** (six stages) was written by me. Steps 1–5 are a reorganisation of Ash's own service checklists, so the specifics are hers. But step 6 originally read *"Walked round the car with you before I leave. If something isn't right, I fix it there and then."* — **that was a service guarantee I invented.** She has never claimed it and would have been held to it. It has been replaced with aftercare advice taken from her own FAQ. **Ash should still read the whole process section and confirm it reflects how she actually works.**

### Two bugs found and fixed during this pass
- **Reveal animations started at `opacity:0`** with no JS fallback — if JavaScript ever failed, content would be invisible. Now gated on a `.js` class set by an inline script, so a no-JS visitor sees everything.
- **`.gpanel__score span` was overriding `.stars { display:inline-flex }`** on specificity, stacking the five stars vertically. Fixed, with a guard so a generic `span` rule can't do it again.

---

## 1. Running it

```bash
python3 -m pip install pillow     # once
python3 build.py                  # build to dist/
python3 build.py --serve          # build, then serve on :8000
python3 build.py --clean          # wipe and rebuild from scratch (~6s)
```

`dist/` is the entire deployable site — flat HTML, CSS, JS and WebP. Drag it into Netlify or Cloudflare Pages, or FTP it to IONOS. No Node, no npm, no build server.

## 2. Where things live

```
build.py              generator + image pipeline
pages.py              every page's structure and copy
src/data/*.json       ← all content and prices live here
src/templates/        base.html + _header / _footer / _mobilebar
src/styles/main.css   the design system
src/scripts/main.js   5 KB of progressive enhancement
src/images/           source photography
dist/                 build output — deploy this
docs/                 discovery, pricing, design, this file
```

**To change a price**, edit `src/data/pricing.json` and rebuild. It is the only place prices exist — the homepage tiers, service pages, pricing page and booking dropdown all read from it. That is deliberate: the old site's £120-vs-£140 contradiction happened because the number lived in two places.

Same pattern for `services.json`, `areas.json`, `faqs.json`, `reviews.json`, `gallery.json`, `site.json`, `redirects.json`.

## 3. What changed, against the audit

All 36 findings from [01-discovery-and-audit.md](01-discovery-and-audit.md) are addressed except where noted below.

| Area | Then | Now |
|---|---|---|
| Homepage HTML | 350 KB | **8.7 KB gzipped** |
| Webfonts | Builder fonts on every page | **0 bytes** — system stack |
| JavaScript | Builder bundle | **1.9 KB gzipped**, vanilla, deferred |
| Hero image | 617 KB JPEG | **27 KB** WebP, art-directed crop |
| Lazy loading | 0 of 15 images | Every below-fold image |
| Title tag | No location | `Mobile Car Detailing Canterbury & Kent …` |
| Open Graph | None | Full OG + Twitter card, 1200×630 image |
| Schema | Thin `LocalBusiness`, `sameAs` = 7 empty strings | `AutoDetailing` + `Service` + `FAQPage` + `AggregateRating` + `Review` + `VideoObject` + `BreadcrumbList` |
| Location pages | 0 | **9**, each with unique local content |
| Header phone | Footer only | Every page + sticky mobile call bar |
| Hero CTA | None | Two, above the fold, plus trust row |
| Pricing | Two contradictory lists | One canonical list, single source |
| Booking order | Pay in full → then find a date | Enquire → date confirmed → 20% deposit |
| Contact form | Free-text "contact details" box | Typed, validated, structured fields |
| YouTube | 16 eager iframes | Click-to-load facades |
| Old URLs | — | 301 redirect map in `_redirects` + `.htaccess` |

Verified: 27 pages, **0 broken internal links**, **0 missing assets**, **valid JSON-LD on every page**, exactly one `<h1>` per page, no console errors.

## 4. Resolved with Ash — 31 July 2026

| Item | Outcome |
|---|---|
| **Opening hours** | Detailing runs **8:00am–8:00pm, seven days**. Phone and email answered any time. Schema, footer and contact page all updated. |
| **Premium Large Van £140** | Confirmed correct by Ash — genuinely the same price as a standard car Premium. Query removed from `pricing.json`. |
| **Award** | Legitimate. Left in as-is; no awarding body named. |
| **Video titles** | Ash had written captions beneath each video on the live Recent Work page. All 16 recovered and paired to the correct video ID by document order, spelling tidied (*Hyandai* → Hyundai, *Cheroke* → Cherokee). They now appear as visible captions **and** as `VideoObject` schema names. |
| **Logo** | Ash's own logo (`ash logo.jpg`) is now the header mark and the source for the favicon, apple-touch-icon and 512px icon. My placeholder SVG is gone. |

## 5. Still open

| # | Item | Why it matters | Where to fix |
|---|---|---|---|
| 1 | **Booking form endpoint** ⏰ *Tyler asked to be reminded* | Currently FormSubmit, which needs a one-time activation email before it will deliver anything. **The form will silently fail until this is done — test it before launch.** Swappable for Formspree / Web3Forms / Netlify Forms in one line. | `site.json` → `formEndpoint` |
| 2 | **The other 26 review texts** | Google's consent wall blocks automated extraction, so I could not pull the review bodies — and I will not invent them, because the `AggregateRating` schema depends on every one being real. Only the 3 already published are on the site. Paste any others in and they render automatically. | `reviews.json` → `items` |
| 3 | **"Next available slot"** | The banner says "taking bookings now". One car a day is the best urgency lever on the site, but only with a real date. Worth Ash updating weekly. | `pages.py` → `home()` slot band |

## 6. Free wins Ash should do herself

Not code — but higher return than most code changes.

1. **Retitle the 16 YouTube videos.** They're captioned properly on the website now, but on YouTube itself every one is still called *"1 March 2026"* — so they're invisible to YouTube search. The titles in `gallery.json` can be copied straight across.
2. **Send the original camera files.** Every image supplied is a low-resolution web copy — most are 384×512, and only three exceed 1000px. The build never upscales, so the gallery is running at the ceiling of what the sources allow. Originals would visibly improve the whole site, particularly the hero.
3. **A simplified logo mark would help.** The full badge is a detailed illustration; below about 64px the "VEHICLE VALET AND DETAILING LTD" banner is unreadable. I crop the icon to the script and car so it survives 32px, but a purpose-made simple mark would be sharper in a browser tab. The full logo is used at 52px in the header, where it reads fine alongside the wordmark.
4. **Caption the gallery photos properly.** I've written deliberately conservative captions ("Prestige SUV interior") wherever the vehicle couldn't be identified with certainty, because misnaming a car on a detailer's site is worse than saying nothing. Real vehicle names and packages would improve both the page and its alt text. → `gallery.json`
5. **Publish more of the 29 reviews.** Only 3 are on the site. `reviews.json` takes more — but **real ones only**: the `AggregateRating` schema depends on them being genuine.
6. **Claim and fill out the Google Business Profile**, and ask every customer for a review. Review velocity drives the local map pack more than anything on the website.

## 7. Previewing it locally

The site uses absolute paths (`/main.css`, `/services/`) because that's what it needs on a real domain. That means **opening `dist/index.html` straight from Finder won't work** — the CSS and links resolve against your hard drive rather than the site root. It needs to be served.

**Double-click `Preview site.command`** in the project folder. It rebuilds, starts a local server and opens your normal browser at `http://localhost:8765`. Leave the Terminal window open while you browse; close it or press Ctrl-C when you're done.

Or from a terminal:

```bash
cd "/Users/tyler/Desktop/ashs website" && python3 build.py --serve
```

## 8. Deploying — GitHub → Netlify

`dist/` is committed to the repo on purpose, so Netlify has nothing to build and no deploy can fail on a dependency.

```bash
cd "/Users/tyler/Desktop/ashs website"
git init && git add -A && git commit -m "Ash's Vehicle Valet & Detailing — site rebuild"
git branch -M main
git remote add origin git@github.com:YOUR-USERNAME/ashs-website.git
git push -u origin main
```

Then in Netlify: **Add new site → Import an existing project → GitHub → pick the repo → Deploy.** `netlify.toml` already sets the publish directory to `dist`, so the defaults are correct.

`dist/_redirects` is picked up automatically, so the old IONOS URLs 301 rather than 404.

**Then, in order:**
1. Netlify → Domain management → add `ashsautodetailingltd.co.uk` and `www.`
2. Point the domain's nameservers (or a CNAME for `www`) at Netlify — this is the step that takes the site live, so do it once you're happy with everything else
3. Turn off the IONOS MyWebsite NOW site, or it will keep answering on the domain
4. Submit `https://www.ashsautodetailingltd.co.uk/sitemap.xml` in Google Search Console
5. Spot-check that `/our-services-and-prices/` and `/book-now/` actually 301
6. **Test the booking form end to end** — see §5.1

To update anything later: edit the JSON in `src/data/`, run `python3 build.py`, commit and push. Netlify redeploys on push.

### If you'd rather stay on IONOS
Upload the contents of `dist/` to the web root. `.htaccess` carries the 301s and forces HTTPS. The MyWebsite NOW site has to be switched off first, since it owns the domain root.

## 9. Known behaviour, not bugs

- **`tel:` links do nothing on a desktop browser** unless something is registered to handle calls (FaceTime, Skype, Teams). They work correctly on phones, which is where the overwhelming majority of "call now" taps come from for a local trade service. The `mailto:` and WhatsApp links behave the same way.
- **The `<video>`-style YouTube thumbnails are click-to-load.** Nothing from YouTube is requested until someone presses play — that's deliberate, for speed and privacy.

## 7. Deliberate decisions worth knowing

- **System fonts, not a webfont.** Costs zero bytes and zero layout shift. The typographic character comes from the scale, weight and tight tracking rather than a downloaded typeface.
- **No framework.** Nothing on this site needs one. The whole JS payload is 1.9 KB gzipped and every page works with JavaScript disabled.
- **Enquiry-first booking.** The old flow took full payment before a date existed. The new one confirms the date, then takes 20%. That change alone is likely the largest conversion gain here.
- **Location pages have real, differentiated content** — salt air in Whitstable, end-of-lease handbacks in Ashford, tight-parking damage in Medway. Nine near-identical pages with the town name swapped is a doorway-page pattern and gets penalised rather than ranked.
- **Gold is used only for stars and the award.** Everything else is the ice-blue accent. Restraint is what keeps it feeling premium.
