# Getting the site in front of Ash

She needs a normal link she can tap on her phone. Nothing to install, no code, no Terminal.

---

## The 3-minute version

**1. Build the share-safe copy as a zip**

```bash
cd "/Users/tyler/Desktop/ashs website" && python3 build.py --clean --preview --zip
```

That writes **`ashs-website-preview.zip`** into the project folder.

`--preview` does two important things:
- Adds `noindex, nofollow` to every page and blocks crawlers in `robots.txt`, so the preview can **never** get picked up by Google and compete with her real site
- Puts a small gold "Preview for review — not the live site" bar at the top, so nobody mistakes it for live

**2. Drop the ZIP online**

Go to **[netlify.com/drop](https://app.netlify.com/drop)** and drag **`ashs-website-preview.zip`** onto the page.

You get a public URL like `https://calm-otter-3f8a21.netlify.app` in about twenty seconds.

> ### ⚠️ Drag the ZIP, not the `dist` folder
> The site is 166 files across nested folders. Dragging the *folder* makes the browser upload every file individually, and it frequently loses the subdirectories — which gives you a working homepage where **every link 404s**. The zip is a single upload, so it can't half-fail.
>
> The zip is built with `index.html` at its root (no `dist/` wrapper), which is what Netlify expects.

**3. Check it before you send it**

Open the URL and click through to **Pricing** and **Gallery**. If those load, everything else will.

**4. Send her the link**

Text it to her. She opens it on her phone like any other website.

---

## ⚠️ Before you send it

**Build with `--preview`, not the normal build.** A public copy of the site without `noindex` is a genuine SEO risk: Google can index the preview, and then two identical sites are competing for the same searches. The preview flag prevents that. When you deploy for real, use the normal `python3 build.py`.

**Tell her not to test the booking form.** The form endpoint hasn't been activated yet (see [handover §5](04-handover.md)), so a test enquiry would go nowhere and she'd think it's broken.

**Ask her to look on her phone first.** That's where most of her customers will see it.

---

## A message you can send her

> Hi Ash — here's the new website, still a draft so nothing is live yet:
>
> [link]
>
> Have a look on your phone first, that's how most people will see it. Don't worry about anything technical, I just want to know:
>
> 1. Does it sound like you? The wording is all new — if anything doesn't sound like something you'd actually say, tell me and I'll change it.
> 2. Is everything **true**? Especially the prices, the services list, and the "six stages" bit on the home page.
> 3. Are the before/after photos matched up right? Drag the slider left and right — is each pair genuinely the same car?
> 4. Anything missing you'd want people to know?
>
> Don't try the booking form yet, it's not switched on.
>
> Just send me a voice note or a list, whatever's easiest.

---

## The things worth her checking most

These are the items where **only she can tell us if it's right** — everything else is my problem, not hers.

| What | Why it needs her |
|---|---|
| **The six-stage process section** | I wrote this from her service lists. Steps are a fair reflection as far as I can tell, but she needs to confirm it's genuinely how she works. |
| **Every price** | The old site contradicted itself in two places. The new one has one price list. She should read it line by line. |
| **The before/after pairs** | I matched these by eye from the photos. A mismatched pair would be embarrassing and damaging. |
| **Opening hours** | Currently 8am–8pm daily, phone and email any time. |
| **"Award-winning in South England"** | Who awarded it? Naming them makes it credible. |
| **The gallery captions** | I wrote deliberately vague ones where I couldn't identify the car. Real names would be better. |
| **The reviews** | Names shortened to "Helen G." style, and two were trimmed where reviewers mentioned health details. She should be comfortable with that. |

---

## If you'd rather she didn't see a public URL at all

Two alternatives:

- **Same wifi:** run `python3 build.py --serve`, find your Mac's IP (System Settings → Network), and send her `http://YOUR-IP:8000`. Only works while your Mac is on and you're both on the same network — fine if she's in the room, useless otherwise.
- **Netlify with a password:** possible, but it's a paid plan feature. The `noindex` preview above is free and good enough for a draft nobody is looking for.
