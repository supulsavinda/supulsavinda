"""Draws the last year of contributions as a grid, with a light cycle riding the lanes
between the squares: a bright head, a fading light trail behind it, and the squares it
passes flashing as it goes. Replaces the contribution snake; same width and theme.
Run by .github/workflows/profile-assets.yml.

Usage: GITHUB_TOKEN=... python lightcycle.py <github-user> <out.svg>
       python lightcycle.py --sample <out.svg>      (made-up data, for previews)
"""
import datetime as dt
import random
import sys

from theme import ACCENT, BG, LINE, MONO, TEXT_DIM, W, svg

CAL_QUERY = '''query($login: String!) { user(login: $login) { contributionsCollection {
  contributionCalendar { weeks { contributionDays { date contributionCount weekday } } }
} } }'''

PITCH, CELL = 18.6, 13          # square spacing and size
X0, Y0 = 12, 12                 # grid origin inside the image
SPEED = 260                     # px per second
TRAIL = 230                     # length of the light trail, px
# Square colours: empty, then four levels from dim to full accent.
LEVELS = ['#161512', '#4a3a0c', '#8a6a00', '#cc9800', ACCENT]


def fetch(login):
    from stat_cards import gql
    weeks = gql(CAL_QUERY, login=login)['user']['contributionsCollection']['contributionCalendar']['weeks']
    return [[(d['weekday'], d['contributionCount']) for d in w['contributionDays']] for w in weeks]


def sample():
    rnd = random.Random(7)
    return [[(d, rnd.choice([0, 0, 0, 1, 2, 3, 5, 8])) for d in range(7)] for _ in range(53)]


def levels(weeks):
    counts = sorted(n for w in weeks for _, n in w if n)
    if not counts:
        return lambda n: 0
    q = [counts[int(len(counts) * f)] for f in (.25, .5, .75)]
    return lambda n: 0 if n == 0 else 1 + sum(n > t for t in q)


def lane_y(i):                  # horizontal lane i runs above row i (0..7)
    return Y0 + i * PITCH - (PITCH - CELL) / 2


def col_x(j):                   # vertical lane j runs left of column j (0..n)
    return X0 + j * PITCH - (PITCH - CELL) / 2


def route(n_cols):
    """A Tron-style ride: long straight runs along the lanes with sharp 90-degree turns,
    out left to right and back again."""
    rnd = random.Random(2010)
    pts, lane = [(col_x(0) - 30, lane_y(3))], 3
    for direction in (1, -1):
        cols = list(range(0, n_cols + 1)) if direction == 1 else list(range(n_cols, -1, -1))
        j = 0
        while j < len(cols) - 1:
            run = rnd.randint(6, 13)
            j = min(j + run, len(cols) - 1)
            x = col_x(cols[j])
            pts.append((x, lane_y(lane)))
            if j < len(cols) - 1:
                lane = min(7, max(0, lane + rnd.choice([-3, -2, 2, 3])))
                pts.append((x, lane_y(lane)))
        if direction == 1:          # turn round at the right edge
            lane = 6 if lane < 4 else 1
            pts.append((pts[-1][0], lane_y(lane)))
    pts.append((pts[-1][0] - 30, pts[-1][1]))
    return pts


def draw(weeks):
    n = len(weeks)
    level = levels(weeks)
    pts = route(n)
    seglens = [abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total = sum(seglens)
    dur = total / SPEED
    loop = dur + 1.5                 # a short pause before the next lap

    # When the head passes along each square's edge: the time it is level with the square's middle.
    flash = {}
    s = 0
    for (a, b), ln in zip(zip(pts, pts[1:]), seglens):
        if a[1] == b[1]:             # horizontal run along lane between rows r-1 and r
            r = round((a[1] - Y0 + (PITCH - CELL) / 2) / PITCH)
            for j in range(n):
                cx = X0 + j * PITCH + CELL / 2
                lo, hi = sorted((a[0], b[0]))
                if lo <= cx <= hi:
                    t = (s + abs(cx - a[0])) / SPEED
                    for row in (r - 1, r):
                        if 0 <= row < 7:
                            flash.setdefault((j, row), t)
        s += ln

    cells = []
    for j, week in enumerate(weeks):
        for weekday, count in week:
            x, y = X0 + j * PITCH, Y0 + weekday * PITCH
            fill = LEVELS[level(count)]
            anim = ''
            t = flash.get((j, weekday))
            if t is not None:
                k0, k1, k2 = t / loop, (t + .06) / loop, min((t + .7) / loop, 1)
                anim = (f'<animate attributeName="fill" dur="{loop:.2f}s" repeatCount="indefinite" calcMode="linear" '
                        f'keyTimes="0;{k0:.4f};{k1:.4f};{k2:.4f};1" values="{fill};{fill};#fff3c4;{fill};{fill}"/>')
            cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2" fill="{fill}">{anim}</rect>')

    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    kt_end = dur / loop
    trail = (f'<path d="{d}" fill="none" stroke="{ACCENT}" stroke-width="2.4" filter="url(#trailglow)" stroke-linejoin="miter" '
             f'stroke-dasharray="{TRAIL} {total + 2 * TRAIL:.0f}" stroke-dashoffset="{TRAIL}">'
             f'<animate attributeName="stroke-dashoffset" dur="{loop:.2f}s" repeatCount="indefinite" calcMode="linear" '
             f'keyTimes="0;{kt_end:.4f};1" values="{TRAIL};{TRAIL - total:.1f};{TRAIL - total - TRAIL:.1f}"/></path>')
    # The cycle itself: a long bright capsule with a white-hot core, pointing along the path.
    bike = (f'<g><animateMotion dur="{loop:.2f}s" repeatCount="indefinite" rotate="auto" calcMode="linear" '
            f'keyPoints="0;1;1" keyTimes="0;{kt_end:.4f};1" path="{d}"/>'
            f'<rect x="-15" y="-3.6" width="18" height="7.2" rx="3.6" fill="{ACCENT}" filter="url(#bikeglow)"/>'
            f'<rect x="-11" y="-1.4" width="12" height="2.8" rx="1.4" fill="#fffbe8"/></g>')

    gw = X0 * 2 + (n - 1) * PITCH + CELL
    gh = Y0 * 2 + 6 * PITCH + CELL
    H = round(gh * W / gw + 26)
    body = f'''<defs>
<filter id="bikeglow" x="-100%" y="-200%" width="300%" height="500%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="trailglow" x="-5%" y="-50%" width="110%" height="200%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="gridclip"><rect width="{gw:.1f}" height="{gh:.1f}"/></clipPath>
</defs>
<svg x="0" y="0" width="{W}" height="{gh * W / gw:.0f}" viewBox="0 0 {gw:.1f} {gh:.1f}">
<g clip-path="url(#gridclip)">{''.join(cells)}{trail}{bike}</g></svg>
<text x="{W / 2}" y="{H - 6}" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing=".5" fill="{TEXT_DIM}" text-anchor="middle">One Square = One Day Of Contributions · Last 12 Months</text>'''
    return svg(W, H, 'A light cycle riding across my contribution graph', body)


def main():
    if sys.argv[1] == '--sample':
        weeks, out = sample(), sys.argv[2]
    else:
        weeks, out = fetch(sys.argv[1]), sys.argv[2]
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(draw(weeks))
    print('wrote', out)


if __name__ == '__main__':
    main()
