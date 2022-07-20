VERSION := $(shell python3 -c 'import CircleciLibrary; print(CircleciLibrary.__version__)')

checkout_current_version:
	git fetch --all --tags
	git checkout $(VERSION)

test: checkout_current_version
	python3 setup.py install
	tox

clean:
	rm -rf dist

build: test
	pip install wheel twine
	python3 setup.py bdist_wheel sdist

test_deploy: build
	twine upload --repository pip-test-account  dist/*

deploy: build
	twine upload --repository pip-prod-account  dist/*

generate-docs:
	export INIT_FOR_LIBDOC_ONLY=1 && python3 -m robot.libdoc --docformat rest  CircleciLibrary/ docs/index.html
