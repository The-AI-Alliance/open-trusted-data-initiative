PYTHON?=python
DOCKER?=docker

.PHONY: install
.PHONY: samples run_python_samples run_ray_samples
.PHONY: tests run_python_tests run_ray_tests
.PHONY: images build_python_image build_ray_image

samples:: run_python_samples run_ray_samples
tests::   run_python_tests run_ray_tests
images::  build_python_image build_ray_image

install::
	pip install --no-cache-dir -e .

run_python_samples::
	pip install --no-cache-dir -e .
	${PYTHON} src/license_validator/python/license_validator_local.py
	${PYTHON} src/license_validator/python/license_validator_local_python.py

run_python_tests::
	pip install --no-cache-dir -e .
	pytest test/python

build_python_image::
	${DOCKER} build . -t license_validator_python -f Dockerfile_python

run_ray_samples::
	pip install --no-cache-dir -e .
	${PYTHON} src/license_validator/ray/license_validator_local_ray.py

run_ray_tests::
	pip install --no-cache-dir -e .
	pytest test/ray


build_ray_image::
	${DOCKER} build . -t license_validator_python -f Dockerfile_ray
