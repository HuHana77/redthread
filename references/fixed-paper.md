# Mandatory theme-responsive lower-panel paper

Use `assets/paper/theme-fiber-paper.jpg` as the lower-panel background in every final collage. This bundled file is the user-selected source of truth.

## Rules

- Treat `theme-fiber-paper.jpg` as the only approved lower paper asset.
- Do not use the legacy `reference-fiber-paper.jpg` file, even if it remains in the package.
- Derive a softened representative theme color from the current source photo.
- Center-cover-crop the paper to the lower panel; never stretch it.
- Map the paper's average RGB to the derived theme while retaining its original luminance detail, fibers, pulp inclusions, short dark strands, small marks, scan softness, and local variation.
- With a selected Python/Pillow backend, use `scripts/recolor_theme_paper.py` for deterministic centered cropping and theme mapping. It requires Pillow but not NumPy and intentionally has no paper override option.
- With another image backend, reproduce the same operation: center-cover-crop the fixed paper; compute Rec. 709 luminance (`0.2126 R + 0.7152 G + 0.0722 B`); retain `72%` of luminance deviation and `8%` of source chroma around the target RGB; then correct the channel means toward the target before clipping. Do not approximate this with a flat color overlay.
- Do not generate, repaint, denoise, blur away, or procedurally synthesize the texture.
- Composite the real subject, Japanese lettering, and connector above the recolored paper.
- Do not substitute another scan or fall back to a flat color.
- If the asset is missing or unreadable, stop and report that the Skill installation is incomplete.
