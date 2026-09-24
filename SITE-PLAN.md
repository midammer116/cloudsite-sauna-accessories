# Sauna Accessories – Tier-2 Cloud-Stack Site Plan

Reference design: https://saunalife.com/products/ (premium Nordic sauna retail mood)
- Fonts: Syne (display/h1-h4), Mulish (body)
- Palette: warm off-white bg, deep navy ink #31384F, sage-green accent #AFCF7B,
  warm timber accent, deep teal-navy footer #2E3A43
- Layout: clean hero + main-with-sidebar (social embed) + plain-footer link grid
  (NO mother-brand Saunazilla social icons — tier-2 rule)

## Tier / linking rules (from cloud-stack workflow)
- Tier-2 site. Tier-1 target (NOT the money site): https://sauna-lifestyle-ls7g3.ondigitalocean.app/
- Exact anchor text fixed by user: **sauna lifestyle**
- Tier-1 link is a plain inline `<a>` in body text, placed high on the homepage
  intro (SEO boost). One inline body link per content page pointing at the tier-1
  homepage. NOT in header/footer/CTAs. Tier-1 domain absent from header, footer,
  privacy, sitemap.
- Do NOT auto-deploy — build for user review first, then deploy to Render.

## Media pools
- Videos (pick 1 random per page): edIPy58vREQ, rTBaHoV5rQo, Fm5MxRaRrLs, UAsdvH0yrcw
- Social sidebar embeds (pick 1 random per page):
  X: platform.twitter.com/embed/Tweet.html?id=2099398319445299577 |
     2097252883825660215 | 2095429689800048736
  Pinterest: https://fi.pinterest.com/pin/<id>/embed/  (924645367275139988 |
     924645367275140150 | 924645367271490187)
- Images: 6 horizontal 1280x720 generated via xAI Imagine (grok-imagine-image,
  '1k' = 1280x720), optimized to .avif quality 52, one random per page.

## Pages (19 total)

1. **index.html** — "Sauna Accessories – Everything You Need for the Perfect Session"
   H1: Sauna Accessories · category: Guides & Buying
   H2: Browse Every Essential; How to Choose the Right Accessories; Start Your
   Collection Today (homepage tier-1 link high in intro body)
2. **essential-sauna-accessories.html** — "Essential Sauna Accessories – The Complete Starting Set"
   H1: Essential Sauna Accessories; H2: The Floor-Starter Set; What Each Essential
   Does; Building Your Kit Over Time; H3 per item
3. **sauna-bucket-and-ladle.html** — "Sauna Buckets and Ladles – The Heart of Löyly"
   H1: Sauna Buckets and Ladles; H2: Why Wood Wins; Choosing Your Size; Care and
   Seasoning
4. **sauna-whisk.html** — "Sauna Whisk (Vasta / Vihta) – Tradition and Ritual"
   H1: The Sauna Whisk; H2: What a Vasta Is; How to Prep and Store; The Ritual
5. **sauna-hat.html** — "Felt Sauna Hat – Protect Your Head in Style"
   H1: The Felt Sauna Hat; H2: Why a Hat Helps; Wool vs Felt; Fit and Care
6. **sauna-thermometer.html** — "Sauna Thermometer – Read the Heat Right"
   H1: Sauna Thermometers; H2: Why Precise Heat Matters; Mounting Best Practice;
   Digital vs Analog
7. **sauna-lighting.html** — "Sauna Lighting – Set the Mood With Warm Light"
   H1: Sauna Lighting; H2: Warm vs Bright; Placement and Safety; Candles and Ambience
8. **sauna-bench.html** — "Sauna Benches and Backrests – Comfort in the Heat"
   H1: Sauna Benches and Backrests; H2: Height and Layering; Materials; Backrests
   and Cushions
9. **sauna-aroma-oils.html** — "Sauna Aroma Oils – Scents for a Calmer Session"
   H1: Sauna Aroma Oils; H2: How Aroma Is Released (löyly water); Best Scents;
   Safe Use
10. **sauna-towels.html** — "Sauna Towels and Linens – Stay Dry, Stay Comfortable"
    H1: Sauna Towels and Linens; H2: The Right Towel; Robes and Sit-On Cloths;
    Care and Rotation
11. **sauna-baskets.html** — "Sauna Baskets – Organize Your Accessories"
    H1: Sauna Baskets; H2: What to Store; Materials That Last; Placement Ideas
12. **sauna-timer.html** — "Sauna Timer – Time Your Session Without Checking Your Phone"
    H1: Sauna Timers; H2: Analog Timers and Hourglasses; Placement; Session Length
13. **sauna-heater-stones.html** — "Sauna Stones – Choose and Care for Your Heater Rocks"
    H1: Sauna Heater Stones; H2: What Good Stones Do; Choosing the Right Rocks;
    Arranging and Replacing
14. **sauna-slippers.html** — "Sauna Slippers and Sandals – Simple Comfort"
    H1: Sauna Slippers and Sandals; H2: Why Footwear Helps; Materials; Care
15. **sauna-brush.html** — "Sauna Bath Brushes – Cleanse and Massage"
    H1: Sauna Bath Brushes; H2: Dry vs Wet Brushing; Felt and Fibre Choices;
    Cleansing Ritual
16. **sauna-backrest.html** — "Sauna Backrests and Headrests – Posture in the Heat"
    H1: Sauna Backrests and Headrests; H2: Supporting Your Back; Headrest Options;
    Materials and Fit
17. **sauna-gifts.html** — "Sauna Gifts – Thoughtful Presents for Sauna Lovers"
    H1: Sauna Gifts; H2: Gift Ideas by Budget; Personalising a Kit; Wrapping the Ritual
18. **privacy-policy.html** — "Privacy Policy"
19. **sitemap.html** — "Sitemap"

## File layout (work folder)
- index.html, 16 content .html, privacy-policy.html, sitemap.html
- components/header.html, components/footer.html (plain link grid, no social icons)
- assets/css/style.css, assets/js/include.js
- img/*.avif (6 images)
- generate-pages.py (generator), gen_images.py (xAI image API)