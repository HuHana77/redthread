# Connector template rendering

Use only authored paths from `assets/connectors/templates.json`. With a selected Python/Pillow backend, `scripts/render_connector.py` is the preferred deterministic renderer. With another raster/SVG backend, reproduce the same template selection and stroke construction below. The template library—not Pillow and not an image-generation model—is the connector source of truth.

## Inputs

- Render at the exact final canvas width and height.
- Pass `--start` and `--end` as corresponding subject-local anchors in final-canvas pixels. For a human subject, use the transferred positions of the same visible little-finger point when available. If no little finger is identifiable, use any clear pointed extremity on the subject contour. For a non-human subject, use any clear corresponding contour tip.
- Pass the lettering accent as `--color`.
- Keep the default stroke width and `--texture-strength 0.58` for the approved thin colored-pencil treatment. Override them only for an explicit connector-stroke revision.
- Keep `--template auto` and `--mirror auto` for a new composition.
- Use a stable integer `--seed` so revisions reproduce the same selection.
- Supply `--avoid-mask` whenever important content lies between the anchors.

The optional avoid mask must be a same-size image. White or opaque pixels are protected; black or transparent pixels are free. Include the face, eyes, hands, held props, Japanese, English, and any region the line must not cross, except for the minimum contact area around the selected little finger or fallback contour tip. The renderer ignores a short distance immediately around each endpoint so the thread can touch its anchors. Do not enlarge the unprotected area beyond the minimum contact needed at the selected tip.

## Selection behavior

In automatic mode the renderer evaluates all bundled paths and both mirror directions. It prefers paths that stay inside the canvas and have the least overlap with the avoid mask, then uses the seed as a deterministic tie-breaker. It transforms the selected normalized path to the two anchors and rerenders the stroke; it never stretches a connector bitmap.

The renderer draws a narrow semi-opaque core with slow pressure variation, two faint offset fibers, irregular edge density, and deterministic micro-grain. The resulting alpha deliberately reveals small amounts of the background like colored pencil or dry wax crayon. Do not post-process it into a fully opaque line.

For a non-Pillow backend, parse only the authored absolute `M` and cubic `C` commands. Sample each cubic densely, normalize the authored endpoints onto the anchor axis, map that axis from `--start` to `--end`, and scale only the perpendicular spread. Evaluate every template in both mirror directions against canvas bounds and the protected mask, select the lowest-collision candidate with the stable seed as tie-breaker, then render the same core, two offset fibers, pressure variation, and translucent grain. Never generate new control points or simplify the template into an S-curve.

Use `--template loose-XX` only when a revision must retain or deliberately replace a known shape. Use `--mirror yes` or `--mirror no` only when directing the line toward a specific free side.

## Visual acceptance

Inspect the connector inside the full composition at full resolution and around 400 px wide. Accept it only when all are true:

- The line is continuous from anchor to anchor.
- When a human little finger is visible, each endpoint visibly meets the corresponding little finger at the same canonical subject-local point.
- When no little finger is identifiable, each endpoint visibly meets the same selected pointed contour extremity; the fallback may be any clear tip but never nearby empty space or invented geometry.
- For a non-human subject, each endpoint visibly meets the same selected contour tip in the two copies.
- Three to five curls are clearly visible and differ in size, direction, or spacing.
- The overall route has long calm sections between some curls.
- Crossings are clean and never collapse into knots or dots.
- The line avoids the face, eyes, hands, props, and lettering except at its intentional anchors.
- The stroke feels related to the DartsFont lettering: thin, dry, slightly fibrous, and handmade rather than mechanically perfect.
- Fine grain and partial transparency are visible at full resolution while the stroke remains continuous and legible at thumbnail size.

Reject a thick opaque marker, clean solid vector, blurry airbrush line, broken speckled line, regular sine wave, one large S-curve, a vertical spine, evenly spaced loops, repeated springs, small side bumps, angular polyline joints, high-frequency path jitter, or visible raster stair-stepping. Change the seed first; if layout constraints remain tight, move the lower subject by translation or choose a specific template and mirror direction.

## Output handling

The script writes one transparent RGBA PNG. Keep it under `work/`, composite it once, and never expose it separately. Do not chroma-key it and do not place it in `outputs/`.
