#!/usr/bin/env python3
"""Build content subpages + privacy-policy + sitemap for Sauna Accessories (tier-2).

Each content page: random hero image (of 6), random YouTube video (of 4), random
social embed (of 6) in the sidebar, and ONE inline tier-1 link in body text with
anchor "sauna accessories" pointing at the tier-1 homepage. Shared header/footer
loaded from components/. The homepage (index.html) is hand-written separately.

Tier rules (cloud-stack workflow):
  - tier-1 link is a plain inline <a> in body intro text, anchor fixed by the user.
  - TIER1_URL absent from header, footer, privacy, sitemap.
  - No mother-brand social icons in the footer.
"""
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent

TIER1_URL = "https://sauna-lifestyle-ls7g3.ondigitalocean.app/"
TIER1_ANCHOR = "sauna lifestyle"

# --- Image pool (6) : filename -> alt text -------------------------------
IMAGES = [
    ("sauna-accessories-bucket-ladle.avif", "Traditional wooden sauna bucket and ladle on a sauna bench"),
    ("sauna-accessories-whisk-vasta.avif", "Fresh birch sauna whisk (vasta) on a wooden bench"),
    ("sauna-accessories-towel-aroma.avif", "Folded towels and aroma oil on a wooden sauna bench"),
    ("sauna-accessories-lighting.avif", "Warm candlelit sauna interior with soft lighting"),
    ("sauna-accessories-thermometer-hat.avif", "Felt sauna hat and wooden thermometer on a sauna bench"),
    ("sauna-accessories-heater-stones.avif", "Glowing sauna heater stones in a warm wooden sauna"),
]
IMAGE_FILES = [i[0] for i in IMAGES]
IMAGE_ALT = dict(IMAGES)

# --- Video pool (4) --------------------------------------------------------
VIDEOS = [
    "edIPy58vREQ",
    "rTBaHoV5rQo",
    "Fm5MxRaRrLs",
    "UAsdvH0yrcw",
]

# --- Social embed pool (6) -------------------------------------------------
# format: (title, iframe-src, fallback-link)
SOCIALS = [
    ("Saunazilla on X", "https://platform.twitter.com/embed/Tweet.html?id=2099398319445299577",
     "https://x.com/saunazilla/status/2099398319445299577"),
    ("Saunazilla on X", "https://platform.twitter.com/embed/Tweet.html?id=2097252883825660215",
     "https://x.com/saunazilla/status/2097252883825660215"),
    ("Saunazilla on X", "https://platform.twitter.com/embed/Tweet.html?id=2095429689800048736",
     "https://x.com/saunazilla/status/2095429689800048736"),
    ("Saunazilla on Pinterest", "https://fi.pinterest.com/pin/924645367275139988/embed/",
     "https://fi.pinterest.com/pin/924645367275139988/"),
    ("Saunazilla on Pinterest", "https://fi.pinterest.com/pin/924645367275140150/embed/",
     "https://fi.pinterest.com/pin/924645367275140150/"),
    ("Saunazilla on Pinterest", "https://fi.pinterest.com/pin/924645367271490187/embed/",
     "https://fi.pinterest.com/pin/924645367271490187/"),
]

_rng = random.Random()


def pick(pool):
    return pool[_rng.randrange(len(pool))]


def json_ld_webpage(title, meta_desc, url):
    import json as _json
    data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": meta_desc,
        "url": url,
        "inLanguage": "en",
    }
    return _json.dumps(data, ensure_ascii=False)


def inject_schema(html, fname):
    """Inject a WebPage JSON-LD block into the <head> of a generated page."""
    import re as _re
    m = _re.search(r"<title>(.*?)</title>", html, _re.S)
    title = (m.group(1).strip().replace("&amp;", "&") if m else "")
    m = _re.search(r'<meta name="description" content="([^"]*)"', html)
    desc = m.group(1) if m else ""
    url = "/index.html" if fname == "index.html" else "/" + fname
    block = ('<script type="application/ld+json">'
             + json_ld_webpage(title, desc, url)
             + '</script>\n')
    i = html.find("</head>")
    return html[:i] + block + html[i:] if i != -1 else html


def build_page(slug, title, description, h1, h2s, closing, related):
    hero_img, hero_alt = pick([(f, IMAGE_ALT[f]) for f in IMAGE_FILES])
    vid_id = pick(VIDEOS)
    s_title, s_src, s_link = pick(SOCIALS)

    # Intro with the single tier-1 inline link (anchor fixed by user).
    intro = (
        f'<p><strong>{h1}</strong> is about choosing the right gear for a relaxed, '
        f'enjoyable session. Whether you are enjoying a home sauna for the first time '
        f'or refining a seasoned routine, the essentials below pair well with the '
        f'broader <a href="{TIER1_URL}" target="_blank" rel="noopener">'
        f'<strong>{TIER1_ANCHOR}</strong></a> guidance on how to make the most of every '
        f'visit. On this page we break down what matters, what to look for, and how '
        f'to care for each item.</p>'
    )

    h2_html = ""
    mid_done = False
    for i, h2 in enumerate(h2s):
        if i == 1:
            mid = pick([(f, IMAGE_ALT[f]) for f in IMAGE_FILES])
            h2_html += (
                f'\n<img class="featured-image" src="img/{mid[0]}" alt="{mid[1]}" '
                f'onerror="this.style.display=\'none\'">\n'
                f'<p class="image-caption">{mid[1]}.</p>\n'
            )
        h2_html += (
            f'\n<h2>{h2}</h2>\n'
            f'<p>Getting <strong>{h2.lower()}</strong> right comes down to a few simple, '
            f'consistent choices. The people who enjoy their sauna most are not chasing '
            f'the biggest collection of gear — they pick what suits their space, use it '
            f'well, and look after it so it lasts.</p>\n'
            f'<p>Start with how you actually like to sauna: alone or with others, at home '
            f'or at a public bath, traditional heat or gentle warmth. With that in mind, '
            f'a short list of <strong>{h2.lower()}</strong> choices quickly feels natural '
            f'rather than overwhelming.</p>\n'
            f'<h3>Keep it simple and build from there</h3>\n'
            f'<p>The best accessories are the ones you reach for without thinking. Choose '
            f'materials that handle heat and moisture well, keep items within easy reach '
            f'of the sauna, and add new pieces only when they genuinely improve the '
            f'experience.</p>\n'
        )

    closing_html = (
        f'\n<h2>{closing}</h2>\n'
        f'<p>We hope this guide to <strong>{h1}</strong> gives you a clear, practical '
        f'starting point. The right accessories make a good sauna feel effortless — '
        f'choose well, care for them, and let comfort do the rest. Explore the related '
        f'guides in the sidebar to keep building your understanding of the kit.</p>\n'
    )

    related_html = ""
    for rtitle, rslug in related:
        related_html += f'<li><a href="{rslug}">{rtitle} <span class="count">Guide</span></a></li>\n'

    video_html = (
        f'<div class="video-embed">\n'
        f'<iframe width="100%" height="400" src="https://www.youtube.com/embed/{vid_id}" '
        f'title="Sauna Accessories video" frameborder="0" '
        f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; '
        f'picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" '
        f'allowfullscreen></iframe>\n</div>\n'
    )

    platform = s_title.split(" on ")[1] if " on " in s_title else "Social"
    social_html = (
        f'<div class="sidebar-card">\n'
        f'<h4>{s_title}</h4>\n'
        f'<div class="social-embed">\n'
        f'<iframe src="{s_src}" title="{s_title}" frameborder="0" '
        f'allowfullscreen scrolling="no" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>\n'
        f'<p style="font-size:.8rem;margin-top:8px;"><a href="{s_link}" target="_blank" '
        f'rel="noopener">View on {platform}</a></p>\n'
        f'</div>\n</div>\n'
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

  <!-- Header placeholder -->
  <div id="header-placeholder"></div>

  <!-- ====== HERO ====== -->
  <div class="page-hero">
    <img class="hero-bg" src="img/{hero_img}" alt="{hero_alt}"
         onerror="this.style.display='none'">
    <div class="hero-overlay">
      <div class="hero-category">Sauna Accessories</div>
      <h1 class="hero-title">{h1}</h1>
      <p class="hero-description">{description}</p>
    </div>
  </div>

  <!-- ====== BREADCRUMB ====== -->
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="index.html">Home</a><span>›</span>
    {h1}
  </nav>

  <!-- ====== MAIN LAYOUT ====== -->
  <div class="layout">

    <!-- ====== MAIN CONTENT ====== -->
    <main class="content-main">

      {intro}

      {video_html}

      {h2_html}

      {closing_html}

      <!-- ====== CTA (internal — homepage carries the tier-1 link) ====== -->
      <div class="cta-box">
        <h3>Explore the Sauna Accessories Guide</h3>
        <p>From starter kits to thoughtful gifts, find the gear that makes every
        session more comfortable.</p>
        <a href="essential-sauna-accessories.html" class="cta-btn">Build Your Kit</a>
      </div>

    </main>

    <!-- ====== SIDEBAR ====== -->
    <aside class="sidebar">

      <div class="sidebar-card">
        <h4>About This Page</h4>
        <p>Learn more about <strong>{h1}</strong> — a practical, honest guide to the
        accessories that make sauna more comfortable, easier and more enjoyable.</p>
      </div>

      {social_html}

      <div class="sidebar-card">
        <h4>Popular Guides</h4>
        <ul class="category-list">
          <li><a href="essential-sauna-accessories.html">Essential Set <span class="count">Guide</span></a></li>
          <li><a href="sauna-bucket-and-ladle.html">Bucket and Ladle <span class="count">Guide</span></a></li>
          <li><a href="sauna-hat.html">Sauna Hats <span class="count">Guide</span></a></li>
          <li><a href="sauna-lighting.html">Lighting <span class="count">Guide</span></a></li>
          <li><a href="sauna-aroma-oils.html">Aroma Oils <span class="count">Guide</span></a></li>
          <li><a href="sauna-gifts.html">Sauna Gifts <span class="count">Guide</span></a></li>
        </ul>
      </div>

      <div class="sidebar-card">
        <h4>Related Pages</h4>
        <ul class="category-list">
          {related_html}
        </ul>
      </div>

    </aside>

  </div><!-- /layout -->

  <!-- Footer placeholder -->
  <div id="footer-placeholder"></div>

  <!-- Scripts -->
  <script src="assets/js/include.js"></script>
</body>
</html>
"""
    return html


# ---- page data: slug, title, desc, h1, h2s, closing, related -----------------
PAGES = [
    ("essential-sauna-accessories",
     "Essential Sauna Accessories – The Complete Starting Set",
     "Discover the essential sauna accessories every sauna needs, from bucket and ladle to whisk, hat, thermometer and lighting. Build a kit that lasts.",
     "Essential Sauna Accessories",
     ["The starter set that covers the basics", "What each essential actually does", "Choosing quality that lasts + care"],
     "Build Your Sauna Kit Today",
     [("Bucket and Ladle", "sauna-bucket-and-ladle.html"),
      ("Sauna Whisk", "sauna-whisk.html"),
      ("Felt Sauna Hat", "sauna-hat.html"),
      ("Sauna Lighting", "sauna-lighting.html")]),

    ("sauna-bucket-and-ladle",
     "Sauna Buckets and Ladles – The Heart of Löyly",
     "Learn why a wooden sauna bucket and ladle are the heart of löyly, how to choose the right size and material, and how to care for them.",
     "Sauna Buckets and Ladles",
     ["Why wood is the classic choice", "Choosing the right size and shape", "Winter-proofing, seasoning and care"],
     "Perfect Your Löyly",
     [("Essential Set", "essential-sauna-accessories.html"),
      ("Sauna Whisk", "sauna-whisk.html"),
      ("Heater Stones", "sauna-heater-stones.html"),
      ("Sauna Timers", "sauna-timer.html")]),

    ("sauna-whisk",
     "Sauna Whisk (Vasta / Vihta) – Tradition and Ritual",
     "Learn about the sauna whisk (vasta or vihta), a traditional birch bundle used for gentle massage, aroma and an authentic Finnish sauna experience.",
     "The Sauna Whisk (Vasta / Vihta)",
     ["What a vasta is and where it comes from", "How to prep, use and store your whisk", "The birch aroma that defines the ritual"],
     "Embrace the Ritual",
     [("Bucket and Ladle", "sauna-bucket-and-ladle.html"),
      ("Essential Set", "essential-sauna-accessories.html"),
      ("Bath Brushes", "sauna-brush.html"),
      ("Aroma Oils", "sauna-aroma-oils.html")]),

    ("sauna-hat",
     "Felt Sauna Hat – Protect Your Head in Style",
     "Discover the felt sauna hat, why it protects your head from intense heat, and how to choose a wool felt hat that stays comfortable for years.",
     "The Felt Sauna Hat",
     ["Why a hat makes a difference in the heat", "Wool felt vs lighter materials", "Fit, style and care for your hat"],
     "Stay Cool-Headed in the Heat",
     [("Essential Set", "essential-sauna-accessories.html"),
      ("Benches and Backrests", "sauna-bench.html"),
      ("Sauna Gifts", "sauna-gifts.html"),
      ("Thermometers", "sauna-thermometer.html")]),

    ("sauna-thermometer",
     "Sauna Thermometer – Read the Heat Right",
     "Choose the right sauna thermometer to dial in the perfect temperature. Learn digital vs analog, mounting best practice and safety.",
     "Sauna Thermometers",
     ["Why precise heat matters", "Digital vs analog readings", "Mounting, placement and accuracy"],
     "Get the Temperature Right",
     [("Essential Set", "essential-sauna-accessories.html"),
      ("Sauna Timers", "sauna-timer.html"),
      ("Heater Stones", "sauna-heater-stones.html"),
      ("Sauna Lighting", "sauna-lighting.html")]),

    ("sauna-lighting",
     "Sauna Lighting – Set the Mood With Warm Light",
     "Create the perfect sauna ambiance with warm, dim lighting. Learn placement, safety and how candlelight completes the retreat.",
     "Sauna Lighting",
     ["Warm vs bright — finding the mood", "Placement and heat-safe fixtures", "Candles and the finishing touch"],
     "Light Up Relaxation",
     [("Essential Set", "essential-sauna-accessories.html"),
      ("Aroma Oils", "sauna-aroma-oils.html"),
      ("Benches and Backrests", "sauna-bench.html"),
      ("Felt Sauna Hat", "sauna-hat.html")]),

    ("sauna-bench",
     "Sauna Benches and Backrests – Comfort in the Heat",
     "Choose the right sauna bench height, layering and material, plus backrests and cushions, for comfortable, relaxing sessions.",
     "Sauna Benches and Backrests",
     ["Height, layering and airflow", "Choosing the right wood", "Backrests, cushions and additions"],
     "Sit Back and Relax",
     [("Essential Set", "essential-sauna-accessories.html"),
      ("Backrests and Headrests", "sauna-backrest.html"),
      ("Sauna Lighting", "sauna-lighting.html"),
      ("Sauna Hats", "sauna-hat.html")]),

    ("sauna-aroma-oils",
     "Sauna Aroma Oils – Scents for a Calmer Session",
     "Discover sauna aroma oils, how they're released through löyly water, the best scents to try, and how to use them safely.",
     "Sauna Aroma Oils",
     ["How aroma is released in the sauna", "The best scents for relaxation", "Safe, measured use on the stones"],
     "Set Your Senses Free",
     [("Bucket and Ladle", "sauna-bucket-and-ladle.html"),
      ("Sauna Whisk", "sauna-whisk.html"),
      ("Essential Set", "essential-sauna-accessories.html"),
      ("Sauna Lighting", "sauna-lighting.html")]),

    ("sauna-towels",
     "Sauna Towels and Linens – Stay Dry, Stay Comfortable",
     "Choose the right sauna towels, robes and sit-on linens for comfort and hygiene. Learn materials, rotation and care.",
     "Sauna Towels and Linens",
     ["The right towel for the job", "Robes, wraps and sit-on cloths", "Care, rotation and keeping them fresh"],
     "Stay Comfortable and Dry",
     [("Essential Set", "essential-sauna-accessories.html"),
      ("Slippers and Sandals", "sauna-slippers.html"),
      ("Bath Brushes", "sauna-brush.html"),
      ("Sauna Baskets", "sauna-baskets.html")]),

    ("sauna-baskets",
     "Sauna Baskets – Organize Your Accessories",
     "Keep sauna essentials organized with a sturdy basket. Learn what to store, which materials last in the heat, and placement ideas.",
     "Sauna Baskets",
     ["What to keep within reach", "Materials that handle moisture", "Placement that keeps the sauna tidy"],
     "Tidy Up Your Sauna",
     [("Essential Set", "essential-sauna-accessories.html"),
      ("Towels and Linens", "sauna-towels.html"),
      ("Sauna Gifts", "sauna-gifts.html"),
      ("Bath Brushes", "sauna-brush.html")]),

    ("sauna-timer",
     "Sauna Timer – Time Your Session Without Checking Your Phone",
     "Use a sauna timer or hourglass to track your session the traditional way. Learn placement, options and sensible session lengths.",
     "Sauna Timers",
     ["Analog timers and hourglasses", "Where to place a timer", "Sensible session lengths and pacing"],
     "Time Your Session Well",
     [("Essential Set", "essential-sauna-accessories.html"),
      ("Thermometers", "sauna-thermometer.html"),
      ("Sauna Lighting", "sauna-lighting.html"),
      ("Sauna Hats", "sauna-hat.html")]),

    ("sauna-heater-stones",
     "Sauna Stones – Choose and Care for Your Heater Rocks",
     "Learn why sauna stones matter, how to choose the right rocks, and how to arrange and replace them for even heat and good löyly.",
     "Sauna Heater Stones",
     ["What good stones do", "Choosing the right rocks", "Arranging, cleaning and replacing"],
     "Get the Heat Just Right",
     [("Bucket and Ladle", "sauna-bucket-and-ladle.html"),
      ("Essential Set", "essential-sauna-accessories.html"),
      ("Thermometers", "sauna-thermometer.html"),
      ("Sauna Timers", "sauna-timer.html")]),

    ("sauna-slippers",
     "Sauna Slippers and Sandals – Simple Comfort",
     "Choose comfortable sauna slippers or sandals for hygiene and comfort between sauna and shower. Learn materials and care.",
     "Sauna Slippers and Sandals",
     ["Why footwear makes a difference", "Materials that handle water", "Finding the right fit and care"],
     "Step Comfortably",
     [("Towels and Linens", "sauna-towels.html"),
      ("Essential Set", "essential-sauna-accessories.html"),
      ("Sauna Baskets", "sauna-baskets.html"),
      ("Bath Brushes", "sauna-brush.html")]),

    ("sauna-brush",
     "Sauna Bath Brushes – Cleanse and Massage",
     "Discover sauna bath brushes for cleansing and gentle massage. Learn dry vs wet brushing, materials, and a simple ritual.",
     "Sauna Bath Brushes",
     ["Dry vs wet brushing", "Choosing fibre and handle", "A simple cleansing ritual"],
     "Polish the Ritual",
     [("Sauna Whisk", "sauna-whisk.html"),
      ("Aroma Oils", "sauna-aroma-oils.html"),
      ("Towels and Linens", "sauna-towels.html"),
      ("Essential Set", "essential-sauna-accessories.html")]),

    ("sauna-backrest",
     "Sauna Backrests and Headrests – Posture in the Heat",
     "Choose a sauna backrest or headrest to support your posture and comfort during longer sessions. Learn options and materials.",
     "Sauna Backrests and Headrests",
     ["Supporting your back in the heat", "Headrest and cushion options", "Materials, mounting and fit"],
     "Relax in Perfect Posture",
     [("Benches and Backrests", "sauna-bench.html"),
      ("Essential Set", "essential-sauna-accessories.html"),
      ("Felt Sauna Hat", "sauna-hat.html"),
      ("Sauna Lighting", "sauna-lighting.html")]),

    ("sauna-gifts",
     "Sauna Gifts – Thoughtful Presents for Sauna Lovers",
     "Find thoughtful sauna gifts for every budget, from buckets and hats to aroma sets and books. Perfect presents for sauna lovers.",
     "Sauna Gifts",
     ["Gift ideas for every budget", "Personalising a gift kit", "Wrapping and presenting the ritual"],
     "Give the Gift of Relaxation",
     [("Essential Set", "essential-sauna-accessories.html"),
      ("Baskets", "sauna-baskets.html"),
      ("Felt Sauna Hat", "sauna-hat.html"),
      ("Aroma Oils", "sauna-aroma-oils.html")]),

    ("privacy-policy",
     "Privacy Policy – Sauna Accessories",
     "Learn how Sauna Accessories handles your data — a simple, transparent privacy policy for this informational site.",
     "Privacy Policy",
     ["Information we collect", "How we use information", "Cookies and third parties", "Your choices"],
     "",
     [("Home", "index.html")]),

    ("sitemap",
     "Sitemap – Sauna Accessories",
     "Browse all pages on Sauna Accessories, from essentials to comfort, ambience and gift guides.",
     "Sitemap",
     [],
     "",
     [("Home", "index.html")]),
]


def main():
    rng_state = _rng.getstate()
    for slug, title, description, h1, h2s, closing, related in PAGES:
        if slug == "privacy-policy":
            html = _static_page(title, description, h1, is_privacy=True)
        elif slug == "sitemap":
            html = _sitemap_page()
        else:
            html = build_page(slug, title, description, h1, h2s, closing, related)
        out = BASE / f"{slug}.html"
        out.write_text(inject_schema(html, f"{slug}.html"), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size} bytes)")
    print("\nDone.")


def _page_shell(title, description, h1, body_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

  <div id="header-placeholder"></div>

  <div class="page-hero">
    <div class="hero-overlay">
      <div class="hero-category">Sauna Accessories</div>
      <h1 class="hero-title">{h1}</h1>
      <p class="hero-description">{description}</p>
    </div>
  </div>

  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="index.html">Home</a><span>›</span>
    {h1}
  </nav>

  <div class="layout">
    <main class="content-main">
      {body_html}
    </main>
    <aside class="sidebar">
      <div class="sidebar-card">
        <h4>About Sauna Accessories</h4>
        <p>A practical guide to the gear behind a great sauna session — from the
        starter essentials to comfort, ambience and thoughtful gifts.</p>
      </div>
      <div class="sidebar-card">
        <h4>Popular Guides</h4>
        <ul class="category-list">
          <li><a href="essential-sauna-accessories.html">Essential Set <span class="count">Guide</span></a></li>
          <li><a href="sauna-bucket-and-ladle.html">Bucket and Ladle <span class="count">Guide</span></a></li>
          <li><a href="sauna-hat.html">Sauna Hats <span class="count">Guide</span></a></li>
          <li><a href="sauna-gifts.html">Sauna Gifts <span class="count">Guide</span></a></li>
        </ul>
      </div>
    </aside>
  </div>

  <div id="footer-placeholder"></div>

  <script src="assets/js/include.js"></script>
</body>
</html>
"""


def _static_page(title, description, h1, is_privacy=False):
    if is_privacy:
        body = """<h2>Overview</h2>
        <p>This privacy policy explains how Sauna Accessories handles information when
        you visit this informational website. We keep things simple: we do not require
        an account, and we do not sell personal data.</p>
        <h2>Information we collect</h2>
        <p>We do not ask you to create an account or provide personal details to browse
        the site. Like most websites, our hosting provider may record standard, technical
        information such as your IP address, browser type and the pages you visit, for
        security and analytics purposes.</p>
        <h2>How we use information</h2>
        <p>Any technical information collected is used to keep the site secure, understand
        how it is used, and improve the content. We do not use it to identify you
        personally.</p>
        <h2>Cookies and third parties</h2>
        <p>Some pages embed media — such as videos and social posts — from third-party
        services like YouTube, X and Pinterest. These services may set their own cookies
        and process data under their own privacy policies. We encourage you to review the
        policies of those services directly.</p>
        <h2>Your choices</h2>
        <p>You can browse without providing personal information, and you can clear
        cookies through your browser settings at any time.</p>
        <p>If you have any questions about this policy, please reach out via the contact
        details shown on the host of this site.</p>"""
    else:
        body = "<h2>Site pages</h2><p>Browse all pages via the <a href=\"sitemap.html\">sitemap</a>.</p>"
    return _page_shell(title, description, h1, body)


def _sitemap_page():
    title = "Sitemap – Sauna Accessories"
    desc = "Browse all pages on Sauna Accessories, from essentials to comfort, ambience and gift guides."
    links = [
        ("Essential Sauna Accessories", "essential-sauna-accessories.html"),
        ("Sauna Buckets and Ladles", "sauna-bucket-and-ladle.html"),
        ("The Sauna Whisk (Vasta / Vihta)", "sauna-whisk.html"),
        ("The Felt Sauna Hat", "sauna-hat.html"),
        ("Sauna Thermometers", "sauna-thermometer.html"),
        ("Sauna Lighting", "sauna-lighting.html"),
        ("Sauna Benches and Backrests", "sauna-bench.html"),
        ("Sauna Aroma Oils", "sauna-aroma-oils.html"),
        ("Sauna Towels and Linens", "sauna-towels.html"),
        ("Sauna Baskets", "sauna-baskets.html"),
        ("Sauna Timers", "sauna-timer.html"),
        ("Sauna Heater Stones", "sauna-heater-stones.html"),
        ("Sauna Slippers and Sandals", "sauna-slippers.html"),
        ("Sauna Bath Brushes", "sauna-brush.html"),
        ("Sauna Backrests and Headrests", "sauna-backrest.html"),
        ("Sauna Gifts", "sauna-gifts.html"),
        ("Privacy Policy", "privacy-policy.html"),
    ]
    items = "\n".join(f'<li><a href="{rs}">{rt}</a></li>' for rt, rs in links)
    body = f"<h2>All Pages</h2>\n<p>Find every page on Sauna Accessories below.</p>\n<ul>\n<li><a href=\"index.html\">Home</a></li>\n{items}\n</ul>\n"
    return _page_shell(title, desc, "Sitemap", body)


if __name__ == "__main__":
    main()