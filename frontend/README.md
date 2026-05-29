# Frontend

This directory contains the React source for the API-first SPA migration. React is still part of the AlertaDengue plan, but the first migration work should be Django/DRF API contracts and database/query modeling for the data that the frontend will consume.

Django remains the stable backend during the transition: existing routes, templates, reports, maps, auth/session behavior, i18n, cache policy, and staticfiles continue to work while API contracts are extracted route by route.

## Layout

```text
src/
  entries/    Vite entrypoints. `app.tsx` is a placeholder until SPA routes exist.
  api/        Typed fetch clients for Django/DRF endpoints.
  pages/      Page-specific React routes/components once their API contracts exist.
  components/ Shared React UI components after duplication appears.
  styles/     Shared or route-scoped CSS.
```

The frontend source stays at repository root under `frontend/`. Build output goes to `AlertaDengue/static/frontend/` so Django can serve it through the normal staticfiles pipeline while deployment remains unified.

## Migration Order

1. Map high-use data surfaces and existing SQL/pandas queries.
2. Add unmanaged models where they help, starting with central tables such as `Notificacao` and `Historico_alerta*`; keep service/query layers where ORM models are not practical yet.
3. Create stable API contracts for the frontend, starting with home chart data.
4. Migrate pages route by route when their API contracts are ready.
5. Use transitional React islands only if a highly coupled Django page would otherwise block delivery.

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

`makim reactjs.build` runs the TypeScript check and Vite production build. `makim tests.reactjs` currently runs the install/build checks; add a real frontend unit-test command once a test runner and `frontend/tests/` suite exist.

`npm run build` writes generated assets to `AlertaDengue/static/frontend/`. Do not edit generated files manually.
