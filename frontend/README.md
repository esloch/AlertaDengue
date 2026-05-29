# Frontend

This directory contains React source mounted as islands inside Django-rendered pages. Django still owns routing, authentication, i18n, cache policy, and the base HTML shell.

## Layout

```text
src/
  entries/    Vite entrypoints. Keep these small.
  pages/      Page-specific React components and types.
  lib/        Shared browser utilities, including React island mounting.
  styles/     Page or island scoped CSS.
  api/        Typed fetch clients for JSON endpoints when needed.
```

## Commands

```bash
npm run typecheck
npm run build
```

`npm run build` writes generated assets to `AlertaDengue/static/frontend/`. Do not edit generated files manually.

## Django Integration

Use the shared templates:

- `AlertaDengue/templates/components/react_assets.html` for CSS and JS assets.
- `AlertaDengue/templates/components/react_mount.html` for the mount element and `json_script` props.

React entrypoints should use `mountReactIsland` from `src/lib/reactIsland.tsx`.
