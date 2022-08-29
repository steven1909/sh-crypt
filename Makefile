test: 
	coverage run -m pytest
	coverage report -m

build: test
	python build_utils/gen_setup.py
	python -m build .

tag: test build
	bash build_utils/git-tag.sh

deploy_test:
	twine upload -r testpypi dist/*
	
deploy_prod:
	twine upload dist/*