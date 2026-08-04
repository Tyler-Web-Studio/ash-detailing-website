# Running Lighthouse

## First — don't extract the zips

The two `.zip` files are **only** for dragging onto Netlify. Never unzip them.

Extracting one created an `ashs-website/` folder inside the project, which was just a duplicate of `dist/` — I've deleted it. If you extract one again, throw the extracted folder away; it isn't used for anything.

**The only folder that matters is `dist/`.** That's what the build writes and what gets deployed.

---

## Step 1 — start the site

Double-click **`Preview site.command`** in the project folder.

It rebuilds, starts a local server, and opens your browser at `http://localhost:8765`.
Leave the Terminal window open. (This runs the **production** build, so the SEO score is accurate.)

---

## Step 2 — open a clean browser window

**Use a private/incognito window with no extensions.** Extensions and ad-blockers skew Performance and Best Practices badly, and you'll chase problems that aren't yours.

- Chrome: `⌘⇧N`
- Brave: `⌘⇧N`, and turn **Shields down** for localhost (click the lion in the address bar)

Paste in `http://localhost:8765`

---

## Step 3 — run it

1. `⌘⌥I` to open DevTools
2. In the DevTools top bar, click the **`»`** chevron and choose **Lighthouse**
3. Set:
   - **Mode:** Navigation
   - **Device:** Mobile *(test this first — it's where most customers are, and it's the harsher score)*
   - **Categories:** tick Performance, Accessibility, Best Practices, SEO
4. Click **Analyze page load**

Run it on a few pages, not just the homepage: `/pricing/`, `/services/exterior-detail/`, `/gallery/`, `/book/`.

---

## ⚠️ Two things that will mislead you

**1. Performance on localhost is inflated.** There's no network latency, so it'll read higher than reality. Accessibility, Best Practices and SEO are accurate locally — Performance is not.

For a real Performance number, deploy `ashs-website.zip` to Netlify and run Lighthouse against that URL instead.

**2. Never Lighthouse the preview build.** `ashs-website-preview.zip` sets `noindex` on purpose, so SEO will fail on "Page is blocked from indexing" and cap around 70–80. That's correct behaviour for a draft, not a bug. Use the production build for scoring.

---

## What I've already verified by hand

I can't run Lighthouse on this machine (no Chrome CLI), so I audited its underlying checks directly:

| Check | Result |
|---|---|
| Colour contrast (WCAG AA) | Every text/background pair computed. 0 failures. |
| Heading order | 0 skips across all 18 pages |
| Images with `alt` | 0 missing |
| Images with `width`/`height` | 0 missing (protects CLS) |
| Duplicate element IDs | 0 |
| Buttons/links without accessible names | 0 |
| Horizontal overflow at 375px | 0 on every page |
| Tap targets under 44px | only inline links inside sentences, which Lighthouse excludes |
| Console errors | 0 |
| `rel="noopener"` on external links | all present |
| Title / description lengths | all within search-result limits |
| Structured data | valid JSON-LD on all 18 pages |

**If Lighthouse still flags something, send me the report and I'll fix exactly what it names.** I'd rather work from its actual output than guess at what it might say.
