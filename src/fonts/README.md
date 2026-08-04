# Fonts

**Archivo** — variable weight 100–900, latin subset, self-hosted as woff2 (34 KB).

Licensed under the SIL Open Font License 1.1 (see `OFL.txt`), which permits
redistribution and self-hosting. Self-hosted rather than loaded from Google's
CDN so there is no third-party request, no privacy exposure, and no extra DNS
lookup on the critical path.

Preloaded in `base.html` and declared with `font-display: swap` plus a metric-ish
system fallback, so text paints immediately and the swap causes minimal shift.
