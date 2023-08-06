default: build

# Dependencies

bootstrap:
	pip install -e .[dev]

bootstrap-release:
	pip install -e .

.PHONY: bootstrap bootstrap-release

# Build

build:
	python manage.py collectstatic --noinput

release:
	fullrelease

.PHONY: build release

# Quality

lint: check-manifest


check-manifest:
	check-manifest


.PHONY: lint check-manifest
