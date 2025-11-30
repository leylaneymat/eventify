start:
	pip3 install pip-tools

update:
	pip3 install --upgrade pip pip-tools
	python3 -m piptools compile --no-upgrade --output-file requirements.txt --resolver=backtracking pyproject.toml

upgrade:
	python3 -m piptools compile --upgrade --output-file requirements.txt --resolver=backtracking pyproject.toml

install: update
	python3 -m piptools sync requirements.txt
	rm -r ./src/src.egg-info

welcome: start install
