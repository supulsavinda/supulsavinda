"""Local preview, no push needed: draws the static artwork, fills the live cards with sample
numbers, and writes preview/index.html (your README on a GitHub-dark page) next to the repo root.

Usage: python scripts/preview.py   then open preview/index.html
"""
import datetime as dt
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUT = os.path.join(ROOT, 'preview')
sys.path.insert(0, HERE)

import stat_cards as sc  # noqa: E402

subprocess.run([sys.executable, os.path.join(HERE, 'draw_assets.py')], check=True)
os.makedirs(OUT, exist_ok=True)

s = {'joined': dt.date(2025, 4, 8), 'today': dt.date.today(), 'total': 412, 'year': 230, 'prs': 12, 'issues': 3,
     'contributed': 5, 'followers': 0, 'repos': 3, 'stars': 0, 'views': 120, 'current': 4,
     'current_range': (dt.date.today() - dt.timedelta(days=3), dt.date.today()), 'longest': 19,
     'longest_range': (dt.date(2026, 3, 2), dt.date(2026, 3, 20)),
     'langs': [('JavaScript', 935, '#f1e05a'), ('Dockerfile', 321, '#384d54')]}
for name, text in {'stats-player.svg': sc.player(s), 'stats-streak-languages.svg': sc.streak_and_languages(s)}.items():
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(text)

html = open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
html = re.sub(r'https://raw\.githubusercontent\.com/[^/]+/[^/]+/output/((?:stats-[\w-]+|snake)\.svg)', r'\1', html)
html = re.sub(r'src="assets/', 'src="../assets/', html)
subprocess.run([sys.executable, os.path.join(HERE, 'lightcycle.py'), '--sample', os.path.join(OUT, 'snake.svg')], check=True)
html = re.sub(r'https://komarev[^"]*', '', html)
with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
    f.write('<body style="background:#0d1117;margin:0 auto;max-width:900px;padding:24px">' + html + '</body>')
print('open', os.path.join(OUT, 'index.html'))
