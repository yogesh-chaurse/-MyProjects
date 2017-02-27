"""
Fabric command script for project MagPIE.
"""
__author__ = 'Richa Sharma <richa@weboniselab.com>'

from fabric.api import task, local


@task
def pep8():
    """
    Checks our code formatting against several PEP8 conventions.
    """
    local('pylint --rcfile=pylint.rc MagPie/CMS/')


@task
def check_code():
    pep8()

