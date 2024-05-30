.DEFAULT_GOAL := help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


install: ## Install dependencies
	@poetry install

start_kafka: ## Start local kafka docker
	@docker-compose -f docker-compose.kafka.yaml up -d --build

stop_kafka: ## Stop local kafka docker
	@docker-compose -f docker-compose.kafka.yaml down

test: ## Run tests
	@poetry run pytest tests/unit tests/step_defs
	
integration_test: start_kafka ## Run integration_test tests
	-@poetry run pytest
	@$(MAKE) stop_kafka

run: ## Run the application
	@poetry run python -m kandy
