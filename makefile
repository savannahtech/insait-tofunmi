# Makefile for Flask API Project

.PHONY: help setup build run test migrate clean logs

# Variables
CONTAINER_NAME := $(shell docker-compose ps -q web 2>/dev/null)
ENV_FILE := .env.sample

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup:
	@if [ ! -f .env ]; then \
		cp $(ENV_FILE) .env; \
		echo "Created .env file. Please update with your configurations."; \
	fi

build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

test:
	@if [ -z "$(CONTAINER_NAME)" ]; then \
		echo "Container is not running. Starting services..."; \
		make run; \
		sleep 5; \
	fi
	docker exec -it $(CONTAINER_NAME) pytest

migrate-init:
	docker exec -it $(CONTAINER_NAME) flask db init

migrate:
	docker exec -it $(CONTAINER_NAME) flask db migrate -m "$(message)"

upgrade:
	docker exec -it $(CONTAINER_NAME) flask db upgrade

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	rm -rf migrations
	find . -type d -name __pycache__ -exec rm -r {} +

ps:
	docker-compose ps