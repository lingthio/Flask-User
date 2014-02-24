from fabric.operations import local
from fabric.api import cd, env, task, prefix, run
from contextlib import contextmanager

@task
def runserver():
    local('python runserver.py')

@task
def test():
    local('py.test --tb short -v -s tests')

@task
def coverage():
    local('coverage run --source=flask_user tests/conftest.py')
    local('coverage report -m')

@task
def babel():
    local('pybabel extract -F misc/babel.cfg -c NOTE -o misc/messages.pot flask_user example_app')
    local('pybabel update -i misc/messages.pot -d example_app/translations -l en')
    local('pybabel update -i misc/messages.pot -d example_app/translations -l nl')
    local('pybabel compile -f -d example_app/translations')

@task
def docs():
    local('touch docs/source/*.rst')
    local('sphinx-build -b html docs/source docs/build')
    local('cd docs/build && zip -u -r docs *')

@task
def release_to_pypi():
    local('python setup.py sdist upload')