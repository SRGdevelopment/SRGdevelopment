# Vertical Branching Strategy

To keep automotive and sports development isolated, use separate long-lived branches:

- `vertical/sports` for all sports-specific features and data providers.
- `vertical/auto` for all automotive-specific features and data providers.

## Environment split

Set `APP_VERTICAL` so runtime identity and defaults are scoped per branch:

- `sports` (default)
- `auto`

When `APP_VERTICAL=auto`, the API/worker names and local database filename are auto-scoped.

## Suggested workflow

1. Branch from `main` into `vertical/sports` and `vertical/auto`.
2. Keep shared platform work in short-lived feature branches and merge into both vertical branches as needed.
3. Keep vertical-only endpoints/tasks behind `APP_VERTICAL` checks to avoid cross-domain leakage.
