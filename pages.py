#!/usr/bin/env python3
"""Page definitions and copy. Imported by build.py."""

import build as b
from build import (
    SITE, PRICING, SERVICES, AREAS, FAQS, REVIEWS, GALLERY, BEFOREAFTER, SERVICE_BY_SLUG,
    e, money, markdown_lite, picture, hero_picture, before_after, price_table, cta_band, faq_list,
    configurator, booking_options, options_map, phead_bg,
    service_card, stars, crumbs_html, write_page,
    business_schema, breadcrumbs, faq_schema, review_schema, video_schema,
    service_schema,
)

PHONE = SITE["phone"]
PHONE_D = SITE["phoneDisplay"]
BRAND = SITE["name"].replace(" Ltd", "")  # apostrophes are awkward inside f-strings

ICONS = {
    "star": '<svg viewBox="0 0 20 19" class="g"><path d="M10 0l2.6 6.3 6.8.5-5.2 4.4 1.6 6.6L10 14.3 4.2 17.8l1.6-6.6L.6 6.8l6.8-.5z"/></svg>',
    "award": '<svg viewBox="0 0 24 24"><path d="M12 2a6 6 0 1 0 0 12A6 6 0 0 0 12 2zm0 10a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM7.6 15 5 22l4.4-1.6L12 22l2.6-1.6L19 22l-2.6-7a8 8 0 0 1-8.8 0z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5zm-1 14-4-4 1.4-1.4L11 13.2l4.6-4.6L17 10z"/></svg>',
    "van": '<svg viewBox="0 0 24 24"><path d="M3 6h11v3h3.4l3.6 4v5h-2a3 3 0 0 1-6 0H9a3 3 0 0 1-6 0H2V7a1 1 0 0 1 1-1zm13 5v2h3.3L17.6 11zM6 19.5A1.5 1.5 0 1 0 6 16a1.5 1.5 0 0 0 0 3.5zm10 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/></svg>',
}


GOOGLE_G = ('<svg class="gpanel__g" viewBox="0 0 48 48" aria-hidden="true">'
  '<path fill="#4285F4" d="M45.1 24.5c0-1.6-.1-2.8-.4-4H24v7.3h12.1c-.2 2-1.6 5-4.5 7l-.04.3 6.5 5 .5.05c4.1-3.8 6.5-9.4 6.5-15.7z"/>'
  '<path fill="#34A853" d="M24 46c5.9 0 10.8-1.9 14.4-5.3l-6.9-5.3c-1.8 1.3-4.3 2.2-7.5 2.2-5.8 0-10.7-3.8-12.4-9l-.3.02-6.8 5.2-.1.3C8 41.6 15.4 46 24 46z"/>'
  '<path fill="#FBBC05" d="M11.6 28.6c-.5-1.4-.7-2.9-.7-4.6s.3-3.2.7-4.6l-.01-.3-6.9-5.3-.2.1A22 22 0 0 0 2 24c0 3.5.9 6.9 2.5 9.9z"/>'
  '<path fill="#EB4335" d="M24 10.4c4.1 0 6.9 1.8 8.5 3.3l6.2-6C34.8 4.1 29.9 2 24 2 15.4 2 8 6.4 4.4 14.1l7.2 5.3c1.7-5.2 6.6-9 12.4-9z"/></svg>')


def google_panel(compact: bool = False) -> str:
    agg = REVIEWS["aggregate"]
    url = SITE["googleProfile"]
    return f"""<div class="gpanel{' gpanel--compact' if compact else ''}">
  <div class="gpanel__head">
    {GOOGLE_G}
    <div>
      <b>Google reviews</b>
      <span>{e(SITE['name'])}</span>
    </div>
  </div>
  <div class="gpanel__score">
    <b>{e(agg['rating'])}</b>
    <div>{stars()}<span>{agg['count']} reviews &middot; every one five stars</span></div>
  </div>
  <div class="gpanel__actions">
    <a class="btn btn--primary" href="{url}" rel="noopener nofollow" target="_blank">Read all on Google</a>
    <a class="btn btn--ghost" href="{url}" rel="noopener nofollow" target="_blank">Leave a review</a>
  </div>
</div>"""


def trust_row() -> str:
    items = [
        ("star", f'<strong>5.0</strong> from {SITE["reviewCount"]} reviews'),
        ("award", "<strong>Award-winning</strong> in South England"),
        ("shield", "<strong>Fully insured</strong>"),
        ("van", "<strong>Mobile</strong> &mdash; I come to you"),
    ]
    return '<div class="trust">' + "".join(
        f'<span class="trust__i">{ICONS[k]}<span>{v}</span></span>' for k, v in items
    ) + "</div>"


# --------------------------------------------------------------------------
# home
# --------------------------------------------------------------------------

def home():
    svc = SERVICE_BY_SLUG

    tiers = []
    for slug, desc, bullets in [
        ("exterior-detail", "A safe, thorough hand wash and protection.",
         ["Citrus pre-wash and snow foam", "Wheels, arches and tyres detailed",
          "Hand polish and ceramic spray wax", "Glass and exterior plastics restored"]),
        ("interior-exterior-detail", "The whole car, inside and out, in one visit.",
         ["Everything in both details", "Full extraction, steam and sanitisation",
          "Decontamination wash and protection", "Add a 2-step polish for £350"]),
        ("ceramic-coating", "Years of protection over corrected paint.",
         ["Full exterior detail included", "2-step machine polish first",
          "1, 2 or 5-year coatings", "Aftercare guidance included"]),
    ]:
        s = svc[slug]
        pop = slug == "interior-exterior-detail"
        tiers.append(f"""<div class="tier{' tier--pop' if pop else ''}">
  {'<span class="tier__flag">Most booked</span>' if pop else ''}
  <h3>{e(s['name'])}</h3>
  <p class="tier__desc">{e(desc)}</p>
  <p class="tier__price"><b>{money(s['from'])}</b><span>from</span></p>
  <ul>{''.join(f'<li>{e(x)}</li>' for x in bullets)}</ul>
  <a class="btn {'btn--primary' if pop else 'btn--ghost'}" href="/services/{slug}/">See what's included</a>
</div>""")

    gal = GALLERY["items"][:8]
    strip = "".join(
        f'<button class="gal__i" type="button" data-cap="{e(g["caption"])}">'
        f'{picture(g["src"], g["alt"], "(min-width:1100px) 24vw, (min-width:700px) 32vw, 48vw")}'
        f'<span class="gal__cap">{e(g["caption"])}</span></button>'
        for g in gal
    )

    revs = "".join(
        f"""<figure class="rev rv">
  {stars(r['rating'])}
  <blockquote>&ldquo;{e(r['text'])}&rdquo;</blockquote>
  <figcaption class="rev__who">
    <span class="rev__av" aria-hidden="true">{e(r['name'][0])}</span>
    <strong>{e(r['name'])}</strong><span class="rev__src">{e(r['source'])}</span>
  </figcaption>
</figure>"""
        for r in REVIEWS["items"][:6]   # homepage shows a curated six; the rest live on /reviews/
    )

    areas = "".join(
        f'<a class="area" href="/areas/"><b>{e(a["name"])}</b>'
        f'<span>{e(a["postcodes"].split(" · ")[0])}</span></a>'
        for a in AREAS
    )

    featured = [f for f in FAQS if f.get("featured")]

    ba = "".join(f'<div class="rv">{before_after(x)}</div>' for x in BEFOREAFTER["pairs"][:2])

    steps = [
        ("Decontaminate", "Citrus pre-wash, snow foam and a full chemical decontamination &mdash; iron fallout and tar dissolved off the paint rather than rubbed off it. Nothing gets touched until the grit is gone &mdash; that's what causes swirl marks."),
        ("Wash safely", "Two buckets, fresh microfibre mitts, non-acidic wheel cleaner. Every panel by hand."),
        ("Correct", "Machine polish where the paint needs it. 70&ndash;80% of swirls and light scratches, cut out properly."),
        ("Deep clean inside", "Extraction, steam and sanitisation. Vents, seams, stitch lines, panel gaps &mdash; fine-pick detailing throughout."),
        ("Protect", "Ceramic sealant, wax or a multi-year coating. Glass treated, trims conditioned, tyres dressed."),
        ("Aftercare", "Advice on keeping it that way &mdash; and why an automated wash undoes the work fastest. A two-bucket hand wash and a plush drying towel is all it takes."),
    ]
    process = "".join(
        f'<div class="pstep rv"><span class="pstep__n" aria-hidden="true">{i+1:02d}</span>'
        f'<b>Step {i+1}</b><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(steps)
    )

    body = f"""
<section class="hero">
  <div class="hero__bg">{hero_picture(SITE['heroImage'], SITE['heroAlt'])}</div>
  <div class="wrap hero__inner">
    {picture(SITE['logo'], BRAND + ' logo', '(max-width:759px) 236px, 74px', cls='hero__logo', priority=True)}
    <p class="eyebrow">Ash&rsquo;s Vehicle Valet &amp; Detailing</p>
    <h1 class="display">One car<em>a day.</em>
      <span class="display__sub">Mobile car detailing in Canterbury &amp; Kent</span></h1>
    <p class="hero__sub">Yours is the only vehicle I touch that day. No clock-watching, no second car waiting on the drive &mdash; just your car, done properly.</p>
    <div class="hero__actions">
      <a class="btn btn--primary btn--lg" href="/book/">Book your detail</a>
      <a class="btn btn--ghost btn--lg" href="#work">See the difference</a>
    </div>
    {trust_row()}
  </div>
  <div class="scrollcue" aria-hidden="true"><i></i><span>Scroll</span></div>
</section>

<section class="slot">
  <div class="wrap slot__inner">
    <span class="slot__dot" aria-hidden="true"></span>
    <p><strong>Taking bookings now.</strong> One vehicle a day means slots are limited &mdash; message me and I'll tell you honestly what's free.</p>
    <a href="/book/">Check availability &rarr;</a>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">Reviews</p>
      <h2>29 reviews. Every one five stars.</h2>
      <p class="lead">Not an average of five &mdash; every single review since the business opened. All public on Google, where they can&rsquo;t be edited.</p>
    </div>
    <div class="revwrap">
      {google_panel(compact=True)}
      <div class="grid grid--2">{revs}</div>
    </div>
    <p class="center" style="margin-top:2.5rem">
      <a class="btn btn--ghost btn--lg" href="/reviews/">Read all {SITE['reviewCount']} reviews</a>
    </p>
  </div>
</section>

<section class="sec" id="work">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">Before &amp; after</p>
      <h2>Drag the handle. That&rsquo;s the same car.</h2>
      <p class="lead">Not a filter, not a different vehicle. Real customer cars in Kent, photographed the day I finished them.</p>
    </div>
    <div class="ba-grid">{ba}</div>
    <p class="center" style="margin-top:3rem">
      <a class="btn btn--ghost btn--lg" href="/gallery/">See every transformation</a>
    </p>
  </div>
</section>

<section class="sec sec--deep">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">Recent work</p>
      <h2>The results speak first.</h2>
      <p class="lead">No stock photography, no borrowed portfolios.</p>
    </div>
    <div class="gal">{strip}</div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">Packages</p>
      <h2>Three ways to start.</h2>
      <p class="lead">Every package comes in Basic or Premium. Not sure which? Send photos and I'll tell you what your car actually needs &mdash; including when the cheaper one is the right call.</p>
    </div>
    <div class="tiers">{''.join(tiers)}</div>
    <p class="center" style="margin-top:2.5rem"><a class="btn btn--ghost" href="/pricing/">See every price, including surcharges</a></p>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="split__media rv">{picture('home/what-service-do-i-offer-current-image.jpg', 'Black Mercedes covered in snow foam during the pre-wash stage of an exterior detail', '(min-width:840px) 46vw, 90vw')}</div>
    <div class="rv">
      <p class="eyebrow">Why one a day</p>
      <h2>Most detailers book three cars a day. I book one.</h2>
      <div class="stack" style="margin-top:1.5rem">
        <p>Plenty of places advertise a full detail in ninety minutes. I genuinely can't see how that works &mdash; cleaning a boot properly can take an hour on its own.</p>
        <p>So I only take one vehicle a day. That means no clock-watching, no cutting the polish short because there's another car waiting on the drive, and no dragging yesterday's grit across your paint with a tired wash mitt.</p>
        <p>It also means I have to charge more than the hand wash down the road. That's the trade, and I'd rather be upfront about it than pretend otherwise.</p>
      </div>
      <ul class="ticks" style="margin-top:1.75rem">
        <li>Fresh microfibres and regularly replaced mitts on every car</li>
        <li>Non-acidic wheel cleaner &mdash; safe on every finish</li>
        <li>Premium products, whether it's a Kia Rio or a Bugatti</li>
        <li>Honest advice when a cheaper option is the right one</li>
      </ul>
      <p style="margin-top:1.75rem"><a class="btn btn--primary" href="/about/">More about how I work</a></p>
    </div>
  </div>
</section>

<section class="sec sec--raise">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b class="gold" data-count="5.0">5.0</b><span>from {SITE['reviewCount']} reviews</span></div>
      <div class="stat"><b class="acc" data-count="1">1</b><span>car per day</span></div>
      <div class="stat"><b data-count="100" data-suffix="%">100%</b><span>five-star reviews</span></div>
      <div class="stat"><b data-count="9">9</b><span>areas covered</span></div>
    </div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">The process</p>
      <h2>Six stages. Every single car.</h2>
      <p class="lead">Every stage, every car. This is what separates a detail from a wash.</p>
    </div>
    <div class="process">{process}</div>
  </div>
</section>


<section class="sec sec--alt">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">Areas covered</p>
      <h2>I come to you, across Kent.</h2>
      <p class="lead">Based in Hersden just outside Canterbury, travelling from Whitstable to Tunbridge Wells and out to the London outskirts.</p>
    </div>
    <div class="areas">{areas}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">Before you book</p>
      <h2>The questions I get asked most.</h2>
    </div>
    <div style="max-width:820px;margin-inline:auto">{faq_list(featured, open_first=True)}</div>
    <p class="center" style="margin-top:2rem"><a class="btn btn--ghost" href="/faq/">All questions answered</a></p>
  </div>
</section>

{cta_band("Ready to book your day?", "Tell me about your car and when suits. I'll confirm a date, then a 20% deposit secures it.")}
"""

    write_page(
        "",
        title="Mobile Car Detailing Canterbury & Kent | Ash's Detailing",
        description=(
            "Award-winning mobile car detailing in Canterbury and Kent. One car a day, "
            "29 five-star reviews. Interior, exterior and ceramic coating from £100."
        ),
        body=body,
        schemas=[business_schema(), faq_schema(featured), review_schema(limit=6)],
        nav_key="",
        priority="1.0",
    )


# --------------------------------------------------------------------------
# services
# --------------------------------------------------------------------------

def services_hub():
    cards = "".join(f'<div class="rv">{service_card(s)}</div>' for s in SERVICES)
    body = f"""
{crumbs_html([("Home", "/"), ("Services", "/services/")])}
<section class="phead phead--img">
  {phead_bg("ba/after-1-6.jpg", 0.5)}
  <div class="wrap">
    <p class="eyebrow">Services</p>
    <h1>Everything I offer, and exactly what's in it.</h1>
    <p class="lead">Eight services, from a straightforward exterior detail at £100 to a two-day full transformation. Every package comes in Basic or Premium &mdash; the difference is spelled out on each page rather than hidden in a dropdown.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head head--center">
      <h2>Choose your package</h2>
      <p class="lead">Every one is priced on this site, in full, with the surcharges listed.</p>
    </div>
    <div class="grid grid--3">{cards}</div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    <div class="head head--center">
      <h2>Not sure which one?</h2>
      <p class="lead">Send me a couple of photos of your car and tell me what's bothering you about it. I'll tell you which package fits &mdash; including when the cheaper one will do the job.</p>
    </div>
    <p class="center"><a class="btn btn--primary btn--lg" href="/contact/">Ask me</a></p>
  </div>
</section>

{cta_band("Know what you need?", "Book it in and I'll confirm your date.")}
"""
    write_page(
        "services",
        title="Car Detailing Services & Prices, Kent | Ash's Detailing",
        description=(
            "Interior, exterior and full detailing, machine polishing, ceramic coatings and SMART repair across Kent. Every package explained, from £100."
        ),
        body=body, schemas=[breadcrumbs([("Home", "/"), ("Services", "/services/")])],
        nav_key="services", priority="0.9",
    )


def service_page(svc):
    slug = svc["slug"]
    trail = [("Home", "/"), ("Services", "/services/"), (svc["name"], f"/services/{slug}/")]

    inc = ""
    if svc.get("includes"):
        inc = f"""<section class="sec">
  <div class="wrap split">
    <div class="rv">
      <p class="eyebrow">What's included</p>
      <h2>Every step, listed.</h2>
      <p class="lead" style="margin-top:1rem">{e(svc['forWho'])}</p>
    </div>
    <ul class="ticks rv">{''.join(f'<li>{e(x)}</li>' for x in svc['includes'])}</ul>
  </div>
</section>"""

    prem = ""
    if svc.get("premium"):
        prem = f"""<section class="sec sec--alt">
  <div class="wrap">
    <div class="head">
      <p class="eyebrow">Basic vs Premium</p>
      <h2>{e(svc['premiumTitle'])}</h2>
      <p class="lead">Premium isn't a bigger version of the same wash &mdash; it's a different level of work. This is exactly what the extra buys.</p>
    </div>
    <ul class="ticks ticks--2">{''.join(f'<li>{e(x)}</li>' for x in svc['premium'])}</ul>
    <p class="callout" style="margin-top:2rem"><strong>Best for:</strong> {e(svc.get('premiumFor', ''))}</p>
  </div>
</section>"""

    if svc.get("priceKey"):
        ptable = f"""<section class="sec">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Prices</p><h2>{e(svc['name'])} pricing</h2>
    <p class="lead">Vans, caravans and XL vehicles take longer, so they carry a surcharge. Everything is listed &mdash; nothing appears at checkout that isn't on this page.</p></div>
    {price_table(svc['priceKey'])}
    <p class="note">Not VAT registered, so the price quoted is the price you pay. Condition surcharges (heavy dirt, mould, pet hair) are assessed on arrival and agreed before any work starts.</p>
  </div>
</section>"""
    elif svc.get("priceNotes"):
        rows = "".join(
            f'<tr><th scope="row">{e(p["label"])}</th><td class="num total" data-label="Price">{e(p["price"])}</td></tr>'
            for p in svc["priceNotes"]
        )
        ptable = f"""<section class="sec">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Prices</p><h2>{e(svc['name'])} pricing</h2></div>
    <div class="table-wrap"><table class="prices">
      <thead><tr><th scope="col">Package</th><th scope="col" class="num">Price</th></tr></thead>
      <tbody>{rows}</tbody></table></div>
    {f'<p class="note">{e(svc["note"])}</p>' if svc.get('note') else ''}
  </div>
</section>"""
    elif svc.get("items"):
        cards = "".join(
            f"""<div class="tier rv"><h3>{e(i['name'])}</h3>
<p class="tier__price"><b>{e(i['price'])}</b></p>
<p class="tier__desc">{e(i['body'])}</p></div>"""
            for i in svc["items"]
        )
        ptable = f"""<section class="sec">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Prices</p><h2>What I can and can't do</h2>
    <p class="lead">SMART stands for Small, Medium And Repeatable Techniques. It fixes a lot &mdash; but not everything, and I'll say so.</p></div>
    <div class="tiers">{cards}</div>
  </div>
</section>"""
    else:
        ptable = f"""<section class="sec">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Price</p><h2>{money(svc['from'])}{e(svc.get('unit',''))}</h2>
    {f'<p class="lead">{e(svc["note"])}</p>' if svc.get('note') else ''}</div>
  </div>
</section>"""

    unit = svc.get("unit", "")
    body = f"""
{crumbs_html(trail)}
<section class="phead phead--spiral">
  {b.partial('spiral')}
  <div class="wrap split">
    <div>
      <p class="eyebrow">{e(svc['short'])}</p>
      <h1>{e(svc['name'])}</h1>
      <p class="lead">{e(svc['tagline'])}</p>
      {configurator(svc)}
      <p class="phead__alt"><a class="tlink" href="tel:{PHONE}">Prefer to talk it through? Call {PHONE_D}
        <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M11 4l6 6-6 6-1.4-1.4 3.6-3.6H3V9h10.2L9.6 5.4z"/></svg>
      </a></p>
    </div>
    <div class="split__media">{picture(svc['image'], svc['name'] + ' by ' + BRAND + ' in Kent', '(min-width:840px) 46vw, 90vw')}</div>
  </div>
</section>

<section class="sec sec--tight">
  <div class="wrap"><p class="lead measure">{e(svc['intro'])}</p></div>
</section>

{inc}
{prem}
{ptable}

{f'<section class="sec sec--alt"><div class="wrap"><p class="callout measure center"><strong>Worth knowing:</strong> {e(svc["upsell"])}</p></div></section>' if svc.get('upsell') else ''}

{cta_band(f"Book your {svc['name'].lower()}", "Tell me about your vehicle and when suits. I'll confirm the date before any deposit.")}
"""

    write_page(
        f"services/{slug}",
        title=f"{svc['titleName']} in Kent from {money(svc['from'])}{unit} | Ash's Detailing",
        description=svc["metaDescription"],
        body=body,
        schemas=[service_schema(svc), breadcrumbs(trail)],
        nav_key="services", priority="0.8",
    )


# --------------------------------------------------------------------------
# pricing
# --------------------------------------------------------------------------

def pricing_page():
    blocks = []
    for key, pkg in PRICING["packages"].items():
        blocks.append(f"""<div class="stack" style="margin-bottom:3rem">
  <h2 id="{key}">{e(pkg['name'])}</h2>
  {price_table(key)}
  <p><a href="/services/{key}/">What's included in a {pkg['name'].lower()} &rarr;</a></p>
</div>""")

    flag = "".join(
        f"""<tr><th scope="row"><a href="/services/{f['slug']}/">{e(f['name'])}</a><br>
<span class="note" style="margin:0">{e(f['note'])}</span></th>
<td class="num total" data-label="Price">{money(f['price'])}{e(f['unit'])}</td></tr>"""
        for f in PRICING["flagship"]
    )
    spec = "".join(
        f"""<tr><th scope="row">{e(s['name'])}<br><span class="note" style="margin:0">{e(s['note'])}</span></th>
<td class="num total" data-label="Price">{e(s['price'])}<br><span class="note" style="margin:0">{e(s['qualifier'])}</span></td></tr>"""
        for s in PRICING["specialist"]
    )
    add = "".join(
        f'<tr><th scope="row">{e(a["name"])}{f" <span class=note style=margin:0>{e(a["note"])}</span>" if a["note"] else ""}</th>'
        f'<td class="num total" data-label="Price">{money(a["price"])}</td></tr>'
        for a in PRICING["addons"]
    )
    sur = "".join(
        f'<tr><th scope="row">{e(s["name"])}</th><td class="num total" data-label="Range">{e(s["range"])}</td></tr>'
        for s in PRICING["surcharges"]
    )
    disc = "".join(
        f"""<div class="tier"><h3>{e(d['name'])}</h3>
<p class="tier__price"><b>{e(d['value'])}</b></p>
<p class="tier__desc">{e(d['detail'])}</p></div>"""
        for d in PRICING["discounts"]
    )

    body = f"""
{crumbs_html([("Home", "/"), ("Pricing", "/pricing/")])}
<section class="phead phead--img">
  {phead_bg("ba/after-4-2.jpg", 0.5)}
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h1>Every price, on one page.</h1>
    <p class="lead">No hidden extras appearing at checkout. Vans, caravans and XL vehicles take longer so they carry a surcharge &mdash; those are listed too. I'm not VAT registered, so the price you're quoted is the price you pay.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap" style="max-width:900px">{''.join(blocks)}</div>
</section>

<section class="sec sec--alt">
  <div class="wrap" style="max-width:900px">
    <h2>Flagship &amp; recurring</h2>
    <div class="table-wrap" style="margin-top:1.5rem"><table>
      <thead><tr><th scope="col">Service</th><th scope="col" class="num">Price</th></tr></thead>
      <tbody>{flag}</tbody></table></div>

    <h2 style="margin-top:3.5rem">Specialist work</h2>
    <p class="lead" style="margin-top:.75rem">Quoted per job. Send photos and I'll give you a real number rather than a range.</p>
    <div class="table-wrap" style="margin-top:1.5rem"><table>
      <thead><tr><th scope="col">Service</th><th scope="col" class="num">Price</th></tr></thead>
      <tbody>{spec}</tbody></table></div>

    <h2 style="margin-top:3.5rem">Add-ons</h2>
    <div class="table-wrap" style="margin-top:1.5rem"><table>
      <thead><tr><th scope="col">Add-on</th><th scope="col" class="num">Price</th></tr></thead>
      <tbody>{add}</tbody></table></div>

    <h2 style="margin-top:3.5rem">Condition surcharges</h2>
    <p class="lead" style="margin-top:.75rem">Assessed when I arrive and agreed with you <em>before</em> any work starts. Heavy soiling takes materially longer and uses far more product &mdash; these aren't a surprise at the end.</p>
    <div class="table-wrap" style="margin-top:1.5rem"><table>
      <thead><tr><th scope="col">Condition</th><th scope="col" class="num">Range</th></tr></thead>
      <tbody>{sur}</tbody></table></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">Discounts</p>
      <h2>Ways to pay less.</h2>
      <p class="lead">These stack &mdash; a blue light discount and a review credit can be used together.</p>
    </div>
    <div class="tiers">{disc}</div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap" style="max-width:820px">
    <h2>How payment works</h2>
    <ol class="steps" style="margin-top:2rem">
      <li><div><b>You enquire</b><p>Tell me the vehicle, what you're after and roughly when. Photos help.</p></div></li>
      <li><div><b>I confirm a date</b><p>One car a day, so I'll be straight about what's actually free. Nothing is paid at this point.</p></div></li>
      <li><div><b>20% deposit secures it</b><p>That covers the reserved day and the premium products bought in for your car.</p></div></li>
      <li><div><b>Balance on the day</b><p>Cash or bank transfer. Invoices available on request.</p></div></li>
    </ol>
  </div>
</section>

{cta_band("Found the one?", "Book it in and I'll confirm your date before any deposit.")}
"""
    write_page(
        "pricing",
        title="Car Detailing Prices in Kent from £100 | Ash's Detailing",
        description=(
            "Full price list for mobile car detailing in Kent. Interior £130, exterior £100, full detail £180, ceramic coating £340. No VAT, no hidden extras."
        ),
        body=body, schemas=[breadcrumbs([("Home", "/"), ("Pricing", "/pricing/")])],
        nav_key="pricing", priority="0.9",
    )


# --------------------------------------------------------------------------
# book
# --------------------------------------------------------------------------

def book_page():
    opts = []
    for s in SERVICES:
        opts.append(f'<option value="{e(s["name"])}" data-slug="{s["slug"]}">{e(s["name"])}</option>')

    areas = "".join(f'<option value="{e(a["name"])}">{e(a["name"])}</option>' for a in AREAS)

    import json as _json
    body = f"""
<script type="application/json" id="pkgdata">{_json.dumps(options_map(), ensure_ascii=False)}</script>
{crumbs_html([("Home", "/"), ("Book", "/book/")])}
<section class="phead phead--img">
  {phead_bg("ba/after-1-4.jpg", 0.5)}
  <div class="wrap">
    <p class="eyebrow">Book</p>
    <h1>Let's get your car in the diary.</h1>
    <p class="lead">Tell me about the vehicle and when suits you. I'll come back with a date I can actually commit to &mdash; then a 20% deposit secures it. You're not paying for anything until the date is agreed.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap split" style="align-items:start">
    <form class="form" id="bookform" method="post" action="{SITE['form']['successPath']}"
          name="{SITE['form']['name']}" data-netlify="true" data-netlify-honeypot="_honey">
      <input type="hidden" name="form-name" value="{SITE['form']['name']}">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">

      <fieldset class="fieldset">
        <legend>About you</legend>
        <div class="frow">
          <div class="field">
            <label for="name">Your name <span class="req">*</span></label>
            <input id="name" name="name" type="text" autocomplete="name" required>
            <span class="err">Please tell me your name.</span>
          </div>
          <div class="field">
            <label for="phone">Phone <span class="req">*</span></label>
            <input id="phone" name="phone" type="tel" autocomplete="tel" required>
            <span class="err">I need a number to confirm your date.</span>
          </div>
        </div>
        <div class="frow">
          <div class="field">
            <label for="email">Email <span class="req">*</span></label>
            <input id="email" name="email" type="email" autocomplete="email" required>
            <span class="err">Please enter a valid email address.</span>
          </div>
          <div class="field">
            <label for="postcode">Postcode <span class="req">*</span>
              <span class="hint">So I can check travel</span></label>
            <input id="postcode" name="postcode" type="text" autocomplete="postal-code" required>
            <span class="err">Please enter your postcode.</span>
          </div>
        </div>
        <div class="frow">
          <div class="field">
            <label for="area">Nearest town</label>
            <select id="area" name="area"><option value="">Choose&hellip;</option>{areas}<option value="Other">Somewhere else</option></select>
          </div>
        </div>
      </fieldset>

      <fieldset class="fieldset">
        <legend>The vehicle</legend>
        <div class="frow">
          <div class="field">
            <label for="vehicle">Make and model <span class="req">*</span></label>
            <input id="vehicle" name="vehicle" type="text" placeholder="e.g. Range Rover Evoque" required>
            <span class="err">Let me know what I'm working on.</span>
          </div>
          <div class="field">
            <label for="size">Vehicle size</label>
            <select id="size" name="size">
              <option>Standard car</option>
              <option>Large / 4x4 / estate</option>
              <option>XL (6+ seats)</option>
              <option>Van</option>
              <option>Caravan or motorhome</option>
            </select>
          </div>
        </div>
        <div class="frow">
          <div class="field">
            <label for="package">Service <span class="req">*</span></label>
            <select id="package" name="package" required>
              <option value="">Choose a service&hellip;</option>{''.join(opts)}
              <option value="Not sure" data-slug="">Not sure &mdash; please advise</option>
            </select>
            <span class="err">Pick one, or choose &ldquo;not sure&rdquo; and I'll advise.</span>
          </div>
          <div class="field" id="optionfield">
            <label for="option">Option <span class="req">*</span>
              <span class="hint">Premium is the most booked</span></label>
            <!-- Deliberately NOT required in the markup: the list is populated by main.js.
                 With JS blocked this select only ever holds the empty placeholder, so a
                 required attribute here would make the form permanently unsubmittable.
                 fillOptions() in main.js sets .required once there are real options. -->
            <select id="option" name="option">
              <option value="">I&rsquo;ll advise on the option</option>
            </select>
            <span class="err">Pick the option you'd like.</span>
          </div>
        </div>
        <div class="frow">
          <div class="field">
            <p class="quote" id="quotebox">
              <span class="quote__l">Your price</span>
              <b id="estimate">&mdash;</b>
              <span class="quote__n">Confirmed once I&rsquo;ve seen the car. Condition surcharges are always agreed before I start.</span>
            </p>
          </div>
        </div>
        <div class="frow">
          <div class="field">
            <label for="condition">Condition and anything I should know</label>
            <textarea id="condition" name="condition" placeholder="Pet hair, smoke smell, kerbed alloys, scratches, mould, how long since it was last detailed — the more you tell me, the more accurate my quote."></textarea>
          </div>
        </div>
      </fieldset>

      <fieldset class="fieldset">
        <legend>When</legend>
        <div class="frow">
          <div class="field">
            <label for="date1">Preferred date</label>
            <input id="date1" name="preferred_date" type="date">
          </div>
          <div class="field">
            <label for="date2">Alternative date</label>
            <input id="date2" name="alternative_date" type="date">
          </div>
        </div>
        <div class="frow">
          <div class="field">
            <label class="check">
              <input type="checkbox" name="access" value="yes" required>
              <span>I can provide a parking space by the vehicle with access to water and electricity (within 30m). <span class="req">*</span></span>
            </label>
          </div>
        </div>
        <div class="frow">
          <div class="field">
            <label class="check">
              <input type="checkbox" name="consent" value="yes" required>
              <span>I'm happy for these details to be stored so Ash can contact me about this enquiry. I can withdraw consent at any time. <span class="req">*</span></span>
            </label>
          </div>
        </div>
      </fieldset>

      <button class="btn btn--primary btn--lg" type="submit">Send enquiry</button>
      <p class="note">No payment is taken now. I'll reply with a date first.</p>
    </form>

    <aside class="stack">
      <div class="callout">
        <h2>What happens next</h2>
        <ol class="steps" style="margin-top:1.25rem">
          <li><div><b>I reply, usually same day</b><p>With a date I can actually commit to.</p></div></li>
          <li><div><b>You confirm</b><p>A 20% deposit secures the slot and the products.</p></div></li>
          <li><div><b>I arrive and get to work</b><p>Yours is the only car I touch that day.</p></div></li>
          <li><div><b>Balance on completion</b><p>Cash or bank transfer.</p></div></li>
        </ol>
      </div>

      <div class="callout">
        <h2>Prefer to talk it through?</h2>
        <p>If you're not sure what your car needs, a two-minute call usually sorts it faster than a form.</p>
        <p style="margin-top:1rem">
          <a class="btn btn--primary" href="tel:{PHONE}">Call {PHONE_D}</a>
          <a class="btn btn--ghost" href="https://wa.me/447907019798" rel="noopener" target="_blank">WhatsApp</a>
        </p>
      </div>

      <div class="callout">
        <h2>Before I arrive</h2>
        <ul class="ticks" style="margin-top:1rem">
          <li>A parking space next to the vehicle</li>
          <li>An outside tap and a plug point within 30m</li>
          <li>Personal belongings removed from the cabin and boot</li>
          <li>Let me know about pet hair or mould in advance</li>
        </ul>
      </div>
    </aside>
  </div>
</section>
"""
    write_page(
        "book",
        title="Book a Mobile Car Detail in Kent | Ash's Detailing",
        description=(
            "Book mobile car detailing in Canterbury and across Kent. I confirm your date first, then a 20% deposit secures it. No payment upfront."
        ),
        body=body, schemas=[breadcrumbs([("Home", "/"), ("Book", "/book/")])],
        nav_key="book", priority="0.9",
    )


# --------------------------------------------------------------------------
# gallery / reviews / about / faq / contact
# --------------------------------------------------------------------------

def gallery_page():
    ba_all = "".join(f'<div class="rv">{before_after(x, "(min-width:1000px) 46vw, 92vw")}</div>'
                     for x in BEFOREAFTER["pairs"])
    items = "".join(
        f'<button class="gal__i" type="button" data-cap="{e(g["caption"])}">'
        f'{picture(g["src"], g["alt"], "(min-width:1100px) 24vw, (min-width:700px) 32vw, 48vw")}'
        f'<span class="gal__cap">{e(g["caption"])}</span></button>'
        for g in GALLERY["items"]
    )
    vids = "".join(
        f"""<figure class="vcard">
  <button class="vid" type="button" data-yt="{e(v['id'])}" aria-label="Play video: {e(v['title'])}">
    <img src="https://i.ytimg.com/vi/{e(v['id'])}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy" decoding="async">
    <span class="vid__play"></span>
  </button>
  <figcaption>{e(v['title'])}</figcaption>
</figure>"""
        for v in GALLERY["videos"]
    )
    body = f"""
{crumbs_html([("Home", "/"), ("Gallery", "/gallery/")])}
<section class="phead phead--img">
  {phead_bg("ba/after-1-8.jpg", 0.55)}
  <div class="wrap">
    <p class="eyebrow">Recent work</p>
    <h1>Real cars. Real customers. Real results.</h1>
    <p class="lead">Every photograph here is a car I've detailed in Kent. Nothing borrowed, nothing stock. Tap any image to see it larger.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">Before &amp; after</p>
      <h2>Drag to reveal.</h2>
      <p class="lead">Same car, same angle. One before I started, one when I finished.</p>
    </div>
    <div class="ba-grid">{ba_all}</div>
  </div>
</section>

<section class="sec sec--deep">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">The work</p>
      <h2>Finished cars.</h2>
    </div>
    <div class="gal">{items}</div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">Video</p>
      <h2>Transformations, start to finish.</h2>
      <p class="lead">Videos load only when you press play &mdash; so the page stays fast for everyone else.</p>
    </div>
    <div class="vids">{vids}</div>
    <p class="center" style="margin-top:2.5rem">
      <a class="btn btn--ghost" href="{SITE['social']['tiktok']}" rel="noopener" target="_blank">More on TikTok</a>
      <a class="btn btn--ghost" href="{SITE['social']['youtube']}" rel="noopener" target="_blank">YouTube channel</a>
    </p>
  </div>
</section>

{cta_band("Want yours to look like this?", "One car a day means the diary fills up. Get your date booked in.")}
"""
    write_page(
        "gallery",
        title="Before & After Car Detailing, Kent | Ash's Detailing",
        description=(
            "Before and after photos and videos from real mobile detailing jobs across Canterbury, Maidstone, Medway and Kent. Drag to reveal the difference."
        ),
        body=body,
        schemas=[breadcrumbs([("Home", "/"), ("Gallery", "/gallery/")]), video_schema()],
        nav_key="gallery", priority="0.8",
    )


def reviews_page():
    items = REVIEWS["items"]
    VISIBLE = 6  # the rest render but stay hidden until asked for — no extra requests
    revs = "".join(
        f"""<figure class="rev rv{' rev--hidden' if i >= VISIBLE else ''}">{stars(r['rating'])}
  <blockquote>&ldquo;{e(r['text'])}&rdquo;</blockquote>
  <figcaption class="rev__who"><span class="rev__av" aria-hidden="true">{e(r['name'][0])}</span>
  <strong>{e(r['name'])}</strong><span class="rev__src">{e(r['source'])}</span></figcaption>
</figure>"""
        for i, r in enumerate(items)
    )
    more = ""
    if len(items) > VISIBLE:
        more = (f'<p class="center" style="margin-top:2.5rem">'
                f'<button class="btn btn--ghost btn--lg" type="button" id="morerevs">'
                f'Show the other {len(items) - VISIBLE} reviews</button></p>')
    url = SITE["googleProfile"]
    body = f"""
{crumbs_html([("Home", "/"), ("Reviews", "/reviews/")])}
<section class="phead phead--img">
  {phead_bg("ba/after-4-1.jpg", 0.45)}
  <div class="wrap">
    <p class="eyebrow">Reviews</p>
    <h1>{SITE['reviewCount']} reviews. Every single one five stars.</h1>
    <p class="lead">Not an average of five. Not "mostly" five. Every review left since the business opened has
    been a five &mdash; and they're all on the Google profile, unedited, where I can't touch them.</p>
  </div>
</section>

<section class="sec sec--tight">
  <div class="wrap" style="max-width:640px">{google_panel()}</div>
</section>

<section class="sec sec--deep">
  <div class="wrap">
    <div class="head head--center">
      <p class="eyebrow">In their words</p>
      <h2>A few of them.</h2>
      <p class="lead">Reproduced exactly as written.</p>
    </div>
    <div class="grid grid--3">{revs}</div>
    {more}
    <p class="center" style="margin-top:2rem">
      <a class="btn btn--ghost btn--lg" href="{url}" rel="noopener nofollow" target="_blank">Read all {SITE['reviewCount']} on Google</a>
    </p>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="stack measure">
      <p class="eyebrow">Why it matters</p>
      <h2>A perfect record is fragile. That&rsquo;s the point.</h2>
      <p>One rushed job would end it. That&rsquo;s exactly why I only take one car a day &mdash; the moment I
      start doubling up, something slips, and the record goes.</p>
      <p>It&rsquo;s also why I&rsquo;d rather talk you into the cheaper package than sell you something your car
      doesn&rsquo;t need. A five-star review is worth more to me than the extra sixty quid.</p>
    </div>
    <div class="split__media">{picture('ba/after-4-2.jpg', 'Cream leather Range Rover interior detailed to a showroom finish', '(min-width:840px) 46vw, 90vw')}</div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap" style="max-width:700px">
    <div class="head head--center">
      <h2>Had your car detailed?</h2>
      <p class="lead">Leaving a review gets you <strong>£10 off your next booking</strong> &mdash; and it genuinely
      helps a one-person business compete with the big names.</p>
    </div>
    <p class="center"><a class="btn btn--primary btn--lg" href="{url}" rel="noopener nofollow" target="_blank">Leave a review on Google</a></p>
  </div>
</section>

{cta_band("Join them.", "Book your detail and see what the fuss is about.")}
"""
    write_page(
        "reviews",
        title=f"{SITE['reviewCount']} Five-Star Reviews | Ash's Detailing, Kent",
        description=(
            f"{SITE['reviewCount']} five-star Google reviews for mobile car detailing across Kent. Not an average of five — every single review since the business opened."
        ),
        body=body,
        schemas=[breadcrumbs([("Home", "/"), ("Reviews", "/reviews/")]), review_schema()],
        nav_key="reviews", priority="0.8",
    )



def about_page():
    body = f"""
{crumbs_html([("Home", "/"), ("About", "/about/")])}
<section class="phead phead--img">
  {phead_bg("ba/after-1.jpg", 0.5)}
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>I'm Ash. I detail one car a day.</h1>
    <p class="lead">Ash's Vehicle Valet and Detailing Ltd is one person, one diary, and only ever one vehicle in it per day. I load the kit into my own car and drive to you. That's not a marketing line &mdash; it's the whole business model.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="split__media split__media--tall rv">{picture('home/why-my-service-is-different-currentimage.jpg', 'Cream leather Range Rover interior detailed to a showroom standard', '(min-width:840px) 44vw, 90vw')}</div>
    <div class="stack rv">
      <h2>How I got here</h2>
      <p>I opened the business in late December 2025. Before that I worked alongside a family member in a body shop &mdash; and I did that work for nothing, on my own cars and on friends' and family's vehicles, purely because I enjoyed it.</p>
      <p>So the company is young. The hands doing the work are not. There's a difference between someone who bought a pressure washer last month and someone who's spent years watching paint get corrected properly and learning why it goes wrong.</p>
      <h2 style="margin-top:2rem">Why one car a day</h2>
      <p>I could book three cars a day and rush all three &mdash; that's what the economics push you towards, and it's what a lot of the industry does.</p>
      <p>I'd rather do one, properly, and be able to stand behind it. That's the entire reason my prices are what they are, and the entire reason every review so far has been five stars.</p>
    </div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    <div class="head head--center">
      <h2>Being a woman in this trade</h2>
      <p class="lead">Detailing is overwhelmingly male, and I won't pretend that's never made things harder. But it turns out to be an advantage for the people who book me.</p>
    </div>
    <div class="grid grid--3">
      <div class="tier"><h3>Someone you're comfortable with</h3><p class="tier__desc">A detailer works at your home and inside your car. Plenty of my customers &mdash; women and older customers especially &mdash; tell me that mattered more than they expected.</p></div>
      <div class="tier"><h3>Straight answers</h3><p class="tier__desc">I'll tell you when the cheaper package is the right one, and when a scratch needs a body shop rather than me. I'd rather lose the upsell than the trust.</p></div>
      <div class="tier"><h3>Something to prove</h3><p class="tier__desc">The work has to speak louder here. Twenty-nine five-star reviews and an award for Best Detailing Service in South England in seven months is me making sure it does.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head head--center"><h2>What I won't do</h2>
    <p class="lead">Just as important as the list of what's included.</p></div>
    <div style="max-width:760px;margin-inline:auto">
      <ul class="ticks">
        <li><strong>I won't use brushes or a dirty mitt.</strong> Cheap car washes are the number one cause of swirl marks. Fresh microfibres, every car.</li>
        <li><strong>I won't chase 100% paint correction.</strong> Clear coat doesn't grow back. 70&ndash;80% is a dramatic change and a safe one; beyond that I'll tell you it isn't worth it.</li>
        <li><strong>I won't pretend to be a body shop.</strong> SMART repair fixes a lot. Deep damage needs a proper shop, and I'll say so.</li>
        <li><strong>I won't perfume over a smell.</strong> If it needs ozone to actually fix it, that's what I'll recommend.</li>
        <li><strong>I won't surprise you with a bill.</strong> Condition surcharges are assessed and agreed before work starts, never after.</li>
      </ul>
    </div>
  </div>
</section>

{cta_band("Let's talk about your car.", "Send photos and I'll tell you honestly what it needs.")}
"""
    write_page(
        "about",
        title="About Ash | Female-Owned Car Detailing in Kent",
        description=(
            "Meet Ashleigh Loosemore — award-winning, female-owned, fully insured, and only ever one car a day. Based in Canterbury, mobile across Kent."
        ),
        body=body, schemas=[breadcrumbs([("Home", "/"), ("About", "/about/")])],
        nav_key="about", priority="0.7",
    )


def faq_page():
    body = f"""
{crumbs_html([("Home", "/"), ("FAQs", "/faq/")])}
<section class="phead phead--img">
  {phead_bg("gallery/gallery-17.png", 0.5)}
  <div class="wrap">
    <p class="eyebrow">FAQs</p>
    <h1>Everything people ask before booking.</h1>
    <p class="lead">If your question isn't here, call or message me &mdash; I'd rather answer it properly than have you guess.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap" style="max-width:860px">{faq_list(FAQS, open_first=True)}</div>
</section>

{cta_band("Still got a question?", "Call, WhatsApp or send me a message. No pressure, no sales pitch.")}
"""
    write_page(
        "faq",
        title="Car Detailing FAQs | Ash's Detailing, Kent",
        description=(
            "Do you need water and electricity? Why cost more than a car wash? Answers to the questions customers ask before booking detailing in Kent."
        ),
        body=body,
        schemas=[breadcrumbs([("Home", "/"), ("FAQs", "/faq/")]), faq_schema(FAQS)],
        nav_key="faq", priority="0.7",
    )


def contact_page():
    hrs = "".join(f"<li><span>{e(h['label'])}</span><span>{e(h['value'])}</span></li>"
                  for h in SITE["hoursDisplay"])
    body = f"""
{crumbs_html([("Home", "/"), ("Contact", "/contact/")])}
<section class="phead phead--img">
  {phead_bg("ba/after-3.jpg", 0.5)}
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Not quite sure? Let's talk it through.</h1>
    <p class="lead">Every car is different. Whether you want a refresh, a full restoration or just some honest advice about what's worth doing, I'm happy to help &mdash; no pressure either way.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap split" style="align-items:start">
    <div class="stack">
      <div class="callout">
        <h2>Call or message</h2>
        <p>Quickest way to get an answer. If I'm mid-detail I'll come back to you the same day.</p>
        <p style="margin-top:1.25rem">
          <a class="btn btn--primary" href="tel:{PHONE}">Call {PHONE_D}</a>
          <a class="btn btn--ghost" href="https://wa.me/447907019798" rel="noopener" target="_blank">WhatsApp</a>
        </p>
        <p style="margin-top:1rem"><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
      </div>

      <div class="callout">
        <h3>Where I'm based</h3>
        <p>{SITE['street']}, {SITE['locality']} {SITE['postcode']}, {SITE['region']}</p>
        <p style="margin-top:.75rem">I'm mobile &mdash; I travel to you across Kent. <a href="/areas/">See areas covered</a>.</p>
      </div>

      <div class="callout">
        <h2>Hours</h2>
        <ul class="ftr__hrs" style="list-style:none;padding:0;display:grid;gap:.5rem;margin-top:1rem">{hrs}</ul>
        <p class="note">{e(SITE['hoursNote'])} I only ever book one vehicle a day, so the day is yours.</p>
      </div>
    </div>

    <div class="stack">
      <div class="map">
        <iframe title="Map showing Ash's Vehicle Valet and Detailing location near Canterbury"
          src="https://www.openstreetmap.org/export/embed.html?bbox=1.115%2C51.296%2C1.195%2C51.328&amp;layer=mapnik&amp;marker={SITE['lat']}%2C{SITE['lng']}"
          loading="lazy"></iframe>
      </div>
      <p class="center"><a class="btn btn--primary btn--lg" href="/book/">Or send a full booking enquiry</a></p>
      <p class="note center">The booking form asks a few more questions about your vehicle so I can quote accurately first time.</p>
    </div>
  </div>
</section>
"""
    write_page(
        "contact",
        title="Contact | Mobile Car Detailing in Kent | Ash's Detailing",
        description=(
            "Call 07907 019798 or message Ash for mobile car detailing across Canterbury and Kent. Honest advice on what your vehicle needs, no pressure."
        ),
        body=body, schemas=[business_schema(), breadcrumbs([("Home", "/"), ("Contact", "/contact/")])],
        nav_key="contact", priority="0.8",
    )


# --------------------------------------------------------------------------
# areas
# --------------------------------------------------------------------------

def areas_hub():
    cards = "".join(
        f"""<div class="area area--static">
<b>{e(a['name'])}</b><span>{e(a['postcodes'])}</span></div>"""
        for a in AREAS
    )
    body = f"""
{crumbs_html([("Home", "/"), ("Areas", "/areas/")])}
<section class="phead phead--img">
  {phead_bg("ba/after-1-7.jpg", 0.6)}
  <div class="wrap">
    <p class="eyebrow">Areas covered</p>
    <h1>I come to you, right across Kent.</h1>
    <p class="lead">I'm based in Hersden, just outside Canterbury, and I travel to your home or workplace.
    I cover the whole of Kent &mdash; from the coast at Whitstable and Folkestone to Tunbridge Wells in the
    west, and out to the London outskirts. The towns below are simply where I am most often, not the limit
    of where I'll go.</p>
    <div class="hero__actions" style="margin-top:1.75rem">
      <a class="btn btn--primary btn--lg" href="/book/">Book your detail</a>
      <a class="btn btn--ghost btn--lg" href="tel:{PHONE}">Call {PHONE_D}</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head head--center">
      <h2>Where I work</h2>
      <p class="lead">The areas I'm in most weeks. No travel surcharge anywhere on this list &mdash; and if
      your town isn't on it, I almost certainly still come to you.</p>
    </div>
    <div class="areas">{cards}</div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap split">
    <div class="stack measure">
      <p class="eyebrow">Before I arrive</p>
      <h2>What I need on the day.</h2>
      <ul class="ticks" style="margin-top:1.5rem">
        <li>A parking space next to the vehicle</li>
        <li>An outside tap and a plug point within 30 metres &mdash; I carry the hose and extension lead</li>
        <li>Personal belongings out of the cabin and boot</li>
        <li>A heads-up about pet hair, mould or smoke so I can bring the right kit</li>
      </ul>
      <p style="margin-top:1.5rem">If any of that is a problem, say so when you enquire. There's usually a way
      round it and I'd much rather sort it beforehand than turn up and find we're stuck.</p>
    </div>
    <div class="split__media">{picture('home/big-size-image-car.jpg', 'Vehicle being detailed on a customer driveway in Kent by ' + BRAND, '(min-width:840px) 46vw, 90vw')}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap" style="max-width:760px">
    <div class="head head--center">
      <h2>Not on the list?</h2>
      <p class="lead">Anywhere in Kent, just ask &mdash; the list above is where I am most weeks, not a
      boundary. Send me your postcode and I'd rather give you a straight yes or no than have you guess.</p>
    </div>
    <div class="measure" style="margin:0 auto">
      <p>I'll look at work outside Kent too. It tends to make sense on the bigger jobs &mdash; a full paint
      correction, a ceramic coating, or the Ultimate Experience &mdash; where I'm with the car all day anyway
      and the drive is worth making. For those I'd usually add somewhere between &pound;50 and &pound;100 for
      the travel depending on how far it is, and you'll know that number before you commit to anything.</p>
    </div>
    <p class="center" style="margin-top:2rem"><a class="btn btn--primary btn--lg" href="/contact/">Ask about your area</a></p>
  </div>
</section>

{cta_band("Ready when you are.", "Tell me where you are and when suits.")}
"""
    write_page(
        "areas",
        title="Areas Covered Across Kent | Ash's Detailing",
        description=(
            "Mobile car detailing across the whole of Kent — Canterbury, Whitstable, Ashford, Folkestone, Medway, Maidstone and beyond. I travel to you."
        ),
        body=body, schemas=[breadcrumbs([("Home", "/"), ("Areas", "/areas/")])],
        nav_key="areas", priority="0.8",
    )



def thanks_page():
    """Where Netlify sends people after a successful booking enquiry.

    noindex + out of the sitemap: it's only reachable after a POST, and a
    thank-you page in the search results is a dead end for anyone who lands
    on it cold.
    """
    body = f"""
<section class="phead phead--img">
  {phead_bg("ba/after-1-4.jpg", 0.55)}
  <div class="wrap">
    <p class="eyebrow">Enquiry sent</p>
    <h1>Thanks &mdash; that's with me.</h1>
    <p class="lead">I've got your details and I'll come back to you with a date I can actually commit to,
    usually the same day. Nothing is booked and no payment is due until we've agreed that date.</p>
    <div class="hero__actions" style="margin-top:1.75rem">
      <a class="btn btn--primary btn--lg" href="tel:{PHONE}">Call {PHONE_D}</a>
      <a class="btn btn--ghost btn--lg" href="/">Back to the site</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap" style="max-width:760px">
    <div class="callout">
      <h2>What happens next</h2>
      <ol class="steps" style="margin-top:1.25rem">
        <li><div><b>I reply, usually same day</b><p>With a date I can actually commit to.</p></div></li>
        <li><div><b>You confirm</b><p>A {SITE['deposit']} deposit secures the slot and the products.</p></div></li>
        <li><div><b>I arrive and get to work</b><p>Yours is the only car I touch that day.</p></div></li>
        <li><div><b>Balance on completion</b><p>Cash or bank transfer.</p></div></li>
      </ol>
      <p style="margin-top:1.5rem">If it's urgent, or you'd rather talk it through, ring or text me on
      <a href="tel:{PHONE}">{PHONE_D}</a> &mdash; that's usually faster than waiting on email.</p>
    </div>
  </div>
</section>
"""
    write_page(
        "thanks",
        title="Enquiry Sent | Ash's Detailing",
        description="Your booking enquiry has been sent. I'll come back to you with a date, usually the same day.",
        body=body, nav_key="book", noindex=True, in_sitemap=False,
    )


def build():
    home()
    services_hub()
    for s in SERVICES:
        service_page(s)
    pricing_page()
    book_page()
    thanks_page()
    gallery_page()
    reviews_page()
    about_page()
    faq_page()
    contact_page()
    areas_hub()
