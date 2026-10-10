# AuroraView Gallery

Interactive showcase of [AuroraView](https://github.com/try-auroraview/auroraview)
features, examples and components.

![AuroraView Gallery](gallery_screenshot.png)

Gallery is a full AuroraView application: a Python host (`main.py` plus the
`backend/` package) driving a React + Vite frontend (`src/`). It is the app the
team uses to demo and exercise the framework, and it lives in its own
repository so it can iterate independently of framework releases.

## Layout

| Path | What it is |
| --- | --- |
| `main.py` | Entry point. Boots the WebView, registers backend APIs. |
| `backend/` | Python host: process management, child windows, browser features, telemetry, dependency checks. |
| `src/` | React + Vite frontend. |
| `examples/` | AuroraView samples shown in the gallery. Vendored — see below. |
| `assets/icons/` | App icons used when packing. |
| `auroraview.pack.toml` | Packaging config for the standalone executable. |

## Quick start

```bash
# Python host (3.11 recommended, matches auroraview.pack.toml)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Frontend
npm ci
npm run build          # produces dist/, which the host loads

# Run
python main.py
```

For frontend iteration with hot reload, run `npm run dev` in one shell and
`python main.py` in another; the host loads `dist/` and Vite serves the dev
server independently.

## Relationship to the framework

Gallery depends on AuroraView through published packages only:

- **Python** — [`auroraview`](https://pypi.org/project/auroraview/) from PyPI.
- **Frontend** — [`@auroraview/sdk`](https://www.npmjs.com/package/@auroraview/sdk) from npm.

Nothing here reaches outside this repository for source. The AI Agent sidebar is
the one exception: `auroraview-ai` is not published yet, so that panel stays
disabled unless you point `AURORAVIEW_AI_SRC` at a local framework checkout.
Both `backend/__init__.py` and `main.py` handle the missing import gracefully.

## The vendored `examples/` directory

`examples/` is a copy of the samples from `try-auroraview/auroraview`, so a fresh
clone works with no setup. To develop against the upstream samples instead, point
the host at a live checkout — no code change needed:

```bash
export AURORAVIEW_EXAMPLES_DIR=/path/to/auroraview/examples
python main.py
```

Refresh the vendored copy from upstream with:

```bash
python scripts/sync_examples.py /path/to/auroraview
```

The script reports what changed and records the upstream commit it synced from.

## Known gap: packing

`auroraview.pack.toml` is carried over from the framework repo, but Gallery
cannot pack itself yet. The `pack` command lives in the Rust `auroraview-cli`
binary, which is built from `try-auroraview/auroraview` and is not published to
PyPI or npm. The PyPI `auroraview` command is only a WebView launcher.

Until `auroraview-cli` is published, build the distributable from the framework
repo. See [issue tracking](https://github.com/try-auroraview/auroraview-gallery/issues)
for progress.

## Known debt

Gallery was never linted in CI while it lived in the framework monorepo, and the
extraction carried 16 pre-existing lint errors with it.

Four were unused-variable errors that were intentional — the bindings are
underscore-prefixed and kept for signature symmetry — so `eslint.config.js` now
honours that convention. The remaining twelve (`any` types, a `react-refresh`
export, and two `react-hooks/set-state-in-effect` findings) are downgraded to
warnings so they stay visible without blocking CI.

They are real and should be paid down; none was introduced by the extraction.
Run `npm run lint` to see the current list.

## Development

```bash
just install   # npm ci
just build     # build the frontend
just lint      # eslint
just check     # build + lint + python checks
```

Commits follow Conventional Commits.

## License

[MIT](LICENSE)
