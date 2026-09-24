#!/usr/bin/env python3
"""Generate 6 x 1280x720 sauna-accessories images via xAI Imagine (grok-imagine-image, 1k),
download results, and optimize to .avif in the tier-2 img folder.
Modest quality on purpose — these are accent images for a topical-authority tier-2 site."""
import json
import os
import time
import urllib.request
from pathlib import Path

PROFILE_ENV = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "profiles" / "dev" / ".env"
OUT_DIR = Path(r"C:\Users\porne\Documents\Marskibrain\projects\saunazilla\cloud-stacks\sauna-accessories-tier-2\img")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def get_key():
    if os.environ.get("XAI_API_KEY", "").startswith("xai-"):
        return os.environ["XAI_API_KEY"]
    for line in PROFILE_ENV.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.strip().startswith("XAI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("XAI_API_KEY not found in profile .env")


KEY = get_key()

# filename (no ext) -> prompt. Topics fit a "sauna accessories" tier-2 site.
IMAGES = {
    "sauna-accessories-bucket-ladle": (
        "A traditional wooden Finnish sauna bucket and ladle resting on a warm sauna "
        "bench, faint steam rising, warm golden ambient light, rustic Nordic sauna "
        "interior, premium lifestyle product photography, horizontal 1280x720. "
        "No people, no text, no watermark."
    ),
    "sauna-accessories-whisk-vasta": (
        "A fresh birch sauna whisk (vasta / vihta) tied with twine lying on a wooden "
        "sauna bench beside a small wooden bucket, soft green leaves, warm natural "
        "light, authentic Finnish sauna accessory, lifestyle photography, horizontal "
        "1280x720. No people, no text."
    ),
    "sauna-accessories-towel-aroma": (
        "Neatly folded white towels and a small bottle of eucalyptus aroma oil on a warm "
        "wooden sauna bench, soft steam and candlelight, spa-like relaxation ambiance, "
        "muted natural tones, lifestyle product photography, horizontal 1280x720. "
        "No people, no text."
    ),
    "sauna-accessories-lighting": (
        "Cozy moody sauna interior with warm candlelight and a dim soft lamp illuminating "
        "dark wooden walls, textured shadows, tranquil spa ambiance, premium wellness "
        "photography, horizontal 1280x720. No people, no text."
    ),
    "sauna-accessories-thermometer-hat": (
        "A felt sauna hat and an analog wooden sauna thermometer resting on a warm wooden "
        "sauna bench, soft warm light, rustic Nordic sauna interior, lifestyle product "
        "photography, horizontal 1280x720. No people, no text."
    ),
    "sauna-accessories-heater-stones": (
        "Glowing sauna stones on a wood-burning sauna heater with a ladle resting on the "
        "stone guard, warm ember light, wooden walls, inviting cozy warmth, close-up "
        "lifestyle photography, horizontal 1280x720. No people, no text."
    ),
}

URL = "https://api.x.ai/v1/images/generations"


def generate(prompt):
    payload = {
        "model": "grok-imagine-image",
        "prompt": prompt,
        "n": 1,
        # No size field: default output is 1280x720. Modest quality, keep tokens low.
        "response_format": "url",
    }
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=240) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-tier2"})
    with urllib.request.urlopen(req, timeout=240) as resp, open(dest, "wb") as f:
        f.write(resp.read())


def to_avif(src, dest):
    try:
        import PIL.Image
        im = PIL.Image.open(src).convert("RGB")
        if im.width > 1360:
            h = int(im.height * 1360 / im.width)
            im = im.resize((1360, h), PIL.Image.LANCZOS)
        im.save(dest, "AVIF", quality=52)
        return True
    except Exception as e:
        print(f"  avif conversion failed ({e}); leaving source")
        return False


def main():
    results = {}
    for name, prompt in IMAGES.items():
        src = OUT_DIR / f"{name}.tmp.jpg"
        avif = OUT_DIR / f"{name}.avif"
        if avif.exists():
            print(f"[skip] {name}.avif already present")
            results[name] = "cached"
            continue
        print(f"[gen ] {name} ...", flush=True)
        for attempt in range(3):
            try:
                data = generate(prompt)
                if "error" in data:
                    raise RuntimeError(data["error"])
                url = data["data"][0]["url"]
                download(url, src)
                break
            except Exception as e:
                print(f"  attempt {attempt+1} failed: {e}")
                if attempt == 2:
                    results[name] = f"ERROR: {e}"
                    continue
                time.sleep(5)
        else:
            results[name] = "ERROR"
            continue
        if to_avif(src, avif):
            results[name] = "ok"
            src.unlink(missing_ok=True)
        else:
            jpg = OUT_DIR / f"{name}.jpg"
            src.replace(jpg)
            results[name] = "ok-jpg"
        print(f"  -> {avif.name} ({avif.stat().st_size} bytes)", flush=True)
    print("\n=== SUMMARY ===")
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()