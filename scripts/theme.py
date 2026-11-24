"""Shared look for the profile README artwork (draw_assets.py) and the live stat
cards (stat_cards.py): a quiet, minimal grid theme. Near-black panels with hairline
borders and softly cut corners, one amber-yellow accent, and the Orbitron display font in a
light weight with wide spacing (SIL Open Font License, fonts/OFL-LICENSE.txt).

Everything is inlined (icons and font included): GitHub shows these files as
images, and an SVG loaded as an image can't fetch anything.
"""
import base64
import os
import re
from html import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, 'icons')

DISPLAY = "'Orbitron', 'Eurostile', 'Bank Gothic', 'Segoe UI', sans-serif"
SANS = "'Inter', 'SF Pro Display', 'Segoe UI Variable Display', 'Segoe UI', system-ui, -apple-system, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'Cascadia Mono', 'JetBrains Mono', Consolas, 'Liberation Mono', monospace"

BG = '#0b0b0a'          # panel surface
LINE = '#1f1e1a'        # dim grid lines and tracks
LINE_STRONG = '#36332b'

ACCENT = '#F5D41E'      # the one accent: Tron: Legacy yellow (sampled from the film) (change this one line to recolour everything)
ORANGE = '#F5D41E'      # second light (kept the same gold, for a single-accent look)

TEXT = '#f2efe8'
TEXT_SOFT = '#a39e93'
TEXT_DIM = '#6b675f'

W = 1000                # every full-width block is drawn 1000 wide
GAP = 12                # gap between blocks that sit side by side
MARGIN = 40             # inner margin of a full-width panel

REDUCED = '@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; } }'

with open(os.path.join(HERE, 'fonts', 'orbitron-500.woff2'), 'rb') as _f:
    FONT_FACE = ("@font-face { font-family: 'Orbitron'; font-weight: 400 900; "
                 f"src: url(data:font/woff2;base64,{base64.b64encode(_f.read()).decode()}) format('woff2'); }}")

DEFS = '''<defs>
<filter id="glow"><feMerge><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft"><feMerge><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''  # glow is switched off for the minimal look; give these a blur again to bring it back


def svg(w, h, label, body, style=''):
    font = FONT_FACE if 'Orbitron' in body else ''
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(label)}">\n<title>{esc(label)}</title>\n'
        f'<style>{font}{style}\n{REDUCED}</style>\n{DEFS}\n{body}\n</svg>\n'
    )


def _shape(w, h, c, x, y):
    """Outline with the top-left and bottom-right corners cut at 45 degrees."""
    x0, y0, x1, y1 = x + 1.5, y + 1.5, x + w - 1.5, y + h - 1.5
    return f'M{x0 + c:g} {y0:g} H{x1:g} V{y1 - c:g} L{x1 - c:g} {y1:g} H{x0:g} V{y0 + c:g} Z'


def panel(w, h, rx=16, x=0, y=0):
    """A dark panel with a hairline border and two softly cut corners."""
    c = max(5, min(rx, 14)) * .7
    return f'<path d="{_shape(w, h, c, x, y)}" fill="{BG}" stroke="{LINE_STRONG}" stroke-width="1"/>'


def hairline(x1, x2, y):
    return f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="1" fill="{LINE_STRONG}" fill-opacity=".7"/>'


def heading(text, kicker, x=MARGIN, y=46):
    """Section heading: a small mono kicker in the accent colour above a widely spaced display title."""
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="11.5" font-weight="600" letter-spacing="2" fill="{ACCENT}">{esc(kicker.upper())}</text>'
            f'<text x="{x}" y="{y + 34}" font-family="{DISPLAY}" font-size="19" font-weight="500" letter-spacing="4" fill="{TEXT}">{esc(text.upper())}</text>')


def split(n, i, total=W, gap=GAP):
    """For n blocks shown side by side as n equal images: the width of each block and
    where block i starts inside its own image, so the gaps between blocks come out equal."""
    w = (total - gap * (n - 1)) / n
    return w, i * (w + gap) - i * total / n


def _read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def logo(key, x, y, size, color=TEXT_SOFT):
    """A single-colour tool logo (Simple Icons, icons/) at (x, y). A key starting 'ui:'
    draws a Lucide line icon instead, for tools that have no logo (SQL, JavaFX)."""
    if key.startswith('ui:'):
        return glyph(key[3:], x, y, size, color)
    src = _read(os.path.join(ICONS, f'{key}.svg'))
    inner = re.sub(r'^.*?<svg[^>]*>|</svg>\s*$', '', src, flags=re.S).replace('currentColor', color)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}">{inner}</svg>'


def glyph(name, x, y, size, color, width=1.75):
    """A Lucide line icon (icons/ui/) in one colour."""
    src = _read(os.path.join(ICONS, 'ui', f'{name}.svg'))
    inner = re.sub(r'^.*?<svg[^>]*>|</svg>\s*$', '', src, flags=re.S)
    inner = inner.replace('currentColor', color).replace('stroke-width="2"', f'stroke-width="{width}"')
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24" overflow="visible">{inner}</svg>'
