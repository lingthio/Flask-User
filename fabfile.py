from fabric.operations import local
from fabric.api import cd, env, task, prefix, run
from contextlib import contextmanager

@task
def runserver():
    local('python runserver.py')

@task
def test():
    # Requires "pip install pytest"
    local('py.test flask_user/tests/')

@task
def coverage():
    # Requires "pip install pytest-coverage"
    local('py.test --cov flask_user --cov-report term-missing --cov-config flask_user/tests/.coveragerc flask_user/tests/')

@task
def babel():
    local('pybabel extract -F flask_user/translations/babel.cfg -c NOTE -o flask_user/translations/flask_user.pot flask_user flask_user')
    for code in ('en', 'fi', 'fr', 'nl', 'sv', 'zh'):
        local('pybabel update -i flask_user/translations/flask_user.pot --domain=flask_user --output-dir flask_user/translations -l '+code)
    local('pybabel compile -f --domain=flask_user --directory flask_user/translations')

@task
def babel_init():
    local('pybabel extract -F flask_user/translations/babel.cfg -c NOTE -o flask_user/translations/flask_user.pot flask_user flask_user')
    for code in ('en', 'fi', 'fr', 'nl', 'sv', 'zh'):
        local('pybabel init -i flask_user/translations/flask_user.pot --domain=flask_user --output-dir flask_user/translations -l '+code)
    local('pybabel compile -f --domain=flask_user --directory flask_user/translations')

@task
def docs():
    local('cp example_apps/*_app.py docs/source/includes/.')
    local('sphinx-build -b html docs/source ../builds/flask_user/docs')
    local('cd ../builds/flask_user/docs && zip -u -r flask_user_docs *')

@task
def rebuild_docs():
    local('rm -fr ../builds/flask_user/docs')
    docs()

@task
def upload_to_pypi():
    local('python setup.py sdist upload')