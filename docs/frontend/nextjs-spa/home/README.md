# Home Route Dependency Map for Next.js/SPA Migration

Date: 2026-05-29

This document maps the current Django-rendered home route before moving it to
a route-by-route Next.js/SPA implementation. The goal is to make the home page
API contract explicit before replacing templates or browser behavior.

## Route Surface

| Route | Django owner | Current response | Cache |
| --- | --- | --- | --- |
| `/` | `dados.urls` -> `AlertaMainView` | `dados/templates/main.html` | 1 hour |
| `/chartshome/<UF>` | `dados.urls` -> `ChartsMainView` | HTML fragment `components/home/home_state_charts.html` | 1 hour |

The Next.js home route should keep `/` as the public URL. During migration,
Django can continue to own `/chartshome/<UF>` until a JSON replacement exists.

## Current Template Components

`main.html` is a shell that renders inclusion tags from
`dados/templatetags/home_components.py`.

| Component | Template | Dynamic data today | Notes for SPA |
| --- | --- | --- | --- |
| Banners | `components/home/home_banners_section.html` | Current language code and static SVG assets | Can become static/i18n content in Next.js. |
| Functionalities | `components/home/home_functionalities_section.html` | None from backend | Preserve links, tooltips, and PWA install behavior. |
| Other products | `components/home/home_other_products_section.html` | None from backend | Static/i18n content. |
| UF incidence | `components/home/home_uf_incidence_section.html` | Static country incidence PNG files | Keep static asset contract or expose map metadata. |
| State epidemiological charts | `components/home/home_state_epi_section.html` | `STATE_NAME` / state abbreviations | Owns AJAX call to `/chartshome/<UF>`. |
| State chart fragment | `components/home/home_state_charts.html` | `ChartsMainView` context | Main backend data dependency. |

## Browser Dependencies

The current home page depends on:

- jQuery for `$.ajax`, document-ready behavior, and Bootstrap tooltip setup.
- Bootstrap tabs, carousel, and tooltip behavior.
- Plotly loaded from CDN in `main.html`.
- Font Awesome from CDN plus local static SVG/PNG assets.
- PWA `beforeinstallprompt`, `appinstalled`, and `localStorage` behavior in
  `home_functionalities_section.html`.

The Next.js route should replace the HTML-fragment AJAX flow with a JSON API
and client components for state selection, disease tabs, charts, maps, and PWA
install state.

## AJAX and Data Endpoints

### Existing Endpoint

`GET /chartshome/<UF>`

Inputs:

- `<UF>`: state abbreviation from `STATE_NAME` (`AC`, `AL`, ..., `TO`).

Current output:

- Server-rendered HTML containing disease tabs, three Plotly charts per
  disease, incidence map images, monitored-city counts, latest SE label, and
  state alert links.

Current default:

- `home_state_epi_section.html` loads `RJ` on first render.

### Proposed JSON Replacement

Add a versioned backend endpoint before replacing the route:

`GET /api/internal/home/states/<UF>/summary/`

Suggested shape:

```json
{
  "state": {"abbr": "RJ", "name": "Rio de Janeiro"},
  "last_update": {"epiweek": 202420, "label": "20/2024"},
  "diseases": {
    "dengue": {
      "monitored_city_count": 92,
      "series": [{"epiweek": 202420, "cases": 10, "estimated_cases": 12.4}],
      "receptive_city_count": {"current": 30, "previous": 28, "total": 92},
      "alert_level_counts": [
        {"epiweek": 202420, "green": 60, "yellow": 20, "orange": 10, "red": 2}
      ],
      "incidence_map_url": "/static/img/incidence_maps/state/incidence_RJ_dengue.png",
      "detail_url": "/alerta/RJ/dengue"
    }
  }
}
```

This endpoint should return data, not Plotly HTML. Next.js should render charts
client-side from the JSON.

## Tables and Views Used by Home

`ChartsMainView` currently reads through `dados.dbdata`.

| Purpose | Current helper | Database object | New model |
| --- | --- | --- | --- |
| State/city history for dengue | `data_hist_uf(..., "dengue")` | `public.hist_uf_dengue_materialized_view` | `HomeUfHistoryDengue` |
| State/city history for chikungunya | `data_hist_uf(..., "chikungunya")` | `public.hist_uf_chik_materialized_view` | `HomeUfHistoryChikungunya` |
| State/city history for zika | `data_hist_uf(..., "zika")` | `public.hist_uf_zika_materialized_view` | `HomeUfHistoryZika` |
| Monitored city count by UF/disease | `NotificationResume.count_cities_by_uf` | `public.city_count_by_uf_<disease>_materialized_view` | `HomeCityCountByUf*` |
| State names and UF mapping | `STATE_NAME`, `ALL_STATE_NAMES` | Python constants | Keep as constants or expose as API metadata. |

Underlying materialized views are built from:

- `"Municipio"."Historico_alerta"`
- `"Municipio"."Historico_alerta_chik"`
- `"Municipio"."Historico_alerta_zika"`
- `"Dengue_global"."Municipio"`
- `"Dengue_global".estado`

The first unmanaged model pass maps the materialized views used directly by the
home route. Direct models for the underlying `Historico_alerta*` tables can be
added when the JSON endpoint needs row-level alert history outside the existing
views.

## Static Assets Used by Home

| Asset pattern | Used by | Notes |
| --- | --- | --- |
| `img/home/banners/banner_home_<lang>.svg` | Banners | Language suffix from Django language code. |
| `img/home/banners/banner_report_<lang>.svg` | Banners | External Zenodo link. |
| `img/home/features/episcanner.svg` | Other products | Product tile. |
| `img/incidence_maps/country/incidence_Nacional_dengue.png` | UF incidence section | Static country map. |
| `img/incidence_maps/country/incidence_Nacional_chikungunya.png` | UF incidence section | Static country map. |
| `img/incidence_maps/state/incidence_<UF>_<disease>.png` | State chart fragment | One image per UF/disease. |

## Phase 2: Backend Contract

The next migration step is to add a backend service/query layer and an internal
JSON endpoint for the home state summary. That endpoint should use the unmanaged
home models, return chart-ready data, and preserve the legacy `/chartshome/<UF>`
HTML fragment until the Next.js route reaches parity.

## Migration Checklist

1. Keep Django-rendered `/` and `/chartshome/<UF>` stable while adding JSON.
2. Use the unmanaged home models in a query/service layer for the new endpoint.
3. Add API tests that verify state filtering, disease keys, latest SE label,
   monitored-city counts, and empty-data behavior.
4. Build the Next.js home route against the JSON endpoint.
5. Replace jQuery/Bootstrap fragment behavior with React state and chart
   components.
6. Switch `/` to the Next.js route only after parity is verified for default
   `RJ`, all disease tabs, state maps, PWA install tile, and translated static
   content.
