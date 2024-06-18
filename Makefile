.DEFAULT_GOAL := help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


install: ## Install dependencies
	@poetry install
	@mkdir ~/.config/kandy
	@echo "default:" >> ~/.config/kandy/hosts.yaml
	@echo "  host: localhost" >> ~/.config/kandy/hosts.yaml
	@echo "  port: 29092" >> ~/.config/kandy/hosts.yaml

start_kafka: ## Start local kafka docker
	docker-compose -f docker-compose.kafka.yaml up -d --build --remove-orphans --wait

stop_kafka: ## Stop local kafka docker
	@docker-compose -f docker-compose.kafka.yaml down

test_unit: ## Run unit tests
	@poetry run pytest tests/unit 

test_behaviour: ## Run behaviour tests
	@poetry run pytest tests/step_defs
	
test_integration: start_kafka ## Run integration_test tests
	-@poetry run pytest tests/integration -vv
	@$(MAKE) stop_kafka

test: start_kafka ## Run all tests
	-@poetry run pytest 
	@$(MAKE) stop_kafka

run: ## Run the application
	@poetry run python -m kandy default -h
