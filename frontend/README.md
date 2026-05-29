# Frontend

This directory contains the React source used by Django-mounted islands. Django still owns routing, authentication, i18n, cache policy, and the base HTML shell. This is intentionally different from LiteRev's SPA direction: AlertaDengue is migrating progressively because existing Django templates, public URLs, maps, charts, reports, and upload flows need to remain stable.

## Layout

```text
src/
  entries/    Vite entrypoints. Keep these small.
  pages/      Page-specific React components and types.
  lib/        Shared browser utilities, including React island mounting.
  styles/     Page or island scoped CSS.
  api/        Typed fetch clients for JSON endpoints when needed.
```

The frontend source stays at repository root under `frontend/`. Build output goes to `AlertaDengue/static/frontend/` so Django can serve it through the normal staticfiles pipeline.

## Commands

Prefer the makim wrappers so frontend work fits the repository workflow:

```bash
makim reactjs.install
makim reactjs.build
makim tests.reactjs
makim django.collectstatic
```

Direct npm commands are still useful while developing:

```bash
npm run typecheck
npm run build
```

`makim reactjs.build` runs the TypeScript check and Vite production build. `makim tests.reactjs` currently runs the install/build checks; add a real frontend unit-test command there once a test runner and `frontend/tests/` suite exist.

`npm run build` writes generated assets to `AlertaDengue/static/frontend/`. Do not edit generated files manually.

## Django Integration

Use the shared templates:

- `AlertaDengue/templates/components/react_assets.html` for CSS and JS assets.
- `AlertaDengue/templates/components/react_mount.html` for the mount element and `json_script` props.

React entrypoints should use `mountReactIsland` from `src/lib/reactIsland.tsx`.
