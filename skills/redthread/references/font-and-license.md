# DartsFont handling

Use the bundled font at `assets/fonts/dartsfont/DartsFont-Regular.ttf` for every English and Japanese fragment.

## Required handling

- Keep the TTF bundled when copying, installing, packaging, or distributing this Skill.
- Treat a missing TTF as an incomplete Skill package; do not ask the user to download it again during normal use.
- Pass the bundled asset path explicitly to the lettering renderer.
- Check the font's Unicode cmap before rendering every phrase. Stop on a missing glyph rather than mixing fonts.
- Preserve the bundled font data unchanged.
- Preserve `assets/fonts/dartsfont/OFL.txt` with every redistributed copy. DartsFont v2.17 by DAICHI / ProjectDARTS is distributed under the SIL Open Font License 1.1. The authoritative source is `https://www.p-darts.jp/font/dartsfont/`.
- Images created by the Skill do not need to include or expose the font file separately.

## Lettering treatment

- Render text deterministically.
- Add restrained per-glyph rotation, baseline drift, and tracking variation.
- Keep English inside the upper silhouette.
- Use one shared Japanese size.
- Prefer two-line Japanese over reducing only one side.
- Preserve clear glyph edges in the final single-pass render.
