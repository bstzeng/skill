**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](https://github.com/heygen-com/hyperframes/blob/HEAD/skills/hyperframes-keyframes/../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames Keyframes

Keyframes are a pose contract: visible states, continuous subject identity, seek-safe runtime, verified pixels.

Use `hyperframes-animation` for broad scene recipes. Use `hyperframes-cli` for full command docs. Use `references/keyframe-patterns.md` only when choosing implementation mechanisms, not visual style.

## Creator editing boundary

Keyframes own visual motion, not clip assembly. Source-range hard cuts, trim,
splice, and reorder belong to `/hyperframes-core`: author one media element per
kept range, place it with `data-start` and `data-duration`, and select its source
offset with `data-media-start`. Adjacent ranges make a hard cut. A crossfade
uses overlapping clips on different tracks plus visual opacity keyframes; sound
fades use `/hyperframes-audio`.