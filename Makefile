.PHONY: up down api worker migrate makemigration test lint validate-engine-assets

up:
	docker compose up --build

down:
	docker compose down

api:
	uvicorn apps.api.src.main:app --reload --host 0.0.0.0 --port 8000

worker:
	celery -A apps.worker.src.celery_app.celery_app worker -l info

migrate:
	alembic upgrade head

makemigration:
	alembic revision --autogenerate -m "init"

test:
	pytest -q

lint:
	ruff check .

validate-engine-assets:
	python3 packages/engine-bay-assets/scripts/validate_manifest.py apps/engine-bay-web/public/assets/sample-engine-bay/manifest.json
