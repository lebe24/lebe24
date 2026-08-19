# tools

The banner and stack panel in the profile README aren't hand-drawn SVG — they're
generated. All display type is converted to **vector outlines**, because GitHub
loads README images through `<img>`, which can't fetch a webfont. Outlines mean
the panels render identically on every machine instead of falling back to
whatever the viewer happens to have installed.

That also means the `.svg` files are ~60 KB of path data and are not meant to be
edited by hand. Change the source here and regenerate.

## Regenerating

```bash
cd tools
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
./fetch-fonts.sh
python gen_hero.py     # -> ../assets/hero-{dark,light}.svg
python gen_stack.py    # -> ../assets/stack-{dark,light}.svg
```

## What to edit

| Want to change | Where |
|---|---|
| Name, role, location, the four footer cells | `gen_hero.py` — the `build()` layout sections |
| Colours (both themes) | `gen_hero.py` — the `DARK` / `LIGHT` dicts |
| Stack columns and their items | `gen_stack.py` — the `COLUMNS` list |
| Typeface | `fetch-fonts.sh`, then the `DISPLAY` / `MONO` constants |

`typeset.py` shapes a string with HarfBuzz (so kerning and ligatures are real)
and returns SVG path data plus its advance width. Layout code uses those widths
to size columns to their content, which is why the footer cells can't collide.

## Two constraints worth keeping

**Nothing may fade in.** Every animation keyframe at `t=0` is the resting,
fully-legible state. If an intro animation started at `opacity: 0`, the panel
would render blank anywhere the animation clock never advances — a background
tab, an image rasterizer, a social-preview card. Ambient motion only.

**Badges need to survive both GitHub themes.** Near-black disappears on dark,
near-white disappears on light. The README uses a mid-slate label with the amber
accent so the badges hold up either way.

## Fonts

- [Big Shoulders Display](https://fonts.google.com/specimen/Big+Shoulders+Display) — SIL Open Font License 1.1
- [IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono) — SIL Open Font License 1.1

`fetch-fonts.sh` downloads them on demand, so the binaries aren't committed.
