# -*- coding: utf-8 -*-
"""Generate the lebe24 profile hero banner: a 'signal panel' in dark + light.

All display type is converted to vector outlines so the banner renders
identically everywhere (GitHub strips webfonts from <img>-embedded SVG).
"""
import typeset

DISPLAY = "fonts/BigShoulders-Bold.ttf"
MONO = "fonts/IBMPlexMono-Medium.ttf"
MONO_SB = "fonts/IBMPlexMono-SemiBold.ttf"

W, H = 1600, 420
MX = 84

DARK = dict(
    name="dark",
    bg="#0A0B0D", bg2="#101318",
    grid="#1A1F26", rule="#2A323C",
    dim="#7D8896", text="#EDF1F6",
    accent="#FF9B21",
    glow=0.22, grain=0.045, grid_op=0.60, flap_op=0.34,
)
LIGHT = dict(
    name="light",
    bg="#F2EFE8", bg2="#E9E5DB",
    grid="#D6CFBE", rule="#B3A992",
    dim="#6E6656", text="#14161A",
    accent="#B8530B",
    glow=0.12, grain=0.030, grid_op=0.95, flap_op=0.46,
)


def path(s, font, size, x, y, fill, tracking=0.0, anchor="start", cls=None, delay=None):
    """Outlined text. Animation classes go on a wrapping <g> so that CSS
    transforms never clobber the <path>'s own positioning transform."""
    d, w = typeset.text_path(s, font, size, tracking)
    if anchor == "end":
        x -= w
    elif anchor == "middle":
        x -= w / 2
    el = f'<path d="{d}" transform="translate({x:.2f},{y:.2f})" fill="{fill}"/>'
    # Intro reveals are deliberately not used: if the animation clock never
    # advances (background tab, image rasterizer, social-preview renderer) an
    # opacity-0 start state would leave the banner blank. Only ambient motion
    # that is fully legible at t=0 is allowed.
    if cls in ("fade", "rise"):
        cls = None
    if cls:
        st = f' style="animation-delay:{delay:.2f}s"' if delay is not None else ""
        el = f'<g class="{cls}"{st}>{el}</g>'
    return el, w


def width(s, font, size, tracking=0.0):
    return typeset.measure(s, font, size, tracking)


def build(P, static=False):
    o = []
    A = P["accent"]

    o.append(f'''<defs>
  <linearGradient id="ground" x1="0" y1="0" x2="0.35" y2="1">
    <stop offset="0" stop-color="{P['bg2']}"/><stop offset="1" stop-color="{P['bg']}"/>
  </linearGradient>
  <radialGradient id="warm" cx="0.12" cy="0.95" r="0.8">
    <stop offset="0" stop-color="{A}" stop-opacity="{P['glow']}"/>
    <stop offset="1" stop-color="{A}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sweepg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{A}" stop-opacity="0"/>
    <stop offset="0.75" stop-color="{A}" stop-opacity="0.16"/>
    <stop offset="1" stop-color="{A}" stop-opacity="0"/>
  </linearGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>
</defs>''')

    if not static:
        o.append('''<style>
  /* Only ambient motion, and every keyframe at t=0 is the resting, fully
     legible state. Nothing fades in, so the banner is complete on first paint
     even where the animation clock never advances. */
  .sweep{animation:sweep 11s cubic-bezier(.55,0,.45,1) infinite}
  @keyframes sweep{0%{transform:translateX(-420px)}60%,100%{transform:translateX(1660px)}}
  .flap{animation:flap 3.6s ease-in-out infinite}
  @keyframes flap{0%,100%{opacity:.34}50%{opacity:.75}}
  .beat{animation:beat 2.6s ease-in-out infinite}
  @keyframes beat{0%,100%{opacity:1}50%{opacity:.35}}
  @media (prefers-reduced-motion:reduce){.sweep,.flap,.beat{animation:none}}
</style>''')

    o.append('<g clip-path="url(#frame)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#ground)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#warm)"/>')

    # hairline grid
    g = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>'
                for x in range(MX, W - MX + 1, 62))
    o.append(f'<g stroke="{P["grid"]}" stroke-width="1" opacity="{P["grid_op"]}">{g}</g>')

    # ruler ticks along top + bottom edges
    t = []
    for i, x in enumerate(range(0, W + 1, 16)):
        h = 11 if i % 5 == 0 else 5
        t.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>')
        t.append(f'<line x1="{x}" y1="{H}" x2="{x}" y2="{H-h}"/>')
    o.append(f'<g stroke="{P["rule"]}" stroke-width="1">{"".join(t)}</g>')

    if not static:
        o.append(f'<g class="sweep">'
                 f'<rect x="0" y="0" width="420" height="{H}" fill="url(#sweepg)"/>'
                 f'<rect x="418" y="0" width="1.5" height="{H}" fill="{A}" opacity="0.35"/></g>')

    # ---------------- meta row ----------------
    y_meta = 92
    x = MX
    for i, tok in enumerate(["LONDON · UK", "LEBEPAGE", "EST. 2017"]):
        if i:
            o.append(f'<line x1="{x-19:.1f}" y1="{y_meta-13}" x2="{x-19:.1f}" y2="{y_meta+4}" '
                     f'stroke="{P["rule"]}" stroke-width="1.5"/>')
        el, w = path(tok, MONO_SB, 20, x, y_meta, P["dim"], 0.24, cls="fade", delay=0.05 * i)
        o.append(el)
        x += w + 40
    o.append(f'<circle cx="{x+4:.1f}" cy="{y_meta-7}" r="5" fill="{A}" class="beat"/>')

    # ---------------- name ----------------
    y_name = 216
    NAME = "EMMANUEL P. AMADIKWA"
    el, nw = path(NAME, DISPLAY, 124, MX, y_name, P["text"], 0.012, cls="rise")
    o.append(el)
    o.append(f'<rect x="{MX+nw+24:.1f}" y="{y_name-86}" width="17" height="86" '
             f'fill="{A}" class="beat"/>')
    o.append(f'<path d="M{MX} {y_name+26} H{MX+nw+41:.1f}" stroke="{A}" '
             f'stroke-width="3" fill="none"/>')

    # ---------------- role ----------------
    y_role = 274
    x = MX
    el, w = path("SOFTWARE DEVELOPER", MONO_SB, 25, x, y_role, P["text"], 0.14,
                 cls="fade", delay=0.5)
    o.append(el); x += w + 26
    el, w = path("/", MONO_SB, 25, x, y_role, A, 0, cls="fade", delay=0.55)
    o.append(el); x += w + 26
    el, w = path("WEB · MOBILE · BLOCKCHAIN", MONO, 25, x, y_role, P["dim"], 0.14,
                 cls="fade", delay=0.6)
    o.append(el)

    # ---------------- divider ----------------
    o.append(f'<line x1="{MX}" y1="316" x2="{W-MX}" y2="316" '
             f'stroke="{P["rule"]}" stroke-width="1"/>')

    # ---------------- stat strip ----------------
    cells = [("STACK", "FLUTTER · REACT · SOLIDITY"),
             ("BUILDING", "BEFIT AI"),
             ("SITE", "LEBE.PAGES.DEV"),
             ("HANDLE", "@LEBE24")]
    LS, VS = 16, 20          # label / value size
    LT, VT = 0.28, 0.02      # label / value tracking
    # Columns are sized to their content, with the slack shared out as equal
    # gutters, so long values can never collide with the next column.
    colw = [max(width(l, MONO, LS, LT), width(v, MONO_SB, VS, VT)) for l, v in cells]
    avail = W - 2 * MX
    gutter = (avail - sum(colw)) / (len(cells) - 1)
    assert gutter > 24, f"stat strip overflows: gutter={gutter:.1f}"
    cx = MX
    for i, (lab, val) in enumerate(cells):
        if i:
            o.append(f'<line x1="{cx-gutter/2:.1f}" y1="336" x2="{cx-gutter/2:.1f}" y2="396" '
                     f'stroke="{P["rule"]}" stroke-width="1"/>')
        el, _ = path(lab, MONO, LS, cx, 356, P["dim"], LT)
        o.append(el)
        el, _ = path(val, MONO_SB, VS, cx, 386, P["text"], VT)
        o.append(el)
        cx += colw[i] + gutter

    # ---------------- split-flap cluster (top right) ----------------
    cols, rows = 7, 5
    cellw, cellh, gap = 34, 22, 7
    gx = W - MX - (cols * cellw + (cols - 1) * gap)
    gy = 216 - (rows * (cellh + gap) - gap)   # bottom-aligns with name baseline
    hot = {(0, 2), (1, 0), (2, 5), (0, 6), (3, 1), (4, 4), (2, 2), (4, 6)}
    fl = []
    for r in range(rows):
        for c in range(cols):
            x0, y0 = gx + c * (cellw + gap), gy + r * (cellh + gap)
            fill = A if (r, c) in hot else P["dim"]
            fl.append(f'<rect x="{x0}" y="{y0}" width="{cellw}" height="{cellh}" rx="2.5" '
                      f'fill="{fill}" opacity="{P["flap_op"]}" class="flap" '
                      f'style="animation-delay:{(r*cols+c)*0.11:.2f}s"/>')
            fl.append(f'<line x1="{x0}" y1="{y0+cellh/2}" x2="{x0+cellw}" y2="{y0+cellh/2}" '
                      f'stroke="{P["bg"]}" stroke-width="1.2" opacity="0.7"/>')
    o.append("".join(fl))
    # ---------------- corner registration marks ----------------
    m = []
    for (cx, cy) in [(MX - 36, 36), (W - MX + 36, 36), (MX - 36, H - 36), (W - MX + 36, H - 36)]:
        m.append(f'<line x1="{cx-10}" y1="{cy}" x2="{cx+10}" y2="{cy}"/>'
                 f'<line x1="{cx}" y1="{cy-10}" x2="{cx}" y2="{cy+10}"/>')
    o.append(f'<g stroke="{A}" stroke-width="1.5" opacity="0.75">{"".join(m)}</g>')

    # grain + frame
    o.append(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity="{P["grain"]}" '
             f'style="mix-blend-mode:overlay"/>')
    o.append(f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" fill="none" '
             f'stroke="{P["rule"]}" stroke-width="1.5"/>')
    o.append('</g>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
            f'height="{H}" role="img" aria-label="Emmanuel P. Amadikwa — software developer '
            f'in London. Web, mobile and blockchain.">\n' + "\n".join(o) + "\n</svg>\n")


if __name__ == "__main__":
    for P in (DARK, LIGHT):
        open(f"../assets/hero-{P['name']}.svg", "w").write(build(P))
        print("wrote assets/hero-%s.svg" % P["name"])
