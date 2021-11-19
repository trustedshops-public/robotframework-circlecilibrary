VERSION := $(shell python3 -c 'import CircleciLibrary; print(CircleciLibrary.__version__)')

checkout_current_version:
	git fetch --all --tags
	git checkout $(VERSION)

test: checkout_current_version
	python3 setup.py install
	pip install tox
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