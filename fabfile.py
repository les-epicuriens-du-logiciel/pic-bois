import sys
from fabric.context_managers import prefix
from fabric.decorators import task
from fabric.operations import local

VIRTUALENV = '.py27'


@task(default=True)
def default():
    lint_py()
    test_py()
    lint_js()
    test_js()


@task
def setup():
    local('npm install')
    local('virtualenv --distribute --python=python2.7 {env}'.format(env=VIRTUALENV))
    install_requirements()


@task
def install_requirements():
    with prefix(_activate_virtual_env()):
        local('pip install -r requirements.txt --use-mirrors')
        local('pip install -r requirements-test.txt --use-mirrors')


@task
def clean():
    local('./build/clean.sh')


@task
def deploy():
    local('git push heroku python:master')


@task
def lint_py():
    with prefix(_activate_virtual_env()):
        local('pylint --rcfile=./build/pylintrc --reports=n features picbois')


@task
def test_py():
    with prefix(_activate_virtual_env()):
        local('nosetests')


@task
def lint_js():
    local('./node_modules/.bin/jshint --verbose --config build/jshintrc client/src')


@task
def test_js():
    local('PHANTOMJS_BIN=./node_modules/.bin/phantomjs '
          './node_modules/.bin/karma start --single-run --browsers PhantomJS build/karma.conf.js')


@task
def karma(*args):
    local('./node_modules/.bin/karma {command} build/karma.conf.js'.format(command=args[0]))


@task
def run_server():
    with prefix(_activate_virtual_env()):
        local("python -c 'import picbois; picbois.APP.run(port=8000)'")


@task
def run_client():
    with prefix('cd client'):
        local('python -m SimpleHTTPServer 5000')


def _activate_virtual_env():
    if not hasattr(sys, 'real_prefix'):
        return '. {env}/bin/activate'.format(env=VIRTUALENV)
    else:
        return 'true'
