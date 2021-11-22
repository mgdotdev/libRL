.PHONY: test
test:
	python -m pytest --pdb
	
cov:
	coverage run --source=src -m pytest && coverage report -m
