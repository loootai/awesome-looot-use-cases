#!/usr/bin/env python3
"""Write calculator.html: fills scripts/calculator_template.html with data/catalog-prices-<date>.json (every endpoint id, provider, price, unit)."""
import json, glob
C = json.load(open(sorted(glob.glob("data/catalog-prices-*.json"))[-1]))
open("calculator.html", "w").write(open("scripts/calculator_template.html").read().replace("/*DATA*/null", json.dumps(C, separators=(",", ":"))))
