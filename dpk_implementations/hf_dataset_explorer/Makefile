PYTHON?=python
DOCKER?=docker

run_python_samples::
	pip install --no-cache-dir -e .
	${PYTHON} src/hf_dataset_explorer/python/dataset_explorer_local.py
	${PYTHON} src/hf_dataset_explorer/python/dataset_explorer_local_python.py

run_python_tests::
	pip install --no-cache-dir -e .
	pytest test/python

build_python_image::
	${DOCKER} build . -t hf_dataset_explorer_python -f Dockerfile_python

run_ray_samples::
	pip install --no-cache-dir -e .
	${PYTHON} src/hf_dataset_explorer/ray/dataset_explorer_local_ray.py

run_ray_tests::
	pip install --no-cache-dir -e .
	pytest test/ray


build_ray_image::
	${DOCKER} build . -t hf_dataset_explorer_python -f Dockerfile_python