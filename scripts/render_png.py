#!/usr/bin/env python3
"""Render an HTML file to a PNG with Playwright Chromium. Usage: python3 -I render_png.py in.html out.png [width height]"""
import sys
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]
w, h = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1600, 900)
import os
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": h})
    pg.goto("file://" + os.path.abspath(src)); pg.wait_for_timeout(400); pg.screenshot(path=out); b.close()
