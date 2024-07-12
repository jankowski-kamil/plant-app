ifeq ($(PROD),true)
	DOCKER_COMPOSE = docker-compose -f production.yml
else
	DOCKER_COMPOSE = docker compose -f local.yml
endif

DOCKER_RUN = $(DOCKER_COMPOSE) run --rm django
RUN_MANAGE_PY = $(DOCKER_RUN) python manage.py

up:
	$(DOCKER_COMPOSE) up --force-recreate $(service)

build:
	$(DOCKER_COMPOSE) build

down:
	$(DOCKER_COMPOSE) down

down-v:
	$(DOCKER_COMPOSE) down -v

migrate:
	$(RUN_MANAGE_PY) migrate

makemigrations:
	$(RUN_MANAGE_PY) makemigrations

createsuperuser:
	$(RUN_MANAGE_PY) createsuperuser

startapp:
	$(DOCKER_RUN) bash -c "cd plant/ && python ../manage.py startapp $(app)"

shell:
	$(DOCKER_COMPOSE) exec -it django bash

mypy:
	$(DOCKER_RUN) mypy .

test:
	$(DOCKER_RUN) pytest

