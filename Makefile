update_conf: 
	./build_utils/gen-pyproject.sh

test:update_conf 
	coverage run -m pytest
	coverage report -m

build: test
	rm -rf dist/
	python -m build .
	tox

tag: build
	bash build_utils/git-tag.sh

deploy_test:
	twine upload -r testpypi dist/* --verbose
	
deploy_prod:
	twine upload dist/*