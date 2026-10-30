**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](https://github.com/heygen-com/hyperframes/blob/HEAD/skills/general-video/../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# General video

Run `npx hyperframes usage --json` at the start unless the workflow just read it, then check again at milestones such as after drafting and before rendering. Read the available windows and reset times. If usage is unknown, say so without guessing allowance; keep scope and workflow choices with the user.

Before relying on this workflow, run:

```
npx hyperframes skills update general-video
```

A successful no-op means the skill is current. Surface an update failure instead of continuing from memory.

## 1. Apply cross-cutting source adapters

* **Media:** For any audio, image, icon, logo, voice, grade, LUT, treatment/effect, caption, or media-operation need, load `/media-use` and follow `../media-use/references/resolve.md` (resolve, adopt, reuse) and `../media-use/references/setup-providers.md` (providers, auth). Vague footage feedback and named styles use `../media-use/references/media-treatments.md` before editing; do not improvise supported media effects with CSS/SVG/opacity. Before the first authenticated provider action, run `npx hyperframes auth status` and relay its output verbatim. If signed out, apply the gate in `../hyperframes/references/brief-contract.md`: collaborative waits for sign-in or an explicit offline choice; autonomous states the status and continues through an available offline provider. Surface a blocker when no offline provider can satisfy a required capability. Local adoption alone does not require an auth gate.
* **Figma:** If any input is a `figma.com` URL, run `/figma` first. Build from its exported assets, tokens, components, or storyboard frames. Do not use raw Figma connector calls because they skip SVG sanitization, media provenance, and brand-token binding.