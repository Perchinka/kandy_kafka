.DEFAULT_GOAL := help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


install: ## Install dependencies
	@poetry install

start_kafka: ## Start local kafka
	@docker-compose -f docker-compose.kafka.yaml up -d

stop_kafka: ## Stop local kafka
	@docker-compose -f docker-compose.kafka.yaml down

test: ## Run tests
	@poetry run pytest tests/