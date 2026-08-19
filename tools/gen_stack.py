# -*- coding: utf-8 -*-
"""Generate the stack panel — same signal-panel language as the hero banner."""
from gen_hero import DARK, LIGHT, DISPLAY, MONO, MONO_SB, path, MX

W, H = 1600, 418

COLUMNS = [
    ("01", "MOBILE",   ["Flutter", "Dart", "Rive", "Firebase", "Appwrite"]),
    ("02", "WEB",      ["React", "Next.js", "TypeScript", "Node.js", "GraphQL", "Tailwind"]),
    ("03", "CHAIN",    ["Solidity", "EVM", "IPFS", "Web3"]),
    ("04", "PLATFORM", ["PostgreSQL", "MongoDB", "AWS", "GCP", "Python"]),
]


def build(P):
    o, A = [], P["accent"]

    o.append(f'''<defs>
  <linearGradient id="sg" x1="0" y1="0" x2="0.3" y2="1">
    <stop offset="0" stop-color="{P['bg2']}"/><stop offset="1" stop-color="{P['bg']}"/>
  </linearGradient>
  <radialGradient id="sw" cx="0.9" cy="0.1" r="0.7">
    <stop offset="0" stop-color="{A}" stop-opacity="{P['glow']*0.6:.3f}"/>
    <stop offset="1" stop-color="{A}" stop-opacity="0"/>
  </radialGradient>
  <filter id="sgrain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
</defs>''')

    o.append(f'<rect width="{W}" height="{H}" fill="url(#sg)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#sw)"/>')

    # ruler ticks, top and bottom, matching the hero
    t = []
    for i, x in enumerate(range(0, W + 1, 16)):
        h = 11 if i % 5 == 0 else 5
        t.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>')
        t.append(f'<line x1="{x}" y1="{H}" x2="{x}" y2="{H-h}"/>')
    o.append(f'<g stroke="{P["rule"]}" stroke-width="1">{"".join(t)}</g>')

    colw = (W - 2 * MX) / 4
    for i, (idx, title, items) in enumerate(COLUMNS):
        cx = MX + i * colw
        if i:
            o.append(f'<line x1="{cx-30:.1f}" y1="62" x2="{cx-30:.1f}" y2="382" '
                     f'stroke="{P["rule"]}" stroke-width="1"/>')
        el, iw = path(idx, MONO_SB, 20, cx, 96, A, 0.1)
        o.append(el)
        el, _ = path(title, DISPLAY, 54, cx + iw + 18, 100, P["text"], 0.03)
        o.append(el)
        o.append(f'<line x1="{cx:.1f}" y1="122" x2="{cx+colw-60:.1f}" y2="122" '
                 f'stroke="{P["rule"]}" stroke-width="1.5"/>')
        for j, item in enumerate(items):
            y = 166 + j * 40
            o.append(f'<rect x="{cx:.1f}" y="{y-9}" width="7" height="7" fill="{A}" '
                     f'opacity="{0.9 - j*0.11:.2f}"/>')
            el, _ = path(item, MONO, 24, cx + 22, y, P["text"], 0.02)
            o.append(el)

    o.append(f'<rect width="{W}" height="{H}" filter="url(#sgrain)" '
             f'opacity="{P["grain"]}" style="mix-blend-mode:overlay"/>')
    o.append(f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" fill="none" '
             f'stroke="{P["rule"]}" stroke-width="1.5"/>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
            f'height="{H}" role="img" aria-label="Stack. Mobile: Flutter, Dart, Rive, '
            f'Firebase, Appwrite. Web: React, Next.js, TypeScript, Node.js, GraphQL, '
            f'Tailwind. Chain: Solidity, EVM, IPFS, Web3. Platform: PostgreSQL, MongoDB, '
            f'AWS, GCP, Python.">\n' + "\n".join(o) + "\n</svg>\n")


if __name__ == "__main__":
    for P in (DARK, LIGHT):
        open(f"../assets/stack-{P['name']}.svg", "w").write(build(P))
        print("wrote assets/stack-%s.svg" % P["name"])
