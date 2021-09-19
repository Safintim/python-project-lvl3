install:
	poetry install

test:
	poetry run pytest -s

test-coverage:
	poetry run pytest --cov=page_loader --cov-report term

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck test lint

format-code:
	black .
	isort .

build:
	poetry build

clean-build:
	rm -rf dist

publish:
	poetry publish --dry-run

publish-testpypi:
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish -r testpypi

package-install:
	python3 -m pip install --user dist/*.whl
