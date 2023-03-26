# Install for production
install:
	@echo Installing dependencies
	python -m pip install --upgrade pip
	python -m pip install -e .

# Install for development
install-dev: install
	@echo Installing development dependencies
	python -m pip install -e ".[dev]"

# Install documentation dependencies
install-doc: install
	@echo Installing documentation dependencies
	python -m pip install -e ".[doc]"

# build python wheel
build: build
	@echo building wheel
	pip install --upgrade build
	python -m build


# documentation build, by default it will be html
# we use autobuild, so it does not require a reload and build command each time
docs-build:
	sphinx-autobuild -b html docs/source/ docs/build/html
