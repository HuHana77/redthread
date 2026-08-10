# AsobiMemogaki font handling

Use the bundled font at `assets/fonts/asobi-memogaki/AsobiMemogaki-Regular-1-02.ttf` for every English and Japanese fragment.

## Required handling

- Keep the TTF bundled when copying, installing, packaging, or distributing this Skill.
- Treat a missing TTF as an incomplete Skill package; do not ask the user to download it again during normal use.
- Pass the bundled asset path explicitly to the lettering renderer.
- Check the font's Unicode cmap before rendering every phrase. Stop on a missing glyph rather than mixing fonts.
- Preserve the bundled font data unchanged.
- Images created by the Skill do not need to include or expose the font file separately.

## Lettering treatment

- Render text deterministically.
- Add restrained per-glyph rotation, baseline drift, and tracking variation.
- Keep English inside the upper silhouette.
- Use one shared Japanese size.
- Prefer two-line Japanese over reducing only one side.
- Preserve clear glyph edges in the final single-pass render.
