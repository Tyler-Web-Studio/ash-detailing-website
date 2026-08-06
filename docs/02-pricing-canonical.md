# Canonical price list

**Confirmed with Ash 31 July 2026. Re-verified against the live booking flow 6 August 2026 — all 28 package prices matched, zero changes required.**

This document mirrors `src/data/pricing.json`, which is what the site is generated from. Changing a price is a one-line edit in one place.

All prices in GBP. **Not VAT registered** — the quoted price is the price paid.

## Which live source wins

Ash's old site carries **two** price lists, and as of 6 August 2026 they disagree:

| Source | Status |
|---|---|
| **The booking flow** (`/book-now/` Ecwid store) | ✅ **CANONICAL.** This is where customers receive their actual quoted price. Verified option-by-option on 6 Aug 2026; matches `pricing.json` exactly. |
| The marketing page (`/our-services-and-prices/`) | ❌ **Do not use.** Hand-edited 6 Aug 2026 and now inconsistent with the booking flow — it shows Premium Exterior £120 vs £140, Premium Interior £180 vs £150, Ceramic "£400+" vs £340, and Ultimate £800 vs £600. |

**Rule: the booking flow is the source of truth, because that is the number the customer is actually charged.** If the two ever disagree again, take the booking flow and get the marketing page corrected — never the reverse.

> ⏳ **Open — needs Ash.** *The Ultimate Experience* has **no booking-flow entry**, so there is no canonical number for it. Our site says **£600**; her marketing page was changed to **£800** on 6 Aug 2026. Left at £600 pending her confirmation. This is the only unresolved price on the site.

---

## 1. Exterior Detail — from £100

| Option | Surcharge | **Total** |
|---|---|---|
| Basic | — | **£100** |
| Premium | +£40 | **£140** |
| Large Van (basic) | +£20 | **£120** |
| Caravan (basic) | +£50 | **£150** |
| Premium Large Van | +£40 | **£140** |
| Premium Caravan | +£70 | **£170** |
| Premium + 2-step machine polish | +£150 | **£250** |
| Premium XL + 2-step polish (vans) | +£200 | **£300** |
| Caravans (full) | +£350 | **£450** |

> ✅ **Resolved.** *Premium Large Van* comes out at £140 — the same as a standard car Premium — even though *Large Van basic* carries a +£20 surcharge. Confirmed correct by Ash (31 July 2026) and re-confirmed against the live booking flow (6 Aug 2026). **Do not "fix" this.**

## 2. Interior Detail — from £130

| Option | Surcharge | **Total** |
|---|---|---|
| Basic | — | **£130** |
| Premium | +£20 | **£150** |
| Large Vehicle Basic | +£30 | **£160** |
| Large Vehicle Premium | +£50 | **£180** |

## 3. Interior + Exterior Detail — from £180

| Option | Surcharge | **Total** |
|---|---|---|
| Basic | — | **£180** |
| Premium | +£60 | **£240** |
| XL Vehicle (6+ seats) Basic | +£40 | **£220** |
| XL Vehicle (6+ seats) Premium | +£80 | **£260** |
| Premium + 2-step machine polish | +£170 | **£350** |

## 4. Ceramic Coating — from £340

Exterior only. Includes full exterior detail + 2-step polish + coating.

| Option | Surcharge | **Total** |
|---|---|---|
| 1 year | +£40 | **£340** |
| 2 year | +£50 | **£350** |
| 5 year | +£150 | **£450** |
| 1 year + Interior Premium | +£100 | **£400** |
| 2 year + Interior Premium | +£120 | **£420** |
| 5 year + Interior Premium | +£220 | **£520** |

> The live site advertises "£300+". The lowest buyable price is **£340**. Corrected in the rebuild.

---

## 5. Flagship & recurring

| Service | Price | Notes |
|---|---|---|
| **The Ultimate Experience** ⏳ | **£600** | ⏳ *Not in the booking flow — her marketing page now says £800. Awaiting Ash's confirmation; see the note at the top.* Drop-off only, 2-day full transformation. Premium interior & exterior detail, 2–3 step polish, 5-year ceramic coating, chrome/rubber/vinyl restoration, glass shield, interior protection, alloy deep clean, engine bay detail, air-con decontamination, exhaust metal polish, seat removal, headlight restoration. |
| **Maintenance plan** | **£70 / month** | Only available after a full interior/exterior detail, so the vehicle starts in the right condition. |

## 6. Specialist work (quoted)

| Service | Price | Notes |
|---|---|---|
| SMART scratch / defect repair (exterior) | £300 +/- | Quote required. Book **1 week ahead** — paint must be colour-matched and ordered. May need 2 sessions where filler is involved. Not a body shop. Includes an exterior detail. |
| SMART alloy repair | £100 per alloy | Sanding, filler, re-spray. Not diamond-cut or powder coating (a body shop charges ~£400/wheel). Rebalancing recommended afterwards, ~£8–15/wheel at a garage. |
| Vinyl / sticker removal | £100–£500 | Priced on quantity. **25% off the detail** when booked together. |
| Badge removal | £100 | De-badging, then machine polish to remove residue. |

## 7. Add-ons

| Add-on | Price | Notes |
|---|---|---|
| Headlight restoration | £50 | +£10 per mile if booked standalone |
| Ozone treatment | £50 | Interior packages only. 48 hours airing required. Temporary chlorine-like scent up to 2 weeks. |
| Engine bay detail | £30 | |
| Exterior metal polishing | +£20 | On the £350 package |

## 8. Condition surcharges

Assessed on arrival and agreed before work starts.

| Condition | Range |
|---|---|
| Excess dirt | £20 – £40 |
| Mould | £20 – £100 |
| Pet hair | £20 – £50 |

Mould can need two sessions — surface mould often doesn't reflect how deep the problem goes — and may require an ozone treatment.

## 9. Discounts

| Offer | Value |
|---|---|
| Blue light & emergency services | 5% off |
| Leave a review | £10 off your next booking |
| Refer a friend | Friend gets £10 off · you get £10 cashback |

## 10. Terms

- **20% deposit** secures the booking — covers the reserved slot and preparation of premium products.
- Customer must provide a **parking space near the vehicle, with access to water and electricity**. Ash carries 30m of hose and extension lead; alternatives can usually be arranged.
- A detail takes **3–12 hours** depending on package. **One vehicle per day** — never rushed, never double-booked.
- Payment by cash or bank transfer.
- Additional fees apply for XL vehicles, vans, caravans and HGVs.
