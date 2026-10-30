**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](https://github.com/heygen-com/hyperframes/blob/HEAD/skills/hyperframes-core/../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames Core

**Agent pitfalls (read first):**

* Center with flex/`inset`, not CSS `transform: translate(-50%,-50%)` on a node you then GSAP `x`/`y`. Lint: `gsap_css_transform_conflict`. Use `fromTo` or `xPercent`/`yPercent`.
* Do not add a scene-exit `tl.set(..., {visibility:"hidden"})`. The runtime already hides timed clips. Opacity fades on inner nodes (or `opacity` on `.clip`) are enough. Caption hard-kills are a different rule.
* `window.__timelines["id"]` must match the root `data-composition-id`.
* After `render`, read the summary's second line: `beginframe` vs `screenshot`, GPU mode, stage timings. `screenshot` + `software gpu` on Linux is the slow path.

HyperFrames renders video from HTML. A composition is an HTML file whose DOM declares timing with `data-*` attributes, whose animation runtime is seekable, and whose media playback is owned by the framework.

This skill is the **technical contract** — how to build one hyperframes project. The body below is the build guide; per-topic detail lives in `references/` (index next), read on demand. Process docs (brief, storyboard, review, production, dispatch, frame-worker) live in `/hyperframes` → `references/`. Other concerns live in the sibling domain skills — `hyperframes-animation`, `hyperframes-creative`, `media-use`, `hyperframes-cli`, `hyperframes-registry`. The capability map in `/hyperframes` says what each one covers.

## References