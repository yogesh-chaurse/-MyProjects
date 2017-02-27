__author__ = 'yogesh'
"""
Fabric command script for project MagPIE.
"""
from fabric.api import task, local


@task
def pep8():
    """
    Checks our code formatting against several PEP8 conventions.
    """
    local('pylint --rcfile=pylint.rc MagPie/WebApp/')


@task
def check_code():
    pep8()

