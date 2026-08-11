# Redthread Plugin Submission Draft

## Listing

- Name: Redthread
- Type: Skills only
- Category: Creative
- Short description: Turn one portrait into a poetic red-thread collage.
- Website: https://github.com/HuHana77/redthread
- Support: https://github.com/HuHana77/redthread/blob/main/SUPPORT.md
- Privacy: https://github.com/HuHana77/redthread/blob/main/PRIVACY.md
- Terms: https://github.com/HuHana77/redthread/blob/main/TERMS.md
- Availability: All countries and regions where ChatGPT and Codex plugins are supported
- Release notes: Initial public submission of the Redthread portrait-collage workflow.

## Long description

Redthread creates a finished 3:4 two-panel editorial collage from one user-supplied portrait. It preserves the real subject, reuses one canonical cutout in both scenes, derives a matching paper palette, adds bilingual hand-lettering, and connects corresponding subject anchors with a restrained wine-red pencil line. The plugin exposes only the final inspected PNG and keeps cutouts, masks, connector layers, and QA thumbnails private.

## Positive test cases

1. Given a portrait with a visible little finger, create a complete collage and connect both subject copies at the corresponding little-finger point.
2. Given a portrait without a visible little finger, select one clear corresponding contour tip and keep that anchor through the final render.
3. Given a pet photo, use one corresponding non-human contour tip and preserve the animal's identity and anatomy.
4. Revise an existing Redthread collage by changing the theme color while preserving subject scale, anchor, paper texture, and typography rules.
5. Given a portrait with reflective glasses and a held prop, preserve both details and keep text and connector away from protected regions.

## Negative test cases

1. A user asks to expose the cutout, masks, connector layer, and QA thumbnail; refuse to expose intermediates and deliver only the final collage.
2. A user supplies no source photo and asks for a named real person's portrait; request a user-supplied photo instead of fabricating the source subject.
3. A user asks to replace the bundled paper, font, or connector template with an arbitrary substitute; preserve required assets unless the user is explicitly revising the plugin itself.
