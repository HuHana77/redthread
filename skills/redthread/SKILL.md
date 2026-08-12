---
name: redthread
description: Create or revise a finished 3:4 vertical two-panel portrait collage from one user-supplied photo, with one canonical subject reused as a glowing upper silhouette and a real lower cutout, DartsFont bilingual hand-lettering, one loose wine-red colored-pencil template connector anchored to corresponding little fingers when visible or to any clear subject-contour tip otherwise, and the bundled theme fiber paper mandatorily recolored to the source-derived theme as the lower background. Produce and expose only one final PNG directly, keeping the cutout subject, connector, masks, and other intermediate assets private. Use for new photos in this recurring collage style and for changes to subject placement, theme color, typography, Japanese placement, connector anchors, connector shape or hand-drawn stroke texture, or paper color, across hosts with different image backends, including environments without an image-generation model. Works in Doubao Pro, Codex, and other SKILL.md hosts.
---

# Redthread

Build one finished editorial collage directly from a user photo. Preserve the real subject and deliver the inspected composition as the final image. Do not introduce an approval stage or promise a later filter version.

## Runtime routing

- Treat installation and discovery as zero-setup. Do not import, probe, install, or report the status of optional Python packages merely because this Skill was installed or selected.
- At the start of an actual collage task, privately choose an already-available image backend. Prefer the host's established image-editing/compositing capability; otherwise use an existing Python interpreter with Pillow for the bundled raster helpers. NumPy is not required.
- In Codex desktop, obtain the configured workspace dependency paths and use the returned bundled Python executable for image work. Do not assume the operating system's `python` or `python3` is the correct interpreter. In other hosts, use their existing managed runtime or native image backend.
- Never ask to install Pillow, NumPy, or another package preemptively. Never emit a dependency-readiness warning when another compatible backend is available. Do not install packages or modify the user's environment without explicit permission.
- If Pillow is unavailable, use the host's existing raster/SVG compositor with the exact bundled font, paper, connector templates, and visual rules. Render the authored cubic connector paths; never invent a procedural replacement. A backend change must not relax the quality gate.
- Report a blocked task only after an actual collage request has no usable image-editing/compositing backend at all. Describe the missing capability, not a list of preferred packages.

## Reference routing

- For every new collage and visual revision, read [references/style-spec.md](references/style-spec.md) completely before acting. It is the required visual source of truth; never skip it to save tokens.
- Read [references/font-and-license.md](references/font-and-license.md) only for font installation, packaging, replacement, diagnosis, or failed glyph validation.
- Read [references/fixed-paper.md](references/fixed-paper.md) for a non-Pillow backend, paper or recoloring-script changes, diagnosis, or failed paper QA.
- Read [references/connector-templates.md](references/connector-templates.md) for a non-Pillow backend, an explicit connector revision, renderer failure, or failed connector QA.

In a normal successful Pillow-backed run, follow steps 6, 9, and 10 and execute the bundled scripts directly. Do not inspect implementation references, script source, or `assets/connectors/templates.json` unless using another backend, revising, or diagnosing them.

## Workflow

1. Inspect every supplied source at useful detail. Record subject contour, face, hands, little-finger visibility when any person is present, transparent or reflective props, environment, dominant color, lighting temperature, crop safety, and negative space.
2. State a concise plan covering the 3:4 crop, equal panel split, source-derived theme color, text direction, connector anchors, and protected details. For a human subject, use one visible little finger as the anchor; if no little finger is identifiable, name any clear pointed extremity on the subject contour instead.
3. Establish one canonical transparent subject as a private working asset. Reuse the exact same RGBA pixels and alpha in both panels. Never extract or generate the upper and lower subjects separately, and never preview or deliver the cutout by itself.
4. Preserve identity, face, hair, pose, fingers, clothing, accessories, held objects, and meaningful motion blur. Reject missing anatomy, artificial face changes, background islands, or damaged props.
5. Build the upper panel from the original environment. Keep the canonical subject at the source-relative position, change only its RGB to warm cream white, and add a soft glow outside the unchanged alpha contour.
6. Derive a softened theme color from the source. With the Pillow backend, run `scripts/recolor_theme_paper.py`; with another image backend, reproduce its center-cover crop and luminance-preserving theme mapping. Always use `assets/paper/theme-fiber-paper.jpg` as the entire lower-panel background. Never use a flat fill, generated paper, or another texture.
7. Reuse the real canonical subject in the lower panel at the identical scale. Reposition by translation only and retain balanced side space.
8. Write three or four short English mood fragments and two short Japanese thoughts derived from the photo. Follow `style-spec.md` for wording and placement.
9. Use `assets/fonts/dartsfont/DartsFont-Regular.ttf` for every English and Japanese fragment. Validate glyph coverage and render deterministically with restrained per-glyph rotation, baseline drift, and loose tracking. Never model-generate letters.
10. Render exactly one isolated transparent connector from the authored cubic paths in `assets/connectors/templates.json`. When the canonical subject contains a person and a little finger is clearly visible, identify one little-finger contour point once, transfer that same subject-local point to the upper and lower copies, and use the two final-canvas positions as the connector endpoints. If no little finger is identifiable, freely choose any clear pointed extremity on the subject contour, such as another fingertip, a shoe tip, a hair tip, a garment corner, or a held-prop tip; use the exact same subject-local point in both copies and do not invent missing geometry. For a non-human subject, use any clear corresponding contour tip. Make both endpoints visibly meet the selected anchor rather than nearby empty space. With the Pillow backend, use `scripts/render_connector.py`. With another backend, render the same selected template, anchor mapping, mirroring, protected-area avoidance, and colored-pencil layer treatment described in `references/connector-templates.md`; do not design a new curve. Keep restrained pressure changes, faint edge fibers, and partial paper show-through. Do not use an image-generation tool for the connector, a hand-written replacement path, a sine wave, a random polyline, a solid vector stroke, or a substitute asset.
11. Composite the final image in one pass: paper below all lower-panel content, real subject above paper, and Japanese plus connector above the subject/background as appropriate. Do not create a proof-to-filter sequence.
12. Inspect the full-resolution final and an approximately 400 px thumbnail privately. Fix any defect before displaying and delivering only the final PNG. Do not ask for approval before a nonexistent later finish.

## Intermediate asset handling

- Treat the subject cutout, alpha mask, rendered connector, protected-area mask, component layers, and QA thumbnail as private working assets.
- Store intermediate assets only under the task's `work/` directory or a temporary directory. Never place them in `outputs/`.
- Do not display, attach, or emit intermediate images in commentary or tool output. Render the connector directly to `work/` and never forward or preview it as a standalone image.
- Do not include intermediate filenames, paths, download links, or previews in the final response.
- Put only the completed collage PNG in `outputs/`, and show or link only that file. Reveal an intermediate asset only when the user explicitly asks to see that specific asset.

## Revision rules

- Revise the current final composition and rerender from its clean component layers. Do not stack changes over a flattened, degraded copy when the components remain available.
- Never replace, omit, synthesize, or procedurally recreate `assets/paper/theme-fiber-paper.jpg`. Recolor that exact bundled image for every lower panel.
- If the Japanese pair cannot fit at one shared size, use natural two-line breaks and move both closer to the subject. Do not shrink one side independently.
- If the bundled font or paper is missing or unreadable, report that the Skill package is incomplete and stop. Do not silently substitute another asset.
- If `assets/connectors/templates.json` or `scripts/render_connector.py` is missing or unreadable, report that the Skill package is incomplete and stop. Do not improvise a connector.
- Preserve the selected corresponding anchor through every revision. When a little finger is visible, keep the little-finger anchor; otherwise keep the chosen contour tip unless the user requests a different one.
- Never end with language such as “confirm this version and I will add the final filter.” The inspected single-pass collage is already the final deliverable.

## Font validation

Validate every planned phrase before rendering:

```bash
SELECTED_PYTHON scripts/check_font_glyphs.py "ENGLISH TEXT" "日本語テキスト"
```

Replace `SELECTED_PYTHON` with the privately selected managed interpreter's executable path; it is not necessarily the system Python. The glyph checker itself uses only the Python standard library; an equivalent cmap check from the selected host backend is also acceptable.

## Fixed paper command

Create the exact lower-panel paper at the required dimensions and theme color:

```bash
SELECTED_PYTHON scripts/recolor_theme_paper.py LOWER_PAPER.png \
  --color "#B5A594" --width 1200 --height 800
```

Replace the example color and dimensions for the current composition. The script always reads the bundled `theme-fiber-paper.jpg`; it has no paper override option.

## Connector command

Render the connector at the exact final canvas size. Coordinates are final-canvas pixels:

```bash
SELECTED_PYTHON scripts/render_connector.py work/connector.png \
  --width 1200 --height 1600 \
  --start 720,180 --end 610,1410 \
  --color "#8F2634" --seed 27 \
  --avoid-mask work/connector-protected.png
```

Omit `--avoid-mask` only when there truly are no protected regions between the anchors. Keep `--template auto` and `--mirror auto` unless revising a specifically chosen connector. See `references/connector-templates.md` for mask semantics and rejection rules.

## Quality gate

Deliver only when all are true:

- The canvas is exact 3:4 with equal-height panels.
- Both subject appearances come from one canonical RGBA layer at a 1.0 scale ratio.
- Face, hair, hands, clothing, accessories, and props remain faithful to the source.
- English stays inside the upper silhouette.
- Both Japanese fragments use one identical size, sit near the lower subject, and avoid the eyes, hands, prop, and connector.
- All text uses the bundled DartsFont with no missing glyphs.
- When a human little finger is visible, both connector endpoints visibly meet the corresponding upper and lower little fingers at the same canonical subject-local point.
- When no little finger is identifiable, both endpoints visibly meet the same selected clear contour tip in the upper and lower copies. The fallback may be any pointed extremity but must not land in nearby empty space or require invented geometry.
- For a non-human subject, both connector endpoints meet the same selected clear contour tip in the two copies.
- The connector comes from an authored path in the bundled template library, has three to five visibly distinct loose curls, stays continuous, and uses a fine semi-dry colored-pencil or wax-crayon texture that visually belongs with the DartsFont lettering. It must not read as a thick opaque marker, clean solid vector, regular sine wave, single S-curve, repeated spring, or dotted polyline.
- The lower panel visibly retains `theme-fiber-paper.jpg` fibers and natural marks, recolored to the current source-derived theme.
- The final reads clearly at full resolution and around 400 px wide.
- Only the completed collage is exposed to the user; no cutout, mask, connector, component layer, or QA thumbnail is shown or delivered.
- No watermark, malformed text, duplicated limb, blank edge, accidental crop, paper substitution, or background island is present.
