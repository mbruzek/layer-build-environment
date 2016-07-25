import os

from shelx import split
from subprocess import check_output

from charms.reactive import when
from charms.reactive import when_not
from charms.reactive import set_state

from charmhelpers import fetch
from charmhelpers.core import hookenv



@when_not('build-environment.installed')
def install_build_environment():
    """Install the base packages for the build environment."""
    hookenv.status_set('maintenance', 'Installing the base packages.')
    base_packages = ['build-essential', 'git', 'make', 'python-pip']
    fetch.apt_update()
    fetch.apt_install(fetch.filter_installed_packages(base_packages))
    hookenv.status_set('active', 'Base packages installed, ready to build.')
    set_state('build-environment.installed')


@when('build-environment.installed', 'config.changed.install-repo')
def clone_install_repository():
    """Pull the repository that has the pre-build install instructions."""
    hookenv.status_set('maintenance', 'Pulling the install repository.')
    install_repo = hookenv.config()['install-repo']
    clone_repository(build_repo, 'install-repository')
    set_state('build-environment.install-repo')


@when('build-environment.installed', 'config.changed.build-repo')
def clone_build_repository():
    """Pull the repository to build."""
    hookenv.status_set('maintenance', 'Pulling the build repository.')
    build_repo = hookenv.config()['build-repo']
    clone_repository(build_repo, 'build-repository')
    set_state('build-environment.repo-pulled')


@when('build-environment.installed', 'build-environment.install-repo')
@when_not('build-environment.repository-installed')
def install_repository():
    """Execute the preinstall instructions from the install repository."""
    directory = 'install-repository'
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path) and os.access(path, os.X_OK):
            print(path)
            output = subprocess.check_output([path])
            print(output)
            

def clone_repository(repository, destination):
    """Clone the repository to the destination directory."""
    git_clone_command = 'git clone {0} {1}'.format(repository, destination)
    print(git_clone_command)
    clone_output = subprocess.check_output(split(git_clone_command))
    print(clone_output)
    return clone_output
