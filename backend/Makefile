start:
	pip install pip-tools

update:
	pip install --upgrade pip pip-tools
	pip-compile --no-upgrade --output-file requirements.txt --resolver=backtracking pyproject.toml

upgrade:
	pip-compile --upgrade --output-file requirements.txt --resolver=backtracking pyproject.toml

install: update
	pip-sync requirements.txt
	rm -r ./src/src.egg-info

welcome: start install
