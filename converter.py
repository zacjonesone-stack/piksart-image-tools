#!/usr/bin/env python3
"""
Image to Black & White Converter
--------------------------------
Simple script to convert an image to:
 - grayscale (shades of gray)
 - bw (pure black & white using a threshold)

Usage:
  python converter.py input.jpg
  python converter.py input.jpg output.png --mode bw --threshold 120

Dependencies:
  pip install pillow
"""
import os
import sys
import argparse
from PIL import Image

def make_output_path(inp, mode):
    base, ext = os.path.splitext(inp)
    suffix = '_bw' if mode == 'bw' else '_grayscale'
    return base + suffix + ext

def convert_image(input_path, output_path, mode='grayscale', threshold=128):
    img = Image.open(input_path)
    if mode == 'grayscale':
        gray = img.convert('L')  # 'L' = 8-bit grayscale
        gray.save(output_path)
    else:
        # Convert to grayscale then apply threshold -> pure black & white
        gray = img.convert('L')
        # point() maps each pixel p to 255 if p>threshold else 0
        bw = gray.point(lambda p: 255 if p > threshold else 0, mode='1')
        bw.save(output_path)
    print(f"[OK] Saved: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Convert image to grayscale or black & white.')
    parser.add_argument('input', help='Input image file path (jpg/png/gif/...)')
    parser.add_argument('output', nargs='?', help='Optional output path (e.g. out.png)')
    parser.add_argument('--mode', choices=['grayscale','bw'], default='grayscale',
                        help='grayscale (default) or bw (binary black & white)')
    parser.add_argument('--threshold', type=int, default=128,
                        help='Threshold 0-255 used only in bw mode (default 128)')
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"[ERROR] Input file not found: {args.input}")
        sys.exit(1)

    out = args.output or make_output_path(args.input, args.mode)
    try:
        convert_image(args.input, out, mode=args.mode, threshold=args.threshold)
    except Exception as e:
        print("[ERROR] Conversion failed:", str(e))
        sys.exit(1)

if __name__ == '__main__':
    main()
