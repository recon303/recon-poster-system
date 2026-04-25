#!/usr/bin/env python3
"""
RECON Poster System — Image Generation Script
Generates the 10 new hero images using Google Gemini Imagen (Nano Banana API).

Usage:
    export GOOGLE_API_KEY=your_key_here
    python3 generate_images.py

    # Or pass key directly:
    python3 generate_images.py --key YOUR_API_KEY

    # Generate a single poster:
    python3 generate_images.py --vol 08

Get your API key at: https://aistudio.google.com/app/apikey
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import urllib.error
import base64
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"

PROMPTS = {
    "vol08": {
        "file": "hero-vol08-form.jpg",
        "label": "VOL.08 — HOLD THE FORM",
        "prompt": (
            "Athletic male powerlifter at the locked-out top of a single-arm overhead press, "
            "heavy kettlebell extended fully above head, chalk dust exploding from hand, "
            "perfect vertical arm alignment, veins visible on forearm, dark industrial gym, "
            "single hard key light from the left casting dramatic shadows across torso, "
            "deep shadows everywhere else, near-black background, compression shorts and "
            "fitted tank, sweat on skin, ultra high contrast, cinematic fitness editorial "
            "photography, portrait orientation 4:5, photorealistic"
        ),
    },
    "vol09": {
        "file": "hero-vol09-edge.jpg",
        "label": "VOL.09 — FIND THE EDGE",
        "prompt": (
            "Mountain biker riding along a razor-thin alpine ridgeline, drop-off into valley "
            "on both sides, dramatic storm clouds building behind rider, golden hour rim light "
            "from behind creating a halo around rider and bike, rider leaning slightly into "
            "a technical section, full downhill helmet and pads, distant valley 3000 feet "
            "below, tiny against the vast mountain landscape, high contrast alpine light, "
            "rich shadows in the rock face, cinematic adventure photography, portrait 4:5, "
            "photorealistic"
        ),
    },
    "vol10": {
        "file": "hero-vol10-base.jpg",
        "label": "VOL.10 — BUILD THE BASE",
        "prompt": (
            "Female sprinter in starting blocks on a rubberized track, stadium empty and dark, "
            "powerful stadium lights from directly above casting a single cone of light on the "
            "athlete, everything else in near-darkness, athlete coiled low in set position, "
            "head down, compression kit and spikes, focused pre-race intensity, chalk on "
            "fingers, the block mechanism close and detailed, dramatic theatrical lighting, "
            "extreme high contrast, cinematic sports photography, portrait 4:5, photorealistic"
        ),
    },
    "vol11": {
        "file": "hero-vol11-pace.jpg",
        "label": "VOL.11 — PUSH THE PACE",
        "prompt": (
            "Male sprinter captured mid-stride at full speed, low camera angle at track level, "
            "side profile showing perfect arm and leg mechanics, one foot driving into the "
            "track surface, opposite knee at maximum drive height, stadium lights creating "
            "rim light along the body edge, dark track surface and blurred background, "
            "compression singlet and spikes, motion freeze at 1/8000s, chalk and track "
            "rubber dust in air, ultra high contrast cinematic athletics photography, "
            "portrait 4:5, photorealistic"
        ),
    },
    "vol12": {
        "file": "hero-vol12-drop.jpg",
        "label": "VOL.12 — TRUST THE DROP",
        "prompt": (
            "Mountain biker fully committed in the air off a steep rock drop in a dense "
            "Pacific Northwest forest, rider and bike perfectly horizontal mid-flight, "
            "dappled late-afternoon light breaking through dark tree canopy creating "
            "spotlight on rider, deep forest shadow everywhere else, full protective gear "
            "including full face helmet, bike wheel at exact horizontal, rider completely "
            "calm and in control, dark mossy rock context below, high contrast forest "
            "action photography, portrait 4:5, photorealistic"
        ),
    },
    "vol13": {
        "file": "hero-vol13-reps.jpg",
        "label": "VOL.13 — FORGE THE REPS",
        "prompt": (
            "Muscular athlete at the peak of a two-hand heavy kettlebell swing, 32kg bell "
            "floating at chest height, arms fully extended forward, chalk dust cloud around "
            "both hands, explosive hip hinge expression, dark industrial gym with concrete "
            "walls, two industrial pendant lights behind creating warm backlight silhouette, "
            "chalk and sweat mist suspended in air, grimace of controlled effort on face, "
            "worn leather belt, near-black background, gritty editorial fitness photography, "
            "portrait 4:5, photorealistic"
        ),
    },
    "vol14": {
        "file": "hero-vol14-moment.jpg",
        "label": "VOL.14 — CLAIM THE MOMENT",
        "prompt": (
            "Female sprinter breaking through the finish line tape at full speed, arms flung "
            "wide in triumph, chest first through the tape, paper tape streaming behind both "
            "arms, roaring stadium crowd blurred beyond, multiple overhead stadium lights "
            "creating dramatic theatrical illumination, camera at low side angle, "
            "compression kit with race number, face showing raw euphoria, ultra high contrast, "
            "peak moment sports photography, portrait 4:5, photorealistic"
        ),
    },
    "vol15": {
        "file": "hero-vol15-grade.jpg",
        "label": "VOL.15 — RISE THE GRADE",
        "prompt": (
            "Mountain biker grinding up a steep 20% dirt grade in the Colorado Rockies, "
            "rider standing on pedals at maximum climbing effort, rear wheel throwing a roost "
            "of dirt and dust, dramatic clear blue sky with a single dramatic cloud formation "
            "above, alpine meadow dropping away behind and below showing massive elevation, "
            "rider tiny against the massive landscape, midday harsh sunlight, deep blue sky "
            "contrast, cinematic landscape fitness photography, portrait 4:5, photorealistic"
        ),
    },
    "vol16": {
        "file": "hero-vol16-tempo.jpg",
        "label": "VOL.16 — KEEP THE TEMPO",
        "prompt": (
            "Sprinter in perfect mid-stride tempo run on a track at sunset, warm golden "
            "hour light raking across from the side creating a long shadow that stretches "
            "across three lane lines, athlete at comfortable but powerful sustained pace, "
            "arms and legs in perfect synchronized form, compression kit glowing amber in "
            "the light, dark track surface, sky transitioning from orange to deep blue "
            "overhead, cinematic long-lens athletics photography, portrait 4:5, photorealistic"
        ),
    },
    "vol17": {
        "file": "hero-vol17-system.jpg",
        "label": "VOL.17 — WORK THE SYSTEM",
        "prompt": (
            "Athlete in the final locked-out position of a Turkish get-up, single 48kg "
            "kettlebell pressed overhead in one arm, arm trembling with effort, lying "
            "partially on dark gym floor, single overhead theatrical spotlight creating "
            "a circle of light on the athlete with everything else in complete darkness, "
            "sweat running down arm and face, absolute focus in eyes, the weight of the "
            "system visible in every muscle fiber, gritty dark athletic photography, "
            "cinematic, portrait 4:5, photorealistic"
        ),
    },
}


def generate_image(api_key: str, prompt: str, output_path: Path) -> bool:
    """Call Gemini Imagen API and save the result."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"imagen-4.0-generate-001:predict?key={api_key}"
    )
    payload = json.dumps({
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "3:4",
            "safetyFilterLevel": "block_only_high",
            "personGeneration": "allow_adult",
        },
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ERROR {e.code}: {body[:300]}")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

    predictions = data.get("predictions", [])
    if not predictions:
        print("  ERROR: no predictions returned")
        return False

    img_b64 = predictions[0].get("bytesBase64Encoded", "")
    if not img_b64:
        print("  ERROR: no image data in response")
        return False

    img_bytes = base64.b64decode(img_b64)
    output_path.write_bytes(img_bytes)
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate RECON poster hero images")
    parser.add_argument("--key", help="Google AI Studio API key (or set GOOGLE_API_KEY env var)")
    parser.add_argument("--vol", help="Generate only this volume (e.g. 08, 09, ..., 17)")
    parser.add_argument("--list", action="store_true", help="List all volumes and exit")
    args = parser.parse_args()

    if args.list:
        for vol_id, info in PROMPTS.items():
            status = "EXISTS" if (ASSETS_DIR / info["file"]).exists() else "missing"
            print(f"  {info['label']:35s} [{status}]  {info['file']}")
        return

    api_key = args.key or os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        print("ERROR: No API key. Set GOOGLE_API_KEY env var or pass --key YOUR_KEY")
        print("Get a free key at: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    targets = PROMPTS
    if args.vol:
        key = f"vol{args.vol.zfill(2)}"
        if key not in PROMPTS:
            print(f"Unknown volume: {args.vol}. Valid: 08-17")
            sys.exit(1)
        targets = {key: PROMPTS[key]}

    total = len(targets)
    for i, (vol_id, info) in enumerate(targets.items(), 1):
        out_path = ASSETS_DIR / info["file"]
        if out_path.exists():
            print(f"[{i}/{total}] SKIP {info['label']} (file exists)")
            continue

        print(f"[{i}/{total}] Generating {info['label']} ...")
        ok = generate_image(api_key, info["prompt"], out_path)
        if ok:
            kb = out_path.stat().st_size // 1024
            print(f"  Saved → {info['file']} ({kb} KB)")
        else:
            print(f"  FAILED — check error above")

        if i < total:
            time.sleep(1.5)  # rate limit courtesy pause

    print("\nDone. Run build_posters.py to generate the final HTML files.")


if __name__ == "__main__":
    main()
