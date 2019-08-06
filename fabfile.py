import os
from fabric.context_managers import cd, settings
from fabric.operations import run, sudo
from fabric.state import env


def legacy():
    env.hosts = ['52.209.114.249']
    env.rapidpro_user = 'www-data'
    env.code_dir = '/var/www/data_api'
    env.virtualenv_home = '/var/www/.virtualenvs/api'
    env.supervisor_process_web = 'api'
    env.supervisor_process_celery = 'data_celery_workers:*'


def production():
    env.hosts = ['rapidpro-api.unicef.io']
    env.rapidpro_user = 'rapidpro'
    env.code_dir = '/home/rapidpro/projects/rapidpro_warehouse'
    env.virtualenv_home = '/home/rapidpro/.virtualenvs/rapidpro_warehouse-4-gga9bH'
    env.supervisor_process_web = 'rapidpro-django'
    env.supervisor_process_celery = None  # celery not setup yet
    env.user = 'dwadmin'
    env.settings_module = 'data_api.settings_production'


def deploy(restart_celery=True, user='www-data', git_hash=None):
    source = 'https://github.com/rapidpro/data_api.git'
    env.rapidpro_user = env.rapidpro_user or user
    workon_home = os.path.join(env.virtualenv_home, 'bin')
    print("Starting deployment")
    django_settings_env = {}
    if env.settings_module:
        django_settings_env['DJANGO_SETTINGS_MODULE'] = env.settings_module
    with settings(warn_only=True):
        if run("test -d %s" % env.code_dir).failed:
            run("git clone %s %s" % (source, env.code_dir))
            with cd(env.code_dir):
                run("git config core.filemode false")
    with cd(env.code_dir):
        _rapidpro_sudo("git stash")
        _rapidpro_sudo("git fetch")
        if not git_hash:
            _rapidpro_sudo("git checkout master")
            _rapidpro_sudo("git pull %s master" % source)
        else:
            _rapidpro_sudo("git checkout %s" % git_hash)
        # required because fabric sudo doesn't seem to support -i option which
        # we need to get pipenv on the path
        run("cd {} && sudo -i -u {} pipenv install --ignore-pipfile".format(
            env.code_dir,
            env.rapidpro_user)
        )
        _rapidpro_sudo('%s/python manage.py collectstatic --noinput' % workon_home,
                       environment_vars=django_settings_env)
        _rapidpro_sudo('%s/python manage.py migrate --noinput' % workon_home,
                       environment_vars=django_settings_env)

        sudo("chown -R %s:%s ." % (env.rapidpro_user, env.rapidpro_user))

    sudo("supervisorctl restart %s" % env.supervisor_process_web)
    if restart_celery and env.supervisor_process_celery:
        sudo("supervisorctl restart {}".format(env.supervisor_process_celery))


def _rapidpro_sudo(command, environment_vars=None):
    """
    Runs a command as env.rapidpro_user
    """
    command = '{} {}'.format(
        _env_to_string(environment_vars),
        command,
    )
    sudo(command, user=env.rapidpro_user)


def _env_to_string(environment_dict):
    if environment_dict:
        return ' '.join('{}={}'.format(k, v) for k, v in environment_dict.items())
    else:
        return ''
