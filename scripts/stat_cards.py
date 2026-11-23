"""Draws the live GitHub stat cards in the README's minimal dark theme (see theme.py):
the headline stats, then the contribution streak and top languages side by side.
Run by .github/workflows/profile-assets.yml, which publishes them to the `output` branch.

Usage: GITHUB_TOKEN=... python stat_cards.py <github-user> <out-dir>
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from collections import Counter

from theme import ACCENT, DISPLAY, GAP, LINE, MONO, SANS, TEXT, TEXT_DIM, TEXT_SOFT, W, esc, glyph, hairline, heading, panel, svg

# ───────────────────────────── data ─────────────────────────────


def get(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'profile-stat-cards', **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8')


def gql(query, **variables):
    body = json.dumps({'query': query, 'variables': variables}).encode()
    res = json.loads(get('https://api.github.com/graphql', body, {'Authorization': f"Bearer {os.environ['GITHUB_TOKEN']}"}))
    if res.get('errors'):
        raise RuntimeError(res['errors'])
    return res['data']


USER_QUERY = '''query($login: String!) { user(login: $login) {
  createdAt
  followers { totalCount }
  pullRequests { totalCount }
  issues { totalCount }
  repositoriesContributedTo(contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) { totalCount }
  allRepos: repositories(ownerAffiliations: OWNER) { totalCount }
  repositories(first: 100, ownerAffiliations: OWNER, isFork: false) { nodes {
    stargazerCount
    languages(first: 10, orderBy: { field: SIZE, direction: DESC }) { edges { size node { name color } } }
  } }
  contributionsCollection { contributionYears }
} }'''

YEAR_QUERY = '''query($login: String!, $from: DateTime!, $to: DateTime!) { user(login: $login) {
  contributionsCollection(from: $from, to: $to) {
    contributionCalendar { weeks { contributionDays { date contributionCount } } }
  }
} }'''


def profile_views(user):
    # komarev only counts requests from GitHub's image proxy, so reading it here doesn't add a view.
    try:
        nums = re.findall(r'>([\d,]+)<', get(f'https://komarev.com/ghpvc/?username={user}'))
        return int(nums[-1].replace(',', '')) if nums else None
    except Exception as e:
        print(f'::warning::profile views: {e}')
        return None


def collect(login):
    u = gql(USER_QUERY, login=login)['user']
    days = {}
    for year in u['contributionsCollection']['contributionYears']:
        c = gql(YEAR_QUERY, login=login, **{'from': f'{year}-01-01T00:00:00Z', 'to': f'{year}-12-31T23:59:59Z'})
        for week in c['user']['contributionsCollection']['contributionCalendar']['weeks']:
            for d in week['contributionDays']:
                days[dt.date.fromisoformat(d['date'])] = d['contributionCount']

    today = dt.datetime.now(dt.timezone.utc).date()
    days = {d: n for d, n in days.items() if d <= today}

    # Streaks. Today doesn't break the current streak until it's over.
    longest, run, run_start, best = 0, 0, None, (None, None)
    for d in sorted(days):
        if days[d]:
            run_start = d if run == 0 else run_start
            run += 1
            if run > longest:
                longest, best = run, (run_start, d)
        else:
            run = 0
    current, d = 0, (today if days.get(today) else today - dt.timedelta(days=1))
    cur_end = d
    while days.get(d):
        current += 1
        d -= dt.timedelta(days=1)
    cur_start = d + dt.timedelta(days=1)

    langs, color, stars_ = Counter(), {}, 0
    for r in u['repositories']['nodes']:
        stars_ += r['stargazerCount']
        for e in r['languages']['edges']:
            langs[e['node']['name']] += e['size']
            color[e['node']['name']] = e['node']['color'] or '#8aa4ad'

    return {
        'joined': dt.date.fromisoformat(u['createdAt'][:10]), 'today': today,
        'total': sum(days.values()),
        'year': sum(n for d, n in days.items() if d.year == today.year),
        'prs': u['pullRequests']['totalCount'], 'issues': u['issues']['totalCount'],
        'contributed': u['repositoriesContributedTo']['totalCount'], 'followers': u['followers']['totalCount'],
        'repos': u['allRepos']['totalCount'], 'stars': stars_, 'views': profile_views(login),
        'current': current, 'current_range': (cur_start, cur_end) if current else None,
        'longest': longest, 'longest_range': best,
        'langs': [(n, sz, color[n]) for n, sz in langs.most_common()],
    }


# ───────────────────────────── helpers ─────────────────────────────

def fmt(n):
    if n is None:
        return '—'
    if n >= 1_000_000:
        return f'{n / 1_000_000:.1f}M'.replace('.0M', 'M')
    if n >= 10_000:
        return f'{n / 1000:.1f}k'.replace('.0k', 'k')
    return f'{n:,}'


def day(d):
    return f'{d:%b} {d.day}, {d.year}' if d else ''


def span(r):
    if not r or not r[0]:
        return 'start one today'
    a, b = r
    if a == b:
        return day(a)
    return f'{a:%b} {a.day} – {b:%b} {b.day}, {b.year}' if a.year == b.year else f'{day(a)} – {day(b)}'


def bar(x, y, w, h, pct, opacity):
    fw = max(w * min(pct, 1), h if pct > 0 else 0)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{LINE}"/>'
            f'<rect x="{x}" y="{y}" width="{fw:.1f}" height="{h}" rx="{h / 2}" fill="{ACCENT}" fill-opacity="{opacity:.2f}" filter="url(#soft)"/>')


# ───────────────────────────── cards ─────────────────────────────

def player(s):
    """Headline numbers: one large lifetime tile and eight small ones."""
    tw, th, x0 = 164, 92, 308
    H = 2 * th + GAP
    tiles = [
        ('git-pull-request', s['prs'], 'Pull requests'), ('bug', s['issues'], 'Issues'),
        ('folder-git-2', s['contributed'], 'Contributed to'), ('star', s['stars'], 'Stars earned'),
        ('book-marked', s['repos'], 'Repositories'), ('users', s['followers'], 'Followers'),
        ('eye', s['views'], 'Profile views'), ('calendar-days', s['year'], f"{s['today'].year} so far"),
    ]
    out = [f'''{panel(296, H)}
<text x="26" y="44" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1.8" fill="{ACCENT}">LIFETIME CONTRIBUTIONS</text>
<text x="24" y="124" font-family="{DISPLAY}" font-size="43" font-weight="500" letter-spacing="-1.5" fill="{TEXT}">{fmt(s['total'])}</text>
{hairline(26, 270, 146)}
<text x="26" y="172" font-family="{SANS}" font-size="13" fill="{TEXT_SOFT}">since {s['joined']:%B %Y}</text>''']
    for i, (g, value, label) in enumerate(tiles):
        x, y = x0 + (i % 4) * (tw + GAP), (i // 4) * (th + GAP)
        out.append(f'''<g transform="translate({x} {y})">{panel(tw, th, 14)}
<text x="18" y="33" font-family="{SANS}" font-size="12.5" fill="{TEXT_SOFT}">{esc(label)}</text>{glyph(g, tw - 33, 20, 15, TEXT_DIM)}
<text x="18" y="72" font-family="{DISPLAY}" font-size="19" font-weight="500" letter-spacing="-.5" fill="{TEXT}">{fmt(value)}</text></g>''')
    label = (f"{s['total']:,} lifetime contributions, {s['year']:,} this year. Pull requests {s['prs']:,}, issues {s['issues']:,}, "
             f"{s['contributed']} repos contributed to, {s['stars']} stars, {s['repos']} repositories, {s['followers']} followers.")
    return svg(W, H, label, ''.join(out))


PANEL_W, PANEL_H = (W - GAP) / 2, 310


def streak(s):
    pw, cx, cy = PANEL_W, PANEL_W / 2, 186

    def column(x, value, label, sub):
        return (f'<text x="{x}" y="{cy + 8}" font-family="{DISPLAY}" font-size="21" font-weight="500" letter-spacing="-.5" fill="{TEXT}" text-anchor="middle">{value}</text>'
                f'<text x="{x}" y="{cy + 32}" font-family="{SANS}" font-size="12.5" fill="{TEXT_SOFT}" text-anchor="middle">{label}</text>'
                f'<text x="{x}" y="{cy + 50}" font-family="{SANS}" font-size="11" fill="{TEXT_DIM}" text-anchor="middle">{esc(sub)}</text>')

    body = f'''{panel(pw, PANEL_H)}{heading('Streak', 'days in a row', 32)}
{column(86, fmt(s['total']), 'Contributions', f"since {s['joined']:%b %Y}")}
{column(pw - 86, s['longest'], 'Best streak', span(s['longest_range']))}
<g transform="translate({cx} {cy})">
  <circle r="44" fill="none" stroke="{LINE}" stroke-width="2"/>
  <circle r="44" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-dasharray="207 70" stroke-linecap="round" transform="rotate(-210)" filter="url(#glow)"/>
  <text y="11" font-family="{DISPLAY}" font-size="22" font-weight="500" letter-spacing="-.5" fill="{TEXT}" text-anchor="middle">{s['current']}</text>
</g>
<text x="{cx}" y="{cy + 72}" font-family="{SANS}" font-size="12.5" fill="{ACCENT}" text-anchor="middle">Current streak</text>
<text x="{cx}" y="{cy + 90}" font-family="{SANS}" font-size="11" fill="{TEXT_DIM}" text-anchor="middle">{esc(span(s['current_range']))}</text>'''
    return body, f"Contribution streak: {s['current']} days now, best {s['longest']} days."


# The languages I know and how well, drawn as-is (GitHub's code-size counts would miss
# everything in private repos). Edit freely: (name, level 0-1, label).
KNOWN_LANGUAGES = [   # (name, level 0-1, label)  set these to match how confident you feel
    ('Python', .6, 'Intermediate'),
    ('Java', .6, 'Intermediate'),
    ('SQL', .5, 'Intermediate'),
    ('JavaScript', .4, 'Beginner'),
    ('HTML', .5, 'Intermediate'),
]


def languages(s):
    pw = PANEL_W
    rows = []
    for i, (name, level, label) in enumerate(KNOWN_LANGUAGES):
        y = 118 + i * 25
        learning = label == 'Learning'
        rows.append(f'<text x="32" y="{y + 9}" font-family="{SANS}" font-size="13.5" font-weight="500" fill="{TEXT}">{esc(name)}</text>'
                    f'{bar(140, y + 4, 210, 2, level, .45 if learning else 1)}'
                    + (f'<circle class="live" cx="{140 + 210 * level + 10:.1f}" cy="{y + 5}" r="2.5" fill="{ACCENT}"/>' if learning else '')
                    + f'<text x="{pw - 32}" y="{y + 9}" font-family="{MONO}" font-size="11.5" fill="{ACCENT if learning else TEXT_SOFT}" text-anchor="end">{label}</text>')
    body = f'{panel(pw, PANEL_H)}{heading("Languages", "what I write", 32)}{"".join(rows)}'
    return body, 'Languages I know: ' + ', '.join(f'{n} ({l.lower()})' for n, _, l in KNOWN_LANGUAGES) + '.'


def streak_and_languages(s):
    b1, l1 = streak(s)
    b2, l2 = languages(s)
    style = '.live { animation: live 2s ease-in-out infinite; } @keyframes live { 50% { opacity: .25; } }'
    return svg(W, PANEL_H, f'{l1} {l2}', f'<g>{b1}</g>\n<g transform="translate({PANEL_W + GAP} 0)">{b2}</g>', style)


def main():
    login, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    s = collect(login)
    for name, text in {'stats-player.svg': player(s), 'stats-streak-languages.svg': streak_and_languages(s)}.items():
        with open(os.path.join(out, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    print({k: v for k, v in s.items() if k != 'langs'})


if __name__ == '__main__':
    main()
