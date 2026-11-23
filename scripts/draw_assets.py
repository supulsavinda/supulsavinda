"""Draws the README's static artwork into ../../assets/ in the minimal dark theme (theme.py).

Usage: python draw_assets.py
Edit the CONTENT block below, then re-run. Anything marked TODO is a placeholder.
"""
import os

from theme import (BG, ACCENT, DISPLAY, LINE, LINE_STRONG, MARGIN, MONO, ORANGE, SANS, TEXT, TEXT_DIM, TEXT_SOFT, W, _shape, esc,
                   glyph, hairline, heading, logo, panel, split, svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')

# ───────────────────────────── CONTENT ─────────────────────────────
NAME = 'Supul Savinda'
USER = 'supulsavinda'                      # GitHub username, shown top right of the hero
KICKER = 'AI & Data Science Student'
TAGLINE = 'Exploring machine learning, NLP and the computing power behind them.'
LOCATION = 'Sri Lanka'
SCHOOL = 'Robert Gordon University'
TYPED = 'live.life()'                              # the line that types itself in the hero

ABOUT = [  # (glyph, label, text)    two per row; add or remove pairs freely
    ('graduation-cap', 'Studying at RGU', 'BSc (Hons) Artificial Intelligence & Data Science'),
    ('brain-circuit', 'Interested in', 'Machine learning, NLP & computing power'),
    ('code-xml', 'I code in', 'Python, SQL, Java & JavaScript'),
    ('app-window', 'I build interfaces with', 'JavaFX and HTML'),
]

# (file, name, meta line, status, description lines, tags, public)
# Empty for now. Add projects like the example below, then uncomment the Projects
# lines in README.md (one <p> per two cards).
# ('my-project', 'My Project', 'Individual project · 2026', '',
#  ['First line of the description,', 'second line,', 'third line.'], ['Python', 'ML'], True),
PROJECTS = []

STACK = [  # (group, [(icon key, label)])    'ui:...' keys are line icons for tools with no logo
    ('Languages', [('python', 'Python'), ('openjdk', 'Java'), ('javascript', 'JavaScript'), ('ui:database', 'SQL'),
                   ('html5', 'HTML')]),
    ('Frameworks & Tools', [('ui:app-window', 'JavaFX'), ('git', 'Git'), ('github', 'GitHub')]),
]

LINKS = [  # (file, label, icon key or None for the globe, live?)    the URLs are in README.md
    ('linkedin', 'LinkedIn', 'linkedin', True),
    ('email', 'Email', 'gmail', True),
    ('github', 'GitHub', 'github', True),
]
FOOTER = 'Thanks for stopping by. Always up for a chat about ML, NLP and new ideas.'
# ───────────────────────────────────────────────────────────────────


def write(name, text):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def grid_floor(H, horizon=196, vx=760):
    """A perspective grid floor that fades in towards the bottom right, a glowing horizon,
    and one thin amber-yellow light trail that draws itself along the grid."""
    depth = (H - horizon) * 2.2
    def on_ray(k, y):          # x of radial line k at height y
        return vx + k * 150 * (y - horizon) / depth
    lines = [f'<path d="M{vx} {horizon} L{vx + k * 150:.0f} {horizon + depth:.0f}"/>' for k in range(-12, 12)]
    rows = [horizon + (H - horizon) * (i / 8) ** 1.7 for i in range(1, 10)]
    lines += [f'<path d="M0 {y:.1f} H{W}"/>' for y in rows]
    y5, y3 = rows[5], rows[3]
    orange = f'M{W} {y5:.1f} H{on_ray(2, y5):.1f} L{on_ray(2, horizon + 10):.1f} {horizon + 10}'
    cyan = f'M{on_ray(-3, H + 20):.1f} {H + 20} L{on_ray(-3, y3):.1f} {y3:.1f} H{W}'
    return f'''<defs>
<clipPath id="pane"><path d="{_shape(W, H, 18, 0, 0)}"/></clipPath>
<linearGradient id="fadeX" x1="0" x2="1"><stop offset=".38" stop-color="#fff" stop-opacity="0"/><stop offset=".72" stop-color="#fff"/></linearGradient>
<linearGradient id="fadeY" x1="0" x2="0" y1="0" y2="1"><stop offset="{horizon / H:.2f}" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="mx"><rect width="{W}" height="{H}" fill="url(#fadeX)"/></mask>
<mask id="my"><rect width="{W}" height="{H}" fill="url(#fadeY)"/></mask>
<linearGradient id="hzv" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset="1" stop-color="{ACCENT}" stop-opacity=".09"/></linearGradient>
<linearGradient id="hz" x1="0" x2="1"><stop offset=".4" stop-color="{ACCENT}" stop-opacity="0"/><stop offset=".76" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity=".2"/></linearGradient>
</defs>
<g clip-path="url(#pane)"><g mask="url(#mx)">
<g mask="url(#my)" stroke="{TEXT_SOFT}" stroke-opacity=".16" stroke-width="1" fill="none">{''.join(lines)}</g>
<path d="M0 {horizon} H{W}" stroke="url(#hz)" stroke-width="1" stroke-opacity=".6"/>
<path class="trail t1" d="{cyan}" fill="none" stroke="{ACCENT}" stroke-width="1.5" stroke-linejoin="miter" pathLength="100"/>
</g></g>'''


def hero():
    H = 310
    x = 56
    tw = len(TYPED) * 8.45
    body = f'''<defs><clipPath id="typed"><rect class="reveal" x="{x + 20}" y="204" width="0" height="24"/></clipPath></defs>
{panel(W, H, 18)}
{grid_floor(H)}
<text x="{W - 44}" y="50" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{TEXT_DIM}" text-anchor="end">USER <tspan fill="{ACCENT}">//</tspan> {esc(USER.upper())}</text>
<text x="{x}" y="74" font-family="{MONO}" font-size="12" font-weight="600" letter-spacing="2.2" fill="{ACCENT}">{esc(KICKER.upper())}</text>
<text x="{x - 2}" y="136" font-family="{DISPLAY}" font-size="40" font-weight="500" letter-spacing="9" fill="{TEXT}">{esc(NAME.upper())}</text>
<text x="{x}" y="174" font-family="{SANS}" font-size="17" fill="{TEXT_SOFT}">{esc(TAGLINE)}</text>
<text x="{x}" y="221" font-family="{MONO}" font-size="14" fill="{ACCENT}">&gt;</text>
<g clip-path="url(#typed)"><text x="{x + 20}" y="221" font-family="{MONO}" font-size="14" fill="{TEXT}">{esc(TYPED)}</text></g>
<rect class="caret" x="{x + 20 + tw + 4:.0f}" y="209" width="2" height="15" fill="{ACCENT}"/>
{glyph('map-pin', x, 249, 14, TEXT_DIM)}<text x="{x + 21}" y="261" font-family="{SANS}" font-size="13" fill="{TEXT_SOFT}">{esc(LOCATION)}</text>
{glyph('graduation-cap', x + 110, 249, 14, TEXT_DIM)}<text x="{x + 131}" y="261" font-family="{SANS}" font-size="13" fill="{TEXT_SOFT}">{esc(SCHOOL)}</text>'''
    style = f'''
.reveal {{ animation: type 2.6s steps({len(TYPED)}, end) .3s forwards; }}
@keyframes type {{ to {{ width: {tw + 4:.0f}px; }} }}
.caret {{ animation: blink 1.1s steps(1) infinite; }} @keyframes blink {{ 50% {{ opacity: 0; }} }}
.trail {{ stroke-dasharray: 100 100; stroke-dashoffset: 100; animation: ride 6s cubic-bezier(.5, 0, .3, 1) infinite; }}
.t2 {{ animation-delay: 1.4s; }}
@keyframes ride {{ 0% {{ stroke-dashoffset: 100; opacity: 1; }} 55% {{ stroke-dashoffset: 0; opacity: 1; }} 85% {{ stroke-dashoffset: 0; opacity: 1; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ .reveal {{ width: {tw + 4:.0f}px; }} .trail {{ stroke-dashoffset: 0; }} }}
'''
    return svg(W, H, f'{NAME}: {KICKER} at {SCHOOL}, {LOCATION}. {TAGLINE}', body, style)


def about():
    y0, rh = 112, 64
    H = y0 + rh * ((len(ABOUT) + 1) // 2) + 10
    cells = []
    for i, (g, label, text) in enumerate(ABOUT):
        x, y = MARGIN + (i % 2) * 470, y0 + (i // 2) * rh
        if i % 2 == 0:
            cells.append(hairline(MARGIN, W - MARGIN, y))
        cells.append(f'{glyph(g, x, y + 16, 14, ACCENT)}'
                     f'<text x="{x + 22}" y="{y + 27}" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1.4" fill="{TEXT_DIM}">{esc(label.upper())}</text>'
                     f'<text x="{x}" y="{y + 50}" font-family="{SANS}" font-size="16" font-weight="600" fill="{TEXT}">{esc(text)}</text>')
    body = f'{panel(W, H)}{heading("About", "who I am")}{"".join(cells)}'
    return svg(W, H, 'About me: ' + '; '.join(f'{l} {t}' for _, l, t in ABOUT), body)


def section_heading(title, kicker):
    H = 104
    return svg(W, H, title, f'{panel(W, H)}{heading(title, kicker)}')


def project(i, n, title, meta, status, lines, tags, public):
    """A project card. Public repos get an arrow (the card links to the repo); private ones a
    status pill (Ongoing / Private) and a lock instead."""
    cw, H = W / n, 238
    pw, ox = split(n, i)
    x, right = ox + 28, ox + pw - 28
    desc = ''.join(f'<text x="{x}" y="{112 + j * 22}" font-family="{SANS}" font-size="14" fill="{TEXT_SOFT}">{esc(l)}</text>' for j, l in enumerate(lines))
    if public:
        corner = f'<text x="{right}" y="50" font-family="{MONO}" font-size="16" fill="{ACCENT}" text-anchor="end">↗</text>'
    else:
        pill_w = round(30 + len(status) * 7)
        live = status == 'Ongoing'
        corner = (f'<rect x="{right - pill_w + .5}" y="31.5" width="{pill_w - 1}" height="25" rx="12.5" fill="{ACCENT if live else "#fff"}" '
                  f'fill-opacity="{.08 if live else .03}" stroke="{ACCENT if live else LINE_STRONG}" stroke-opacity="{.5 if live else 1}"/>'
                  + (f'<circle class="live" cx="{right - pill_w + 14}" cy="44" r="3" fill="{ACCENT}"/>' if live
                     else glyph('lock', right - pill_w + 9, 38, 11, TEXT_SOFT, 2))
                  + f'<text x="{right - pill_w + 23}" y="48.5" font-family="{MONO}" font-size="11.5" font-weight="600" fill="{ACCENT if live else TEXT_SOFT}">{esc(status)}</text>')
    body = f'''{panel(pw, H, x=ox)}
<text x="{x}" y="50" font-family="{DISPLAY}" font-size="15" font-weight="500" letter-spacing="3" fill="{TEXT}">{esc(title.upper())}</text>{corner}
<text x="{x}" y="74" font-family="{MONO}" font-size="12" fill="{ACCENT}">{esc(meta)}</text>
{desc}{hairline(x, right, 186)}
<text x="{x}" y="214" font-family="{MONO}" font-size="12" fill="{TEXT_DIM}">{esc("  ·  ".join(tags))}</text>'''
    style = '.live { animation: live 2s ease-in-out infinite; } @keyframes live { 50% { opacity: .25; } }'
    return svg(f'{cw:g}', H, f'{title} ({meta}{", " + status if status else ""}): {" ".join(lines)} {", ".join(tags)}.', body, style)


def stack():
    """The toolbox as loose tiles (no panel behind them): a centred title plate, then each group
    under a small label with dotted rules either side, its tiles centred in a row."""
    tw, th, gap = 112, 100, 12
    pw = 220
    px = (W - pw) / 2
    out = [panel(pw, 80, x=px),
           f'<text x="{W / 2}" y="31" font-family="{MONO}" font-size="11.5" font-weight="600" letter-spacing="2" fill="{ACCENT}" text-anchor="middle">TECH STACK</text>'
           f'<text x="{W / 2}" y="61" font-family="{DISPLAY}" font-size="18" font-weight="500" letter-spacing="5" fill="{TEXT}" text-anchor="middle">TOOLBOX</text>']
    y, n = 108, 0
    for group, items in STACK:
        cw = round(40 + len(group) * 7.2)
        cx = (W - cw) / 2
        out.append(f'<path d="M0 {y + 14} H{cx - 14:.0f} M{cx + cw + 14:.0f} {y + 14} H{W}" stroke="{LINE}" stroke-width="1"/>'
                   f'{panel(cw, 28, 14, x=cx, y=y)}<circle cx="{cx + 16:.1f}" cy="{y + 14}" r="3" fill="{ACCENT}"/>'
                   f'<text x="{cx + 27:.1f}" y="{y + 18}" font-family="{MONO}" font-size="11.5" font-weight="600" letter-spacing=".4" fill="{TEXT_SOFT}">{esc(group)}</text>')
        y += 44
        x0 = (W - (len(items) * tw + (len(items) - 1) * gap)) / 2
        for i, (key, label) in enumerate(items):
            x = x0 + i * (tw + gap)
            out.append(f'''<g transform="translate({x:.1f} {y})">{panel(tw, th, 14)}
<g class="item" style="animation-delay:{-n * .37:.2f}s">{logo(key, tw / 2 - 13, 24, 26, TEXT_SOFT)}</g>
<text x="{tw / 2}" y="86" font-family="{SANS}" font-size="12.5" font-weight="600" fill="{TEXT}" text-anchor="middle">{esc(label)}</text></g>''')
            n += 1
        y += th + 26
    H = y - 26
    style = '.item { animation: hover 3.6s ease-in-out infinite; } @keyframes hover { 50% { transform: translateY(-3px); } }'
    return svg(W, H, 'My toolbox. ' + ' '.join(f'{g}: {", ".join(l for _, l in it)}.' for g, it in STACK), ''.join(out), style)


def button(i, n, label, key, live=True):
    """A link button; one that isn't live yet is drawn dimmed, with a dashed border."""
    cw, H = W / n, 56
    pw, ox = split(n, i)
    content = 16 + 14 + len(label) * 11.6
    x = ox + (pw - content) / 2
    ink = TEXT if live else TEXT_DIM
    icon = logo(key, f'{x:.1f}', 20, 16, TEXT_SOFT if live else ink) if key else glyph('globe', f'{x:.1f}', 19, 18, ink)
    frame = panel(pw, H, 12, x=ox) if live else (
        f'<rect x="{ox + .5}" y=".5" width="{pw - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{LINE_STRONG}" stroke-dasharray="4 4"/>')
    body = (f'{frame}{icon}'
            f'<text x="{x + 30:.1f}" y="33" font-family="{DISPLAY}" font-size="11.5" font-weight="500" letter-spacing="3.5" fill="{ink}">{esc(label.upper())}</text>')
    return svg(f'{cw:g}', H, label, body)


def footer():
    H = 72
    body = (f'{panel(W, H)}<circle cx="{W / 2 - len(FOOTER) * 3.7 - 16:.0f}" cy="36" r="2.5" fill="{ACCENT}"/>'
            f'<text x="{W / 2}" y="41" font-family="{SANS}" font-size="15" fill="{TEXT_SOFT}" text-anchor="middle">{esc(FOOTER)}</text>')
    return svg(W, H, FOOTER, body)


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith('.svg'):
            os.remove(os.path.join(OUT, f))
    write('hero.svg', hero())
    write('about.svg', about())
    if PROJECTS:
        write('projects.svg', section_heading('Projects', 'what I build'))
    for i, (f, *card) in enumerate(PROJECTS):
        write(f'project-{f}.svg', project(i % 2, 2, *card))     # two to a row
    write('stack.svg', stack())
    for i, (f, label, key, live) in enumerate(LINKS):
        write(f'btn-{f}.svg', button(i, len(LINKS), label, key, live))
    write('footer.svg', footer())
    print('wrote', len(os.listdir(OUT)), 'files to', os.path.abspath(OUT))


if __name__ == '__main__':
    main()
