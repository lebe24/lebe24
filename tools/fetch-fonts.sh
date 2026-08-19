#!/usr/bin/env bash
# Downloads the two OFL typefaces the banner is set in, then instances the
# Big Shoulders variable font at the fixed weights the generators use.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p fonts

echo "→ fetching Big Shoulders Display + IBM Plex Mono (SIL Open Font License)"
curl -sL -o fonts/BigShouldersDisplay.ttf \
  "https://github.com/google/fonts/raw/main/ofl/bigshouldersdisplay/BigShouldersDisplay%5Bwght%5D.ttf"
curl -sL -o fonts/IBMPlexMono-Medium.ttf \
  "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Medium.ttf"
curl -sL -o fonts/IBMPlexMono-SemiBold.ttf \
  "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-SemiBold.ttf"

echo "→ instancing the variable font at weight 700 / 500"
python3 - <<'PY'
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
for wght, name in [(700, "Bold"), (500, "Medium")]:
    f = TTFont("fonts/BigShouldersDisplay.ttf")
    instancer.instantiateVariableFont(f, {"wght": wght}, inplace=True)
    f.save(f"fonts/BigShoulders-{name}.ttf")
    print("   wrote fonts/BigShoulders-%s.ttf" % name)
PY
echo "✓ fonts ready"
