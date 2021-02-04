paths = aptdepends tests

isort:
	isort $(paths)

black:
	black $(paths)

format: black isort

mypy:
	mypy $(paths)

check: mypy

all: format check
