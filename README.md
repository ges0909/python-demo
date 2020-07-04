# Python

## Python installation

- [Python 3](https://www.python.org/downloads/) installation on local machine

## Pyenv installation

- `git clone https://github.com/pyenv-win/pyenv-win.git %USERPROFILE%/.pyenv`
- add to PATH:
    - `%USERPROFILE%\.pyenv\pyenv-win\bin`
    - `%USERPROFILE%\.pyenv\pyenv-win\shims`
- test installation: `pyenv --version`
- update (required to get offered new python versions)
    - `cd %USERPROFILE%/.pyenv/pyenv-win`
    - `git pull`
 
### Pyenv commands

- `pyenv local`
- `pyenv install --list`
- `pyenv install 3.7.4`
- `pyenv uninstall 3.7.4`
- `pyenv version`
- set python version globally: `pyenv global 3.7.4`
- set python version locally: `pyenv global 3.7.4`
    -  will be automatically activated by entering the folder

- run python's built-in test suite: `python -m test`

## Virtual Environment

- _virtual_ == **isolated** project environment

Project Setup

- `git clone <project url>`
- `cd <project>`
- create virtual env: `python -m venv venv`
- enter virtual env: `venv\Scripts\activate.bat`
- test virtual env: `where python`
- install project dependencies: `pip install -r requirements.txt`
- freeze project dependencies: `pip freeze > requirements.txt` 
- leave virtual env: `deactivate`

## Tox

- `pip install tox`
- `tox`
