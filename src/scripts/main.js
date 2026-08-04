/* Ash's Vehicle Valet & Detailing — progressive enhancement only.
   Every page works with this file blocked; it only adds polish. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- header: shadow on scroll, hide on scroll down --------------------- */
  var hdr = $('#hdr');
  if (hdr) {
    var lastY = 0;
    var onScroll = function () {
      var y = window.scrollY;
      hdr.classList.toggle('is-stuck', y > 8);
      var menuOpen = $('.mega.is-open') || $('.mnav.is-open');
      hdr.classList.toggle('is-hidden', !menuOpen && y > 420 && y > lastY + 4);
      lastY = y;
    };
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });
  }

  /* --- mega menu --------------------------------------------------------- */
  var megaBtn = $('.navbtn[aria-controls]');
  if (megaBtn) {
    var mega = document.getElementById(megaBtn.getAttribute('aria-controls'));
    var closeT;
    var setMega = function (open) {
      clearTimeout(closeT);
      megaBtn.setAttribute('aria-expanded', String(open));
      mega.classList.toggle('is-open', open);
    };
    megaBtn.addEventListener('click', function (e) {
      e.preventDefault();
      setMega(megaBtn.getAttribute('aria-expanded') !== 'true');
    });
    [megaBtn, mega].forEach(function (el) {
      el.addEventListener('mouseenter', function () { if (innerWidth > 1120) setMega(true); });
      el.addEventListener('mouseleave', function () {
        if (innerWidth > 1120) closeT = setTimeout(function () { setMega(false); }, 180);
      });
    });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') setMega(false); });
    document.addEventListener('click', function (e) {
      if (!mega.contains(e.target) && !megaBtn.contains(e.target)) setMega(false);
    });
  }

  /* --- full-screen mobile nav ---------------------------------------------
     Opening/closing is handled by CSS (#navtoggle checkbox) so it still works
     if this file never loads. Everything here is optional polish. */
  var navToggle = $('#navtoggle'), mnav = $('.mnav');
  if (navToggle && mnav) {
    var sync = function () {
      var open = navToggle.checked;
      document.body.style.overflow = open ? 'hidden' : '';
      if (open && hdr) hdr.classList.remove('is-hidden');
    };
    navToggle.addEventListener('change', sync);
    mnav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { navToggle.checked = false; sync(); }
    });
    addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && navToggle.checked) { navToggle.checked = false; sync(); }
    });
  }

  /* --- before / after sliders -------------------------------------------- */
  $$('[data-ba]').forEach(function (fig) {
    var stage = $('.ba__stage', fig), range = $('.ba__range', fig);
    if (!stage || !range) return;
    var set = function (v) {
      v = Math.max(0, Math.min(100, v));
      stage.style.setProperty('--pos', v + '%');
    };
    set(range.value);
    range.addEventListener('input', function () { set(range.value); });

    // Drag anywhere on the image, not just the handle.
    var drag = false;
    var at = function (clientX) {
      var r = stage.getBoundingClientRect();
      var v = ((clientX - r.left) / r.width) * 100;
      range.value = v;
      set(v);
    };
    stage.addEventListener('pointerdown', function (e) {
      drag = true; stage.setPointerCapture(e.pointerId); at(e.clientX);
    });
    stage.addEventListener('pointermove', function (e) { if (drag) at(e.clientX); });
    ['pointerup', 'pointercancel'].forEach(function (ev) {
      stage.addEventListener(ev, function () { drag = false; });
    });

    // Nudge off centre when it first scrolls in, so it reads as interactive.
    if (!reduce && 'IntersectionObserver' in window) {
      var teased = false;
      var io = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting || teased) return;
        teased = true;
        var start = performance.now(), from = 50, to = 68;
        var step = function (t) {
          var p = Math.min(1, (t - start) / 900);
          var eased = 1 - Math.pow(1 - p, 3);
          set(from + (to - from) * eased);
          range.value = from + (to - from) * eased;
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
        io.disconnect();
      }, { threshold: 0.45 });
      io.observe(fig);
    }
  });

  /* --- scroll reveal ----------------------------------------------------- */
  var rv = $$('.rv');
  if (rv.length && 'IntersectionObserver' in window && !reduce) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
    rv.forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 70 + 'ms'; ro.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  /* --- animated stat counters -------------------------------------------- */
  var counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window && !reduce) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, target = parseFloat(el.dataset.count);
        var dec = (el.dataset.count.split('.')[1] || '').length;
        var pre = el.dataset.prefix || '', suf = el.dataset.suffix || '';
        var start = performance.now();
        var step = function (t) {
          var p = Math.min(1, (t - start) / 1100);
          var v = target * (1 - Math.pow(1 - p, 3));
          el.textContent = pre + v.toFixed(dec) + suf;
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
        co.unobserve(el);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { co.observe(el); });
  }

  /* --- YouTube facade: nothing loads until the user presses play ----------
     The iframe REPLACES the button rather than going inside it — interactive
     content nested in a <button> is invalid HTML and the player misbehaves. */
  $$('.vid').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.dataset.yt;
      if (!id) return;
      var wrap = document.createElement('div');
      wrap.className = 'vid vid--live';
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1';
      f.title = btn.getAttribute('aria-label') || 'Vehicle transformation video';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      f.allowFullscreen = true;
      wrap.appendChild(f);
      btn.replaceWith(wrap);
    }, { once: true });
  });

  /* --- reveal more reviews ------------------------------------------------ */
  var moreBtn = $('#morerevs');
  if (moreBtn) {
    moreBtn.addEventListener('click', function () {
      $$('.rev--hidden').forEach(function (el) { el.classList.remove('rev--hidden'); });
      moreBtn.remove();
    });
  }

  /* --- gallery lightbox -------------------------------------------------- */
  var thumbs = $$('.gal__i');
  if (thumbs.length) {
    var lb = document.createElement('div');
    lb.className = 'lb';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Image viewer');
    lb.innerHTML = '<button class="lb__x" aria-label="Close">&times;</button>' +
      '<button class="lb__nav lb__nav--p" aria-label="Previous">&#8249;</button>' +
      '<button class="lb__nav lb__nav--n" aria-label="Next">&#8250;</button>' +
      '<div><img alt=""><p class="lb__cap"></p></div>';
    document.body.appendChild(lb);

    var lbImg = $('img', lb), lbCap = $('.lb__cap', lb), idx = 0, last = null;
    function show(i) {
      idx = (i + thumbs.length) % thumbs.length;
      var t = thumbs[idx], src = $('img', t);
      lbImg.src = src.currentSrc || src.src;
      lbImg.alt = src.alt;
      lbCap.textContent = t.dataset.cap || '';
    }
    function open(i) {
      last = document.activeElement; show(i);
      lb.classList.add('is-open'); document.body.style.overflow = 'hidden';
      $('.lb__x', lb).focus();
    }
    function close() {
      lb.classList.remove('is-open'); document.body.style.overflow = '';
      lbImg.src = ''; if (last) last.focus();
    }
    thumbs.forEach(function (t, i) { t.addEventListener('click', function () { open(i); }); });
    $('.lb__x', lb).addEventListener('click', close);
    $('.lb__nav--p', lb).addEventListener('click', function () { show(idx - 1); });
    $('.lb__nav--n', lb).addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* --- gentle hero parallax ----------------------------------------------- */
  var heroImg = $('.hero__bg img');
  if (heroImg && !reduce && matchMedia('(min-width:760px)').matches) {
    var raf = false;
    addEventListener('scroll', function () {
      if (raf) return;
      raf = true;
      requestAnimationFrame(function () {
        var y = Math.min(window.scrollY, 700);
        heroImg.style.transform = 'translate3d(0,' + (y * 0.14).toFixed(1) + 'px,0) scale(1.06)';
        raf = false;
      });
    }, { passive: true });
  }

  /* --- price bump when a configurator value changes ------------------------ */
  function bump(el) {
    if (!el || reduce) return;
    el.classList.remove('is-bump');
    void el.offsetWidth;
    el.classList.add('is-bump');
    setTimeout(function () { el.classList.remove('is-bump'); }, 300);
  }

  /* --- service page configurator ------------------------------------------
     Pick an option, see the price, and carry the choice into the booking form.
     Works without JS too: it's a real GET form pointing at /book/. */
  $$('[data-cfg]').forEach(function (form) {
    var sel = $('select', form), out = $('[data-cfg-price]', form);
    if (!sel || !out) return;
    var sync = function () {
      var o = sel.options[sel.selectedIndex];
      var p = o && o.dataset.price;
      out.textContent = p ? '£' + Number(p).toLocaleString('en-GB') : 'Quoted';
    };
    sel.addEventListener('change', function () { sync(); bump(out); });
    sync();
  });

  /* --- booking form -------------------------------------------------------- */
  var form = $('#bookform');
  if (form) {
    var data = {};
    try { data = JSON.parse($('#pkgdata').textContent); } catch (e) {}

    var pkg = $('#package', form), opt = $('#option', form), est = $('#estimate');

    var priceOf = function () {
      var o = opt && opt.options[opt.selectedIndex];
      return o && o.dataset.price ? Number(o.dataset.price) : null;
    };
    var unitOf = function () {
      var s = pkg.options[pkg.selectedIndex];
      var d = s && data[s.dataset.slug];
      return d ? (d.unit || '') : '';
    };
    var showPrice = function () {
      if (!est) return;
      var p = priceOf();
      est.textContent = p ? '£' + p.toLocaleString('en-GB') + unitOf() : '—';
    };

    var fillOptions = function (preselect) {
      if (!pkg || !opt) return;
      var s = pkg.options[pkg.selectedIndex];
      var slug = s && s.dataset.slug;
      var d = slug && data[slug];
      opt.innerHTML = '';
      if (!d || !d.options.length) {
        opt.innerHTML = '<option value="">Not applicable — I\'ll advise</option>';
        opt.required = false;
        showPrice();
        return;
      }
      opt.required = true;
      d.options.forEach(function (o) {
        var el = document.createElement('option');
        el.value = o.label;
        if (o.price) el.dataset.price = o.price;
        el.textContent = o.label + (o.price ? ' — £' + o.price.toLocaleString('en-GB') + (o.unit || d.unit || '') : ' — quoted')
                         + (o.popular ? ' · most booked' : '');
        opt.appendChild(el);
      });
      var want = preselect && [].slice.call(opt.options).find(function (o) { return o.value === preselect; });
      var pop = d.options.findIndex(function (o) { return o.popular; });
      opt.selectedIndex = want ? [].slice.call(opt.options).indexOf(want) : (pop > -1 ? pop : 0);
      showPrice();
    };

    if (pkg) pkg.addEventListener('change', function () { fillOptions(); });
    if (opt) opt.addEventListener('change', function () { showPrice(); bump(est); });

    // Pre-fill from the service page: /book/?service=slug&option=Label
    var q = new URLSearchParams(location.search);
    var wantSlug = q.get('service'), wantOpt = q.get('option');
    if (wantSlug && pkg) {
      var match = [].slice.call(pkg.options).find(function (o) { return o.dataset.slug === wantSlug; });
      if (match) {
        pkg.value = match.value;
        fillOptions(wantOpt);
        var box = $('#quotebox');
        if (box) {
          box.classList.add('quote--set');
          form.scrollIntoView({ block: 'start', behavior: reduce ? 'auto' : 'smooth' });
        }
      }
    } else {
      fillOptions();
    }

    form.addEventListener('submit', function (e) {
      var bad = null;
      $$('[required]', form).forEach(function (f) {
        var wrap = f.closest('.field');
        var ok = f.checkValidity();
        if (wrap) wrap.classList.toggle('has-err', !ok);
        if (!ok && !bad) bad = f;
      });
      if (bad) {
        e.preventDefault(); bad.focus();
        bad.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
      }
    });
  }
})();
