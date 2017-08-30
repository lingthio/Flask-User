from fabric.api import task
from fabric.operations import local


@task
def runserver():
    local('python runserver.py')

@task
def runapp(appname):
    local('PYTHONPATH=. python example_apps/'+appname+'_app.py')

@task
def update_babel():
    local('pybabel extract -F flask_user/translations/babel.cfg -k lazy_gettext -c NOTE -o flask_user/translations/flask_user.pot flask_user flask_user')
    for code in ('de', 'en', 'es', 'fa', 'fi', 'fr', 'it', 'nl', 'ru', 'sv', 'tr', 'zh'):
        local('pybabel update -i flask_user/translations/flask_user.pot --domain=flask_user --output-dir flask_user/translations -l '+code)
    local('pybabel compile -f --domain=flask_user --directory flask_user/translations')

@task
def test():
    # Requires "pip install pytest"
    local('py.test flask_user/tests/')

@task
def cov():
    # Requires "pip install pytest-coverage"
    local('py.test --cov flask_user --cov-report term-missing --cov-config flask_user/tests/.coveragerc flask_user/tests/')

@task
def docs(rebuild=False):
    local('cp example_apps/*_app.py docs/source/includes/.')
    options=''
    if rebuild:
        options += ' -E'
    local('sphinx-build -b html -a {options} docs/source ../builds/flask_user1/docs'.format(options=options))
    local('cd ../builds/flask_user1/docs && zip -u -r flask_user1_docs *')

@task
def rebuild_docs():
    local('cp example_apps/*_app.py docs/source/includes/.')
    local('sphinx-build -b html -a -E docs/source ../builds/flask_user1/docs')
    local('cd ../builds/flask_user1/docs && zip -u -r flask_user1_docs *')

# sphinx-apidoc -f -o docs/source flask_user flask_user/tests flask_user/db_adapters
# rm docs/source/flask_user.rst docs/source/modules.rst

@task
def upload_to_pypi():
    update_babel()
    rebuild_docs()
    local('python setup.py sdist')
    local('twine upload dist/*')

# PyEnv: https://gist.github.com/Bouke/11261620
# PyEnv and Tox: https://www.holger-peters.de/using-pyenv-and-tox.html
# Available Python versions: pyenv install --list
@task
def setup_tox():
    versions_str = '2.6.9 2.7.13 3.3.6 3.4.6 3.5.3 3.6.2'
    versions = versions_str.split()
    for version in versions:
        local('pyenv install --skip-existing '+version)
    local('pyenv global '+versions_str)

@task
def tox():
    local('tox')
