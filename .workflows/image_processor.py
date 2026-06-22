#!/usr/bin/env python3
import os
import math
import random
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw

TARGET_WIDTH = 1600  # github banner width is 1600px
TARGET_HEIGHT = 400  # github banner height is 400px


def scale_to_cover(img, target_width, target_height):
    """Resizes an image to cover target dimensions while preserving aspect ratio."""
    src_width, src_height = img.size
    scale_w = target_width / src_width
    scale_h = target_height / src_height
    scale = max(scale_w, scale_h)

    new_width = int(round(src_width * scale))
    new_height = int(round(src_height * scale))
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)


def center_crop(img, target_width, target_height):
    """Trims the canvas to the final target banner dimensions."""
    width, height = img.size
    left = (width - target_width) // 2
    top = (height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    return img.crop((left, top, right, bottom))


ASSET_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


def _pick_image(seed):
    """Pick a random image from assets/ using the daily seed."""
    assets_dir = Path("assets")
    candidates = sorted(
        f for f in assets_dir.iterdir() if f.suffix.lower() in ASSET_EXTENSIONS
    )
    if not candidates:
        return None
    rng = random.Random(seed)
    return rng.choice(candidates)


def displace_image(img, seed):
    """
    Applies the displaced dot pattern filter.

    Darker pixels undergo maximum displacement; white pixels remain stationary.
    A daily-rotating angle changes the displacement direction once a day.
    """
    random.seed(seed)

    width, height = img.size

    gray_img = img.convert("L")
    pixels = gray_img.load()

    out_img = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(out_img)

    step_size = 10
    block_size = 8

    angle = random.uniform(0, 2 * math.pi)
    displacement_strength = -120.0

    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    for y in range(0, height, step_size):
        for x in range(0, width, step_size):
            b = pixels[x, y] / 255.0

            offset = displacement_strength * (1.0 - b)

            new_x = (x + cos_a * offset) % width
            new_y = (y + sin_a * offset) % height

            block_color = int(b * 255)
            r = block_size / 2.0
            draw.ellipse([new_x - r, new_y - r, new_x + r, new_y + r], fill=block_color)

    return out_img


def halftone_image(img, seed):
    """
    Converts an image to a retro binary halftone dot pattern.

    Dot size varies with brightness — darker regions produce larger dots,
    lighter regions produce smaller dots (or none). The output is pure
    monochrome (black ink on white paper), giving a classic print halftone
    / newspaper / risograph aesthetic that pairs naturally with ASCII art.
    """
    random.seed(seed)

    width, height = img.size

    gray = img.convert("L")

    # Contrast stretch for punchier halftone separation
    px = list(gray.getdata())
    lo, hi = min(px), max(px)
    if hi > lo:
        gray = gray.point(lambda p: int((p - lo) * 255.0 / (hi - lo)))

    pixels = gray.load()

    out = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(out)

    curve_bias = random.uniform(-0.05, 0.05)
    dot_gain = random.uniform(0.95, 1.05)

    cell_size = 12
    half_cell = cell_size / 2.0

    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            sx = min(x + int(half_cell), width - 1)
            sy = min(y + int(half_cell), height - 1)
            b = pixels[sx, sy] / 255.0

            b = max(0.0, min(1.0, b + curve_bias))
            radius = half_cell * (1.0 - b) * dot_gain

            if radius > 0.4:
                cx = x + half_cell
                cy = y + half_cell
                draw.ellipse(
                    [cx - radius, cy - radius, cx + radius, cy + radius], fill=0
                )

    return out


def main():
    today_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    seed = int(today_str)

    output_dir = Path(".workflows")
    output_image_path = output_dir / "daily_art.png"

    img_path = _pick_image(seed)
    if img_path is None:
        print("Error: No image files found in assets/")
        return

    print(f"Processing {img_path.name} (seed: {seed})...")
    try:
        with Image.open(img_path) as img:
            output_dir.mkdir(exist_ok=True)

            # 1. Rotate portrait → landscape
            if img.height > img.width:
                img = img.rotate(90, expand=True, resample=Image.Resampling.LANCZOS)

            # 2. Scale up for roaming crop room (3x target size)
            img = scale_to_cover(img, TARGET_WIDTH * 3, TARGET_HEIGHT * 3)

            # 3. Apply both filters at full intermediate size
            halftone = halftone_image(img, seed)
            displace = displace_image(img, seed * 31 + 1)

            # 4. Same random crop position for both (seeded daily)
            crop_rng = random.Random(seed)
            cx = crop_rng.randint(0, max(0, halftone.width - TARGET_WIDTH))
            cy = crop_rng.randint(0, max(0, halftone.height - TARGET_HEIGHT))

            def _crop(image):
                return image.crop((cx, cy, cx + TARGET_WIDTH, cy + TARGET_HEIGHT))

            halftone_cropped = _crop(halftone)
            displace_cropped = _crop(displace)

            halftone_cropped.save(output_dir / "daily_art_halftone.png", "PNG")
            displace_cropped.save(output_dir / "daily_art_displace.png", "PNG")

            hour = datetime.now(timezone.utc).hour
            if hour < 12:
                primary = halftone_cropped
                variant = "halftone"
            else:
                primary = displace_cropped
                variant = "displace"

            primary.save(output_image_path, "PNG")
            print(f"Success: {img_path.name} → {variant} crop=({cx},{cy})")
    except Exception as e:
        print(f"Error processing image: {e}")


if __name__ == "__main__":
    main()
