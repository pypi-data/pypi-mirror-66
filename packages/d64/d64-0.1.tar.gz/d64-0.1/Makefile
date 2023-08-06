.PHONY: install
install:
	pip3 install . --upgrade

.PHONY: unittest
unittest:
	PYTHONPATH=$(PYTHONPATH):d64 python3 -m unittest discover -s test -v

.PHONY: lint
lint:
	flake8 d64
