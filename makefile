all: black

black:
	black .

requirements:
	pip install -r requirements-dev.txt
