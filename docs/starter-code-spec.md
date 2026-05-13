# Starter Code Spec: Sports Bet Copilot

## Monorepo Layout

```text
sports-bet-copilot/
  apps/
    api/
    worker/
    web/
  packages/
    schemas/
    prompts/
    ml/
  infra/
    docker/
    terraform/
  ops/
    scripts/
  tests/
    integration/
    e2e/
```

## FastAPI Skeleton

```text
apps/api/src/
  main.py
  core/config.py
  db/session.py
  db/models/
  schemas/
  services/
  api/routers/
```

## Worker Skeleton

```text
apps/worker/src/
  celery_app.py
  tasks/
    ingest_markets.py
    ingest_sports_context.py
    compute_features.py
    run_predictions.py
    compute_edges.py
    ingest_media.py
    extract_claims.py
    evaluate_claims.py
```

## Initial DB Tables

- `events`
- `markets`
- `market_ticks`
- `model_predictions`
- `edges`
- `recommendations`
- `combo_legs`
- `media_items`
- `media_claims`
- `claim_evaluations`

## API Contracts (v1)

- `GET /health`
- `GET /markets/live`
- `GET /markets/{market_id}`
- `GET /markets/{market_id}/mispricing`
- `GET /recommendations/top`
- `POST /combos/generate`
- `POST /combos/tweak`
- `POST /media/ingest`
- `GET /media/{id}/claims`
- `GET /claims/{id}/evaluation`

## Scoring Starter Logic

- `edge = p_model - p_market`
- `value_score = 0.55*edge + 0.20*liquidity - 0.15*volatility - 0.10*uncertainty`
- Staking uses fractional Kelly with hard max exposure caps.

## Media Claim Extraction JSON

```json
{
  "claims": [
    {
      "claim_text": "Team X is 8-1 on back-to-backs",
      "entity_tags": ["Team X"],
      "metric": "win_rate",
      "time_horizon": "last_9_back_to_back_games",
      "league": "NBA",
      "confidence_extract": 0.88
    }
  ]
}
```

## Environment Variables

```env
APP_ENV=dev
DATABASE_URL=postgresql+psycopg://...
REDIS_URL=redis://redis:6379/0
OPENAI_API_KEY=...
MARKET_API_KEY=...
SPORTS_DATA_API_KEY=...
JWT_SECRET=...
```

## Make Targets

- `make up`
- `make down`
- `make migrate`
- `make test`
- `make lint`

## First 10 Tickets

1. Scaffold monorepo and CI
2. Add SQLAlchemy models + Alembic migrations
3. Implement health + market endpoints
4. Build market ingestion worker
5. Add feature pipeline stub
6. Implement prediction + edge services
7. Build top recommendations endpoint
8. Implement combo generation and constraints
9. Add media ingest + claim extraction
10. Add risk controls and audit log


## Integrity / Fairness Analyzer (Anti-Cheating)

- Add `GET /integrity/{market_id}/report` to audit potentially harmful platform behavior.
- Track suspicious patterns such as spread widening against retail flow, asymmetric fill latency, and unexplained quote pulls.
- Treat this component as compliance protection for customers, not as a betting exploit mechanism.


## False-Odds / Mispricing Analyzer

- Compare model probability vs implied market probability to flag potential false-odds trades.
- Add action labels (`consider_buy`, `consider_sell_or_hedge`, `no_trade`, `hold_low_confidence`) with confidence gating to avoid overtrading.
- This is intended for legitimate market-making/trading decisions, not manipulation or platform abuse.
