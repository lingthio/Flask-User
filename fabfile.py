from fabric.api import task
from fabric.operations import local


@task
def runserver():
    local('python runserver.py')

@task
def runapp(appname):
    local('PYTHONPATH=. python example_apps/'+appname+'.py')

@task
def babel(command):
    # Generate the .pot file from source code files
    if command=='extract':
        local('pybabel extract -F flask_user/translations/babel.cfg -k lazy_gettext -c NOTE -o flask_user/translations/flask_user.pot --project Flask-User --version v1.0.0.0 flask_user flask_user')

    # Update .po files from the .pot file
    elif command=='update':
        local('pybabel update -i flask_user/translations/flask_user.pot --domain=flask_user --output-dir flask_user/translations')
    elif command=='compile':
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
def cov2():
    # Requires "pip install pytest-coverage"
    local('py.test --cov flask_user --cov-report term-missing --cov-config flask_user/tests/.coveragerc flask_user/tests/test_views.py')

@task
def profiling():
    # Requires "pip install pytest-profiling"
    local('py.test --profile flask_user/tests/')


@task
def docs(rebuild=False):
    # local('cp example_apps/*_app.py docs/source/includes/.')
    options=''
    if rebuild:
        options += ' -E'
    local('sphinx-build -b html -a {options} docs/source ../builds/flask_user1/docs'.format(options=options))
    local('cd ../builds/flask_user1/docs && zip -u -r flask_user1_docs *')

# sphinx-apidoc -f -o docs/source flask_user flask_user/tests flask_user/db_adapters
# rm docs/source/flask_user.rst docs/source/modules.rst

# PyEnv: https://gist.github.com/Bouke/11261620
# PyEnv and Tox: https://www.holger-peters.de/using-pyenv-and-tox.html
# Available Python versions: pyenv install --list
@task
def setup_tox():
    versions_str = '2.7.17 3.4.10 3.5.9 3.6.9 3.7.5 3.8.0'
    versions = versions_str.split()
    for version in versions:
        local('pyenv install --skip-existing '+version)
    local('pyenv local '+versions_str)

@task
def tox():
    local('tox')

@task
def start_mongodb():
    local('mongod -dbpath ~/mongodb/data/db')

@task
def build_dist():
    # Compile translation files
    babel('compile')
    # Build distribution file
    local('rm -f dist/*')
    local('python setup.py sdist')

@task
def upload_to_pypi():
    build_dist()
    local('twine upload dist/*')

