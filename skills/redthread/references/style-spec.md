# Style specification

## Canvas and subject

- Use an exact 3:4 vertical canvas with a clean 50/50 horizontal split.
- Build one canonical transparent subject from the source photo.
- Preserve identity, expression, pose, scale, hand shape, clothing, accessories, and props.
- Reuse the exact RGBA subject and alpha contour for both appearances.
- Keep the upper copy at the source-relative position when practical.
- Reposition the lower copy by translation only; never resize it independently.

## Upper panel

- Retain the original environment and perspective.
- Convert the canonical subject to warm cream white without changing its alpha.
- Add a soft temperature-aware glow outside the contour.
- Keep the silhouette mostly solid while retaining faint hand or prop detail only when it improves recognition.

## Lower panel

- Use `assets/paper/theme-fiber-paper.jpg` as the entire background.
- Center-cover-crop it to the panel without stretching.
- Recolor its average color to a softened source-derived theme while preserving fibers, short dark strands, pulp marks, scan softness, and local tonal variation.
- Composite the real canonical subject above the recolored paper without changing identity or photographic texture.
- Reserve useful negative space on both sides for Japanese.

## Palette

Derive four roles from the source:

1. Environment: retain the source scene in the upper panel.
2. Theme: sample a muted representative source color for recoloring the fixed paper.
3. Accent: choose a darker related vintage red, brown-red, or brick red.
4. Glow: choose neutral white, warm white, or cream white from the source lighting.

Use the same accent for all lettering and the connector.

## Text

- Generate three or four English fragments of two to five words from the scene's time, place, action, prop, and emotion.
- Place all English entirely inside the upper silhouette.
- Generate two short Japanese thoughts, one on each side of the lower subject.
- Prefer no punctuation.
- Give both Japanese fragments exactly the same font size and make them visibly larger than English when space allows.
- Move Japanese close to the subject contour without touching the face, hands, held prop, or connector.
- Use natural two-line breaks instead of shrinking one Japanese side independently.
- Use small opposing rotations and asymmetric placement.

## Connector

- Use one uninterrupted line rendered from `assets/connectors/templates.json` by `scripts/render_connector.py` in the text accent color.
- When the canonical subject contains a person and a little finger is clearly visible, connect the upper and lower copies at the exact corresponding subject-local point on that little finger.
- If no little finger is identifiable, freely choose any clear pointed extremity on the subject contour, such as another fingertip, a shoe tip, a hair tip, a garment corner, or a held-prop tip. Do not invent missing geometry.
- For a non-human subject, choose any clear contour tip on the main object.
- In every case, transfer one selected subject-local point to both copies and make both endpoints visibly meet it rather than nearby empty space.
- Prefer long loose meanders with three to five isolated curls.
- Vary curl size, direction, spacing, and pressure.
- Use the renderer's thin colored-pencil treatment: a semi-dry wine-red core, faint offset fibers, subtly irregular edges, and small translucent grain that lets the background show through.
- Match the quiet hand-drawn character of the DartsFont lettering without copying glyph shapes or making the connector look fuzzy.
- Keep the line readable at thumbnail size and away from the face and eyes.
- Prefer `--template auto --mirror auto` and supply a protected-area mask so template selection can avoid important content.
- Do not generate or redraw the connector with an image model, Pillow primitives, a sine wave, random points, or a newly invented spline.
- Reject thick marker strokes, fully opaque solid vectors, airbrush softness, broken dotted lines, springs, telephone cords, stacked circles, repeated loops, small attached blobs, regular S-curves, and straight vertical spines.

## Final output

- Treat the assembled composition as the final image; do not create an approval proof followed by a separate filter pass.
- Preserve the fixed paper's visible texture. Do not cover it with synthetic paper grain or replace it with a flat color.
- Keep the real lower subject naturally integrated with the theme color without rebuilding the face or clothing.
- Inspect both full resolution and a roughly 400 px thumbnail privately, then deliver one final PNG.
- Keep the subject cutout, masks, connector asset, component layers, and QA thumbnail internal. Do not preview, attach, link, or place them in the user-facing output directory unless the user explicitly asks for a specific intermediate.

At thumbnail size, the person, two-panel structure, wine-red graphic system, Japanese side placement, and paper texture must remain immediately readable.
