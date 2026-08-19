"""Shape a string with HarfBuzz and return SVG path data in user units."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

_cache = {}

def _load(path):
    if path not in _cache:
        blob = hb.Blob.from_file_path(path)
        face = hb.Face(blob)
        font = hb.Font(face)
        tt = TTFont(path)
        _cache[path] = (font, tt, face.upem, tt.getGlyphSet())
    return _cache[path]

def text_path(s, font_path, size, tracking=0.0):
    """tracking = extra letterspacing in em units (e.g. 0.08 = 8% of size).
    Returns (svg_path_d, advance_width). Baseline at y=0, text starts at x=0."""
    hbfont, tt, upem, gs = _load(font_path)
    buf = hb.Buffer()
    buf.add_str(s)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})

    scale = size / upem
    track_units = tracking * size
    order = tt.getGlyphOrder()
    parts = []
    x = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gname = order[info.codepoint]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        # flip Y (font up-positive -> SVG down-positive) and scale
        t = Transform(scale, 0, 0, -scale, x + pos.x_offset * scale, -pos.y_offset * scale)
        gs[gname].draw(TransformPen(pen, t))
        d = pen.getCommands()
        if d:
            parts.append(d)
        x += pos.x_advance * scale + track_units
    if s and track_units:
        x -= track_units  # no trailing track
    return " ".join(parts), x

def measure(s, font_path, size, tracking=0.0):
    return text_path(s, font_path, size, tracking)[1]
